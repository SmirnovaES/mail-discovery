from topicmodeling.lib.metrics.metricsABC import MetricsABC
import numpy as np
from joblib import Parallel, delayed


def tf_idf(obj, word_id, document_id):
    if obj.docs_words[document_id, word_id] == 0:
        return 0
    else:
        tf = 0.5 + obj.docs_words[document_id, word_id] / obj.docs_words[document_id].max()
        idf = np.log(obj.docs_words.shape[0] / (obj.docs_words[:, word_id] > 0).sum())
        return tf * idf


def parallel_task(w1, w2, values, smoothing):
    return np.log((smoothing + np.sum(values[:, w1] * values[:, w2])) / np.sum(values[:, w1]))


class TfIdf(MetricsABC):
    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 1e-3]

        tf_idf_values = Parallel(n_jobs=self.proc_num)(
            delayed(tf_idf)(self, w, d) for d in range(self.docs_words.shape[0])
                                        for w in words_index
        )
        tf_idf_values = np.array(tf_idf_values).reshape((self.docs_words.shape[0], words_index.size))

        result = Parallel(n_jobs=self.proc_num)(
            delayed(parallel_task)(i, j, tf_idf_values, self.smoothing) for i in range(words_index.size)
                                                                        for j in range(words_index.size)
                                                                        if i != j
        )

        self.is_calculated[topic_id] = True
        self.metrics[topic_id] = sum(result)
        return self.metrics[topic_id]
