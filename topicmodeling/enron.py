from topicmodeling.lib.visualization.visualizer import Visualizer
from topicmodeling.lib.baseline.lsa import LsaModel
from topicmodeling.lib.baseline.lda import LdaModel


path = '/home/geras-artem/Desktop'
corpus_path = '/home/geras-artem/Desktop/Study/6sem/InPrak/MailDiscoveryML//part/'


def main():
    model = LdaModel()
    # model.load()
    model.extract_corpus(corpus_path)
    model.data_processing()
    model.build(num_topics=20, passes=20)

    docs_words = model.get_docs()
    topics_words = model.get_topics()
    topics_top_terms = model.show_topics(num_topics=20, formatted=False)

    Visualizer(docs_words, topics_words, topics_top_terms).run(path, metrics='coherence')

if __name__ == '__main__':
    main()
