import numpy as np
from topicmodeling.lib.metrics.metricsABC import MetricsABC


class TfIdf(MetricsABC):
    def __init__(self, docs_words, topics_words, smoothing=1):
        self.docs_words = docs_words
        self.topics_words = topics_words
        self.smoothing = smoothing
        self.metrics = np.zeros(topics_words.shape[0])
        self.is_calculated = np.zeros(topics_words.shape[0], dtype=np.bool)

    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        def tf_idf(word_id, document_id):
            tf = 0.5 + self.docs_words[document_id, word_id] / self.docs_words[document_id].max()
            idf = np.log(self.docs_words[document_id].sum() / (self.docs_words[:, word_id] > 0).sum())
            return tf * idf

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 0]

        tf_idf_for_words = np.zeros_like(words_index)
        for w in words_index:
            document_index = self.docs_words[:, w]
            document_index = np.arange(document_index.size)[document_index > 0]
            for d in document_index:
                tf_idf_for_words[w] += tf_idf(w, d)

        for w1 in words_index:
            for w2 in words_index:
                if w1 == w2:
                    continue

                step_sum = self.smoothing

                for d in self.docs_words.shape[0]:
                    if self.docs_words[d, w1] * self.docs_words[d, w2] > 0:
                        step_sum += tf_idf(w1, d) * tf_idf(w2, d)

                step_sum /= tf_idf_for_words[w1]
                self.metrics[topic_id] += np.log(step_sum)

        self.is_calculated[topic_id] = True
        return self.metrics[topic_id]

    def calculate_all_topics(self):
        for i in np.arange(self.topics_words.shape[0]):
            self.calculate_topic(i)
        return self.metrics
