from abc import ABCMeta, abstractmethod
import numpy as np

class MetricsABC():
    __metaclass__=ABCMeta

    def __init__(self, docs_words, topics_words, smoothing=1):
        self.docs_words = docs_words
        self.topics_words = topics_words
        self.smoothing = smoothing
        self.metrics = np.zeros(topics_words.shape[0])
        self.is_calculated = np.zeros(topics_words.shape[0], dtype=np.bool)

    @abstractmethod
    def calculate_topic(self, topic_id):
        """Calculates metrics for one topic"""

    def calculate_all_topics(self):
        """Calculates metrics for all the topics"""
        for i in np.arange(self.topics_words.shape[0]):
            self.calculate_topic(i)
        return self.metrics
