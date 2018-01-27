# from nltk.stem.porter import PorterStemmer
# from nltk.stem.lancaster import LancasterStemmer
# from nltk.stem import SnowballStemmer
# from nltk.tokenize import wordpunct_tokenize
#
# def stemming(text, algorithm):
#     return " ".join([algorithm.stem(word) for word in wordpunct_tokenize(text.lower())])
#
# text = "this is some kind of text to read and make many kinds of analysis"
# porter_stemmer = PorterStemmer()
# print(stemming(text, porter_stemmer))
# lancaster_stemmer = LancasterStemmer()
# print(stemming(text, lancaster_stemmer))
# snowball_stemmer = SnowballStemmer("english")
# print(stemming(text, snowball_stemmer))
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN



lemmatizer = WordNetLemmatizer()
text = "this is some kind of text to read and make many kinds of analysis"
for w,f in nltk.pos_tag( wordpunct_tokenize(text.lower())):
    print(lemmatizer.lemmatize(w, get_wordnet_pos(f)))