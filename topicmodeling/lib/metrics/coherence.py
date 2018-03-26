import numpy as np
from topicmodeling.lib.metrics.metricsABC import MetricsABC


class Coherence(MetricsABC):
    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 0]
        words_docs_for_topic = (self.docs_words[:, words_index]).T

        tmp = np.repeat(words_docs_for_topic[:, np.newaxis, :], words_docs_for_topic.shape[0], axis=1)
        tmp = (tmp * words_docs_for_topic > 0).sum(axis=-1)
        self.metrics[topic_id] = np.log(tmp / np.diagonal(tmp) + self.smoothing).sum() - \
                                 tmp.shape[0] * np.log(1 + self.smoothing)
        self.is_calculated[topic_id] = True

        return self.metrics[topic_id]
