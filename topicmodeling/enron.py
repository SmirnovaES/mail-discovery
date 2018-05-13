from topicmodeling.lib.visualization.visualizer import Visualizer
from topicmodeling.lib.baseline.lsa import LsaModel
from topicmodeling.lib.baseline.lda import LdaModel
from topicmodeling.lib.baseline.ldamulticore import LdaMulticoreModel
import gc


path = '/home/geras-artem/Desktop/'
corpus_path = '/home/geras-artem/Desktop/Study/6sem/InPrak/MailDiscoveryML/data/maildir/'
part_path = '/home/geras-artem/Desktop/Study/6sem/InPrak/MailDiscoveryML/data/maildir/arnold-j/sent'
model_path = '/home/geras-artem/Desktop/ldamodel_part1'


def main():
    model = LdaMulticoreModel(sourse=part_path)
    model.load(path=model_path)
    # model.build(num_topics=10, passes=20, workers=8, path=model_path)

    docs_words = model.get_docs()
    topics_words = model.get_topics()
    topics_top_terms = model.show_topics(num_topics=10, formatted=False)

    del model
    gc.collect()

    Visualizer(docs_words, topics_words, topics_top_terms).run(path)

if __name__ == '__main__':
    main()
