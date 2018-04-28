from topicmodeling.lib.baseline.lda import LdaModel
from topicmodeling.output.gettopics import getTopics


corpus_path = '/home/geras-artem/Desktop/Study/6sem/InPrak/MailDiscoveryML/part'
part_path = '/home/geras-artem/Desktop/Study/6sem/InPrak/MailDiscoveryML/data/maildir/arnold-j/sent'

if __name__ == '__main__':
    print(getTopics(source=part_path)[1][100])
