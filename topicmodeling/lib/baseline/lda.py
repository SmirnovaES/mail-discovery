from baselineABC import BaselineABC
from gensim import models


class LdaModel(BaselineABC):

    def build(self, num_topics=10, passes=10):
        if self.model is None:
            self.model = models.ldamodel.LdaModel(self.corpus, num_topics=num_topics,
                                                 id2word=self.dictionary, passes=passes)
        return self.model

    def get_topics(self):
        if self.topic_terms is None:
            self.topic_terms = self.model.get_topics()
        return self.topic_terms

