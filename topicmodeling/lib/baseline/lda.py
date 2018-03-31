from topicmodeling.lib.baseline.baselineABC import BaselineABC
from gensim import models


class LdaModel(BaselineABC):
    def build(self, num_topics=10, passes=10, path='/home/geras-artem/Desktop/ldamodel'):
        if self.model is None:
            self.model = models.ldamodel.LdaModel(self.corpus, num_topics=num_topics,
                                                  id2word=self.dictionary, passes=passes)
        self.model.save(path)
        return self.model

    def load(self, path='/home/geras-artem/Desktop/ldamodel'):
        self.model = models.ldamodel.LdaModel.load(path, mmap='r')
        return self.model

    def get_topics(self):
        if self.topic_terms is None:
            self.topic_terms = self.model.get_topics()
        return self.topic_terms

    def show_topics(self, num_topics=10, num_words=10, log=False, formatted=True):
        return self.model.show_topics(num_topics, num_words, log, formatted)
