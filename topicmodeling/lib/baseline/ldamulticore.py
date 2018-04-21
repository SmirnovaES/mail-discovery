from topicmodeling.lib.baseline.baselineABC import BaselineABC
from gensim import models


class LdaMulticoreModel(BaselineABC):
    def build(self, num_topics=10, passes=10, workers=1, path='/home/ldamodel'):
        print('Started building model')
        if self.model is None:
            self.model = models.ldamulticore.LdaMulticore(self.corpus, num_topics=num_topics,
                                                  id2word=self.dictionary, passes=passes, workers=workers)
        self.model.save(path)
        print('Finished building model')
        return self.model

    def load(self, path='/home/ldamodel'):
        self.model = models.ldamulticore.LdaMulticore.load(path, mmap='r')
        return self.model

    def get_topics(self):
        if self.topic_terms is None:
            self.topic_terms = self.model.get_topics()
        return self.topic_terms

    def show_topics(self, num_topics=10, num_words=10, log=False, formatted=True):
        return self.model.show_topics(num_topics, num_words, log, formatted)
