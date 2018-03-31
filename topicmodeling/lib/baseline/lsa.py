from baselineABC import BaselineABC
from gensim import models


class LsaModel(BaselineABC):

    def build(self, num_topics=10):
        if self.model is None:
            self.model = models.lsimodel.LsiModel(self.corpus, num_topics=num_topics,
                                                 id2word=self.dictionary)
        return self.model

    def get_topics(self):
        if self.topic_terms is None:
            self.topic_terms = self.model.get_topics()
        return self.topic_terms

