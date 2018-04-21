import numpy as np
from joblib import Parallel, delayed
from topicmodeling.lib.metrics.metricsABC import MetricsABC
from tqdm import tqdm


def parallel_task(obj, w1, w2):
    return np.log((obj.smoothing + (obj.docs_words[:, w1] * obj.docs_words[:, w2] > 0).sum()) /
                  (obj.docs_words[:, w1] > 0).sum())


class Coherence(MetricsABC):
    def calculate_topic(self, topic_id):
        if self.is_calculated[topic_id]:
            return self.metrics[topic_id]

        topic_distribution = self.topics_words[topic_id]
        words_index = np.arange(topic_distribution.size)[topic_distribution > 1e-4]

        result = Parallel(n_jobs=self.proc_num, max_nbytes='250M', mmap_mode='r+')(
            delayed(parallel_task)(self, words_index[i], words_index[j]) for i in tqdm(range(words_index.size))
                                                                         for j in range(words_index.size)
                                                                         if i != j
        )

        self.is_calculated[topic_id] = True
        self.metrics[topic_id] = sum(result)
        return self.metrics[topic_id]
