import numpy as np
import matplotlib.pyplot as plt
from topicmodeling.lib.metrics.coherence import Coherence
from topicmodeling.lib.metrics.tfIdf import TfIdf
from os import cpu_count


class Visualizer:
    def __init__(self, docs_words, topics_words, topics_terms):
        self.docs_words = docs_words
        self.topics_words = topics_words
        self.topics_terms = topics_terms

    def run(self, path, metrics='tfIdf', proc_num=cpu_count()):
        def draw(ax, values, names, title):
            index = np.argsort(values, kind='mergesort')

            ax.barh(np.arange(values.size), values[index], align='center')

            ax.set_yticks(np.arange(values.size))
            ax.set_yticklabels(names[index])

            max_value = ax.get_xlim()[1] - ax.get_xlim()[0]
            for i, v in enumerate(values[index]):
                if v > max_value * 0.8:
                    shift = max_value * -0.1
                else:
                    shift = max_value * 0.1
                ax.text(v + shift, i - 0.1, str(round(v, 2)), fontweight='bold')

            ax.set_ylim((-0.6, values.size - 0.4))
            ax.set_title(title)
            ax.tick_params(
                axis='x',
                which='both',
                bottom='off',
                top='off',
                labelbottom='off')

        if metrics == 'coherence':
            metrics_model = Coherence(self.docs_words, self.topics_words, proc_num=proc_num)
        elif metrics == 'tfIdf':
            metrics_model = TfIdf(self.docs_words, self.topics_words, proc_num=proc_num)
        else:
            raise ValueError('wrong metrics name: {}'.format(metrics))

        # Some calculations
        topics_metrics = metrics_model.calculate_all_topics()
        topics_num = topics_metrics.size
        topics_names = np.array(['Topic #{}'.format(i + 1) for i in range(topics_num)])
        index = np.argsort(topics_metrics, kind='mergesort')
        topics_metrics = topics_metrics[index]
        topics_names = topics_names[index]

        # Draw general info
        fig = plt.figure(figsize=(15, 0.5 * topics_num))
        ax = fig.add_subplot(111)
        draw(ax, topics_metrics, topics_names, metrics)
        plt.savefig(path + '/general.pdf', dpi=300, format='pdf')

        # Draw info for each topic
        fig = plt.figure(figsize=(21, 5 * ((topics_num - 1) / 3 + 1)))
        for i in index[::-1]:
            ax = fig.add_subplot(topics_num / 3 + 1, 3, i + 1)
            names = np.array(list(map(lambda x: x[0], self.topics_terms[i][1])))
            probs = np.array(list(map(lambda x: x[1], self.topics_terms[i][1])))
            draw(ax, probs, names, topics_names[i] + ' ' + str(topics_metrics[i]))
        plt.savefig(path + '/topics.pdf', dpi=300, format='pdf')