import os
import re
import string
from abc import ABCMeta, abstractmethod

import nltk
import numpy as np
from gensim import corpora, matutils
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer


class BaselineABC:
    __metaclass__ = ABCMeta

    def __init__(self, source=None, lemmatizer=WordNetLemmatizer()):
        self.docs = list()
        self.texts = list()
        self.corpus = list()
        self.docs_terms = None
        self.docs_topics = None
        self.topic_terms = None
        self.dictionary = None
        self.model = None
        self.count_vectorizer = None
        self.num_topics = None
        self.lemmatizer = lemmatizer

        if isinstance(source, str):
            self.extract_corpus(path=source)
        elif isinstance(source, list):
            self.texts = source
        else:
            raise ValueError('Invalid value of source: {}'.format(source))

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text)
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens

    @staticmethod
    def preprocess(text):
        text = text.lower()
        text = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', "", text)
        text = re.sub(r"\S*@\S*\s?", '', text)
        allow = string.ascii_letters + string.whitespace
        text = re.sub('[^%s]' % allow, '', text)
        return text

    def extract_corpus(self, path):
        for subdir, dirs, files in os.walk(path):
            for file in files:
                file_path = subdir + os.path.sep + file
                shakes = open(file_path, 'r')
                text = shakes.read()
                self.texts.append(text)

    def vectorize(self, **kwargs):
        # this can take some time
        self.count_vectorizer = CountVectorizer(preprocessor=self.preprocess, tokenizer=self.tokenize,
                                                stop_words='english', **kwargs)
        self.docs_terms = self.count_vectorizer.fit_transform(self.texts)
        return self.docs_terms, self.count_vectorizer

    def count_num_topics(self):
        if self.num_topics is None:
            self.num_topics = self.docs_terms.sum(axis=0) > 100
            self.num_topics = self.num_topics.sum() / 200
            self.num_topics = np.min([30, self.num_topics])
            self.num_topics = np.max([3, self.num_topics])

    def do_processing(self):
        self.vectorize(min_df=1e-3, max_df=1.)
        self.corpus = [matutils.scipy2sparse(doc) for doc in self.docs_terms]
        self.dictionary = corpora.Dictionary([list(self.count_vectorizer.get_feature_names())])
        self.count_num_topics()

    @abstractmethod
    def build(self, num_topics=None, passes=10, workers=os.cpu_count(), path='/home/geras-artem/ldamodel'):
        """Builds the selected model"""

    @abstractmethod
    def get_topics(self):
        """Returns num_topics x num_terms size numpy.ndarray"""

    @abstractmethod
    def show_topics(self, num_topics=-1, num_words=10, log=False, formatted=True):
        """Returns result of show_topics of model"""

    def get_docs(self):
        return self.docs_terms

    def get_id2token(self):
        return self.dictionary.id2token

    def get_token2id(self):
        return self.dictionary.token2id

    def get_docs_topics(self):
        if self.docs_topics is None:
            self.docs_topics = np.zeros((len(self.texts), self.model.num_topics))
            for i, doc in enumerate(self.corpus):
                dist = self.model.get_document_topics(doc)
                for id, prob in dist:
                    self.docs_topics[i][id] = prob
        return self.docs_topics

    def get_topics_names(self, words_per_topic=3):
        words_for_topic = self.show_topics(num_topics=self.model.num_topics, num_words=words_per_topic, formatted=False)
        words_for_topic = [[x[0] for x in topic[1]] for topic in words_for_topic]
        return words_for_topic
