from abc import ABCMeta, abstractmethod
import nltk
from collections import defaultdict
from stop_words import get_stop_words
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from os import listdir, chdir
import re
from collections import defaultdict
import numpy as np
from gensim import corpora, models

re0 = re.compile('>')
re1 = re.compile('(Message-ID(.*?\n)*X-FileName.*?\n)|'
                 '(To:(.*?\n)*?Subject.*?\n)|'
                 '(< (Message-ID(.*?\n)*.*?X-FileName.*?\n))')
re2 = re.compile('(.+)@(.+)')  # Remove emails
re3 = re.compile('\s(-----)(.*?)(-----)\s', re.DOTALL)
re4 = re.compile('''\s(\*\*\*\*\*)(.*?)(\*\*\*\*\*)\s''', re.DOTALL)
re5 = re.compile('\s(_____)(.*?)(_____)\s', re.DOTALL)
re6 = re.compile('\n( )*-.*')
re7 = re.compile('\n( )*\d.*')
re8 = re.compile('(\n( )*[\w]+($|( )*\n))|(\n( )*(\w)+(\s)+(\w)+(( )*\n)|$)|'
                 '(\n( )*(\w)+(\s)+(\w)+(\s)+(\w)+(( )*\n)|$)')
re9 = re.compile('.*orwarded.*')
re10 = re.compile('From.*|Sent.*|cc.*|Subject.*|Embedded.*|http.*|\w+\.\w+|.*\d\d/\d\d/\d\d\d\d.*')
re11 = re.compile(' [\d:;,.]+ ')
re12 = re.compile('[\n\t]+')
re13 = re.compile('[\s]{2,}')


class BaselineABC():
    __metaclass__ = ABCMeta

    def __init__(self):
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

    @abstractmethod
    def get_topics(self):
        '''Returns num_topics x num_terms size numpy.ndarray'''

    def extract_corpus(self, path):
        docs = []  # all documents
        docs_num_dict = []  # Stores email sender's name and number
        chdir(path)
        names = [i for i in listdir()]
        m = 0
        for name in names:
            sent = path + str(name) + '/sent'
            try:
                chdir(sent)
                d = []
                for email in listdir():
                    text = open(email, 'r').read()
                    # Regular expressions are used below to remove 'clutter'
                    text = re.sub(re0, ' ', text)
                    text = re.sub(re1, ' ', text)
                    text = re.sub(re2, ' ', text)
                    text = re.sub(re3, ' ', text)
                    text = re.sub(re4, ' ', text)
                    text = re.sub(re5, ' ', text)
                    text = re.sub(re6, ' ', text)
                    text = re.sub(re7, ' ', text)
                    text = re.sub(re8, ' ', text)
                    text = re.sub(re9, ' ', text)
                    text = re.sub(re10, ' ', text)
                    text = re.sub(re11, ' ', text)
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
        tokenizer = RegexpTokenizer(r'\w+')

        self.texts = []

        for i in range(0, len(self.docs_num_dict.items())):
            new_docs_num_dict_1 = []
            for doc in self.docs_num_dict[i][1]:
                raw = doc.lower()
                tokens = tokenizer.tokenize(raw)
                en_stop = get_stop_words('en')
                stopped_tokens = [i for i in tokens if not i in en_stop]
                wordnet_lemmatizer = WordNetLemmatizer()
                lemmatized_tokens = [wordnet_lemmatizer.lemmatize(i) for i in stopped_tokens]
                self.texts.append(lemmatized_tokens)
                new_docs_num_dict_1.append(lemmatized_tokens)
                for word in lemmatized_tokens:
                    self.d[word] += 1
            self.docs_num_dict[i][1] = new_docs_num_dict_1

        docs_name_dict = []
        for i in range(0, len(self.docs_num_dict.items())):
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
        for doc in temp_texts:
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
        for i in range(self.docs_terms.shape[0]):
            temp_dic = self.dictionary.doc2bow(self.texts[i])
            for par in temp_dic:
                self.docs_terms[i][par[0]] = par[1]
        return self.docs_terms

