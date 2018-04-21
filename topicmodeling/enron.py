import nltk
import matplotlib
matplotlib.use('Agg')
import sys
import time
sys.path.append('/home/lexkoz_yan/MailDiscoveryML')
#nltk.download()

from topicmodeling.lib.visualization.visualizer import Visualizer
from topicmodeling.lib.baseline.lsa import LsaModel
from topicmodeling.lib.baseline.lda import LdaModel
from topicmodeling.lib.baseline.ldamulticore import LdaMulticoreModel

path = '/home/lexkoz_yan/results/ldamodels/test/'
corpus_path = '/home/lexkoz_yan/maildiscovery/maildir/'
modelpath = '/home/lexkoz_yan/models/ldamodels/test/ldamodel'


def main():
    model = LdaMulticoreModel()
    #model.load(path=modelpath)
    model.extract_corpus(corpus_path)
    model.data_processing()
    start = time.time()
    model.build(num_topics=10, passes=1, path=modelpath, workers=7)
    end = time.time()
    print(str(end - start))

    #docs_words = model.get_docs()
    #topics_words = model.get_topics()

    #topics_top_terms = model.show_topics(num_topics=10, formatted=False)

    #Visualizer(docs_words, topics_words, topics_top_terms).run(path, metrics='tfIdf', proc_num=7)

if __name__ == '__main__':
    main()
