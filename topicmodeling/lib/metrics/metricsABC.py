from abc import ABCMeta, abstractmethod
from os import cpu_count
from time import time, sleep

import numpy as np


class MetricsABC:
    __metaclass__ = ABCMeta

    def __init__(self, docs_words, topics_words, proc_num=cpu_count(), smoothing=1):
        self.docs_words = docs_words
        self.topics_words = topics_words
        self.smoothing = smoothing
        self.metrics = np.zeros(topics_words.shape[0])
        self.is_calculated = np.zeros(topics_words.shape[0], dtype=np.bool)
        self.proc_num = proc_num

    @abstractmethod
    def calculate_topic(self, topic_id):
        """Calculates metrics for one topic"""

    def calculate_all_topics(self):
        """Calculates metrics for all the topics"""
        sleep(5)
        for i in range(self.topics_words.shape[0]):
            print('Calculating metrics for {}-th topic'.format(i))
            start = time()
            self.calculate_topic(i)
            end = time()
            print('It took {} seconds'.format(end - start))
        return self.metrics
