from topicmodeling.lib.metrics.metricsABC import MetricsABC
import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfTransformer


def parallel_task(w1, w2, values, smoothing):
    return np.log(smoothing + np.sum(values.getcol(w1).toarray() * values.getcol(w2).toarray()) / values.getcol(w1).sum())


class TfIdf(MetricsABC):
    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 1e-4]

        tf_idf_values = TfidfTransformer().fit_transform(self.docs_words[:, words_index])

        result = Parallel(n_jobs=self.proc_num, verbose=10, max_nbytes='250M')(
            delayed(parallel_task)(i, j, tf_idf_values, self.smoothing) for i in range(words_index.size)
                                                                        for j in range(words_index.size)
                                                                        if i != j
        )

        self.is_calculated[topic_id] = True
        self.metrics[topic_id] = sum(result)
        return self.metrics[topic_id]
