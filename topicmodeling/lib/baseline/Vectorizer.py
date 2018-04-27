import nltk
import string
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

'''
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed
'''


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [WordNetLemmatizer().lemmatize(i) for i in tokens]
    return lemmatized_tokens


def Vectorizer(path):
    token_dict = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file_path = subdir + os.path.sep + file
            shakes = open(file_path, 'r')
            text = shakes.read()
            lowers = text.lower()

            allow = string.ascii_letters + string.whitespace
            lowers = re.sub('[^%s]' % allow, '', lowers)

            # translator = str.maketrans('', '', string.punctuation)
            # no_punctuation = lowers.translate(translator)
            token_dict[file] = lowers

    # this can take some time
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_dict.values())
    return tfs, tfidf