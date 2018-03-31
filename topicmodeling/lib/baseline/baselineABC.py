from abc import ABCMeta, abstractmethod
import nltk
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from os import listdir, chdir
import re
from collections import defaultdict
import numpy as np
from gensim import corpora, models
from tqdm import tqdm


class BaselineABC:
    __metaclass__ = ABCMeta

    class Parser:
        def __init__(self):
            self.regulars = []
            self.regulars.append(re.compile('>'))
            self.regulars.append(re.compile('(Message-ID(.*?\n)*X-FileName.*?\n)|'
                             '(To:(.*?\n)*?Subject.*?\n)|'
                             '(< (Message-ID(.*?\n)*.*?X-FileName.*?\n))'))
            self.regulars.append(re.compile('(.+)@(.+)'))  # Remove emails
            self.regulars.append(re.compile('\s(-----)(.*?)(-----)\s', re.DOTALL))
            self.regulars.append(re.compile('''\s(\*\*\*\*\*)(.*?)(\*\*\*\*\*)\s''', re.DOTALL))
            self.regulars.append(re.compile('\s(_____)(.*?)(_____)\s', re.DOTALL))
            self.regulars.append(re.compile('\n( )*-.*'))
            self.regulars.append(re.compile('\n( )*\d.*'))
            self.regulars.append(re.compile('(\n( )*[\w]+($|( )*\n))|(\n( )*(\w)+(\s)+(\w)+(( )*\n)|$)|'
                             '(\n( )*(\w)+(\s)+(\w)+(\s)+(\w)+(( )*\n)|$)'))
            self.regulars.append(re.compile('.*orwarded.*'))
            self.regulars.append(re.compile('From.*|Sent.*|cc.*|Subject.*|Embedded.*|http.*|\w+\.\w+|.*\d\d/\d\d/\d\d\d\d.*'))
            self.regulars.append(re.compile(' [\d:;,.]+ '))
            self.regulars.append(re.compile('[\n\t]+'))
            self.regulars.append(re.compile('[\s]{2,}'))

        def parse(self, text):
            for reg in self.regulars:
                text = re.sub(reg, ' ', text)
            return text

    def __init__(self, parser=Parser, tokenizer=RegexpTokenizer(r'\w+'), lemmatizer=WordNetLemmatizer(),
                 embedding=None, clf_embed=None, n_clusters_embed=None, emb_del_unknown=False, emb_limit=0):
        self.docs_num_dict = {}
        self.docs = []
        self.d = {}  # global counter of words # depricated, use self.dictioanry instead
        self.texts = []  # [lem_words_of_doc1, ...]
        self.docs_name_dict = {}  # {name: {lem_word1: num1, lem_word2: num2, ...}}
        self.dictionary = []
        self.corpus = []
        self.docs_terms = None
        self.model = None
        self.topic_terms = None
        self.parser = parser()
        self.tokenizer = tokenizer
        self.lemmatizer = lemmatizer
        self.embedding = embedding
        self.clf_embed = clf_embed
        self.n_clusters_embed = n_clusters_embed
        self.emb_word2cluster = {}
        self.emb_del_unknown = emb_del_unknown
        self.emb_limit = emb_limit

    def embed(self):
        file = open(self.embedding)
        vec_of_words = []
        emb_words = []
        for line in tqdm(file, desc='embading'):
            nums = line.split()
            emb_words.append(nums[0])
            vec_of_words.append(nums[1:])
        y_pred = self.clf_embed(self.n_clusters_embed).fit_predict(vec_of_words)
        lemmatized_emb_words = [self.lemmatizer.lemmatize(i) for i in emb_words]
        if self.emb_limit == 0:
            self.emb_limit = len(lemmatized_emb_words)
        self.emb_word2cluster = dict(zip(lemmatized_emb_words[: self.emb_limit], y_pred[: self.emb_limit]))

    @abstractmethod
    def get_topics(self):
        """Returns num_topics x num_terms size numpy.ndarray"""

    @abstractmethod
    def show_topics(self, num_topics=-1, num_words=10, log=False, formatted=True):
        """Returns result of show_topics of model"""

    def extract_corpus(self, path):
        docs = []  # all documents
        docs_num_dict = []  # Stores email sender's name and number
        chdir(path)
        names = [i for i in listdir()]
        m = 0
        for name in tqdm(names, desc='extract_corpus'):
            sent = path + str(name) + '/sent'
            try:
                chdir(sent)
                d = []
                for email in listdir():
                    text = open(email, 'r').read()
                    text = self.parser.parse(text)
                    docs.append(text)
                    d.append(text)
                docs_num_dict.append((m, [name, d]))
                m += 1
            except:
                pass

        self.docs_num_dict = dict(docs_num_dict)
        self.docs = docs

    def data_processing(self):
        self.d = defaultdict(int)

        self.texts = []

        for i in tqdm(range(0, len(self.docs_num_dict.items())),
                      desc='data_processing 1/3'):
            new_docs_num_dict_1 = []
            for doc in self.docs_num_dict[i][1]:
                raw = doc.lower()
                tokens = self.tokenizer.tokenize(raw)
                en_stop = stopwords.words('english')
                stopped_tokens = [i for i in tokens if not i in en_stop]
                lemmatized_tokens = [self.lemmatizer.lemmatize(i) for i in stopped_tokens if i.isdigit() == False]
                if self.embedding is not None:
                    self.embed()
                    if self.emb_del_unknown:
                        lemmatized_tokens = [self.emb_word2cluster[i] for i in lemmatized_tokens if i in self.emb_word2cluster]
                    else:
                        lemmatized_tokens = [self.emb_word2cluster[i] if i in self.emb_word2cluster else self.emb_word2cluster["unk"] for i in lemmatized_tokens]
                self.texts.append(lemmatized_tokens)
                new_docs_num_dict_1.append(lemmatized_tokens)
                for word in lemmatized_tokens:
                    self.d[word] += 1
            self.docs_num_dict[i][1] = new_docs_num_dict_1

        docs_name_dict = []
        for i in tqdm(range(0, len(self.docs_num_dict.items())),
                      desc='data_processing 2/3'):
            temp_dict = defaultdict(int)
            for j in self.docs_num_dict[i][1]:
                for k in j:
                    temp_dict[k] += 1
            # Append the temporary dictionary to docs_name_dict
            docs_name_dict.append((self.docs_num_dict[i][0], temp_dict))
        self.docs_name_dict = dict(docs_name_dict)

        num_docs = len(self.texts)
        temp_texts = self.texts
        self.texts = []
        upper_lim = int(0.20 * num_docs)
        for doc in tqdm(temp_texts,
                        desc='data_processing 3/3'):
            temp_doc = []
            for word in doc:
                # If the word is in the required interval, we add it to a NEW texts variable
                if 4 < self.d[word] < upper_lim and len(word) > 2:
                    temp_doc.append(word)
                # If the word is not in the required interval,
                # we lower the index of the word in the docs_name_dict dictinoary
                else:
                    for group in self.docs_name_dict.items():
                        person = group[0]
                        if word in self.docs_name_dict[person]:
                            if self.docs_name_dict[person][word] > 1:
                                self.docs_name_dict[person][word] -= 1
                            else:
                                del self.docs_name_dict[person][word]
            self.texts.append(temp_doc)

        self.dictionary = corpora.Dictionary(self.texts)
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]

    def get_docs(self):
        if self.docs_terms is not None:
            return self.docs_terms
        self.docs_terms = np.zeros((len(self.texts), len(self.dictionary)))
        for i in tqdm(range(self.docs_terms.shape[0]),
                      desc='get_docs'):
            temp_dic = self.dictionary.doc2bow(self.texts[i])
            for par in temp_dic:
                self.docs_terms[i][par[0]] = par[1]
        return self.docs_terms

    def get_id2token(self):
        return self.dictionary.id2token

    def get_token2id(self):
        return self.dictionary.token2id