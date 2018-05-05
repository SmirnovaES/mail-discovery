from gensim import models

from topicmodeling.lib.baseline.baselineABC import BaselineABC


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

    def show_topics(self, num_topics=10, num_words=10, log=False, formatted=True):
        # if num_topics = -1 - all topics will be in result (ordered by significance).
        return self.model.show_topics(num_topics, num_words, log, formatted)
