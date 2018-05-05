import numpy as np
from joblib import Parallel, delayed
from tqdm import tqdm

from topicmodeling.lib.metrics.metricsABC import MetricsABC


def parallel_task(w1, w2, values, smoothing):
    return np.log(smoothing + np.sum(values[:, w1] * values[:, w2]) / values[:, w1])


class Coherence(MetricsABC):
    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 1e-4]

        value = self.docs_words.toarray()[:, words_index]
        result = Parallel(n_jobs=self.proc_num, max_nbytes='250M', mmap_mode='r+')(
            delayed(parallel_task)(i, j, value, self.smoothing) for i in tqdm(range(words_index.size))
                                                                for j in range(words_index.size)
                                                                if i != j
        )

        self.is_calculated[topic_id] = True
        self.metrics[topic_id] = sum(result)
        return self.metrics[topic_id]
