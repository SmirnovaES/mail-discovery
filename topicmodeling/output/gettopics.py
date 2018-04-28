from topicmodeling.lib.baseline.ldamulticore import LdaMulticoreModel
from topicmodeling.lib.baseline.lda import  LdaModel
from topicmodeling.lib.baseline.lsa import LsaModel

def getTopics(source, words_per_topic=3, num_topics=10, passes=10,modelClass=LdaMulticoreModel):
    model = modelClass(sourse=source)
    model.do_processing()
    model.build(num_topics=num_topics, passes=passes)
    return model.show_topics(num_topics=10, formatted=False), model.get_docs_topics()