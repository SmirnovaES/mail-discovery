from topicmodeling.lib.baseline.ldamulticore import LdaMulticoreModel
from topicmodeling.lib.baseline.lda import  LdaModel
from topicmodeling.lib.baseline.lsa import LsaModel


def getTopics(source, words_per_topic=3, num_topics=None, passes=10, modelClass=LdaMulticoreModel):
    model = modelClass(source=source)
    model.do_processing()
    model.build(num_topics=num_topics, passes=passes)
    return model.get_topics_names(words_per_topic=words_per_topic), model.get_docs_topics()
