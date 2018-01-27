from nltk.corpus import stopwords, wordnet
from nltk.tokenize import wordpunct_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re, csv, nltk

class Preprocessing:

    algorithms = ["stopword","porter","lancaster","snowball_english","wordnetlemmatizer"]
    stop_words = set(stopwords.words('english'))


    def __init__(self, file, algorithm):
        self.file = file
        if algorithm in self.algorithms:
            self.algorithm = algorithm
        else:
            raise ForbiddenAlgorithmException

    def run_algorithm(self):
        if self.algorithm == 'stopword':
            return self.run_stopwords()
        elif self.algorithm == 'porter':
            porter_stemmer = PorterStemmer()
            return self.run_stemming(porter_stemmer)
        elif self.algorithm == 'lancaster':
            lancaster_stemmer = LancasterStemmer()
            return self.run_stemming(lancaster_stemmer)
        elif self.algorithm == 'snowball_english':
            snowball_stemmer = SnowballStemmer("english")
            return self.run_stemming(snowball_stemmer)
        elif self.algorithm == 'wordnetlemmatizer':
            lemmatizer = WordNetLemmatizer()
            return self.run_lemmatization(lemmatizer)


    def run_stemming(self, stemmer):
        with open(self.file+"new", 'w') as csvoutfile:
            with open(self.file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                writer = csv.DictWriter(csvoutfile, fieldnames=reader.fieldnames, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                for row in reader:
                    row['title'] = " ".join(
                        [stemmer.stem(word) for word in wordpunct_tokenize(row['title'].lower())])
                    row['content'] = " ".join(
                        [stemmer.stem(word) for word in wordpunct_tokenize(row['content'].lower())])
                    writer.writerow(row)
        return self.file+"new"

    def run_lemmatization(self, lemmatization):
        with open(self.file+"new", 'w') as csvoutfile:
            with open(self.file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                writer = csv.DictWriter(csvoutfile, fieldnames=reader.fieldnames, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                for row in reader:
                    row['title'] = " ".join(
                        [lemmatization.lemmatize(word, get_wordnet_pos(func)) for word, func in nltk.pos_tag(wordpunct_tokenize(row['title'].lower()))])
                    row['content'] = " ".join(
                        [lemmatization.lemmatize(word, get_wordnet_pos(func)) for word, func in nltk.pos_tag(wordpunct_tokenize(row['content'].lower()))])
                    writer.writerow(row)
        return self.file+"new"

    def run_stopwords(self):
        self.stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}'])
        with open(self.file+"new", 'w') as csvoutfile:
            with open(self.file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                writer = csv.DictWriter(csvoutfile, fieldnames=reader.fieldnames, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                for row in reader:
                    row['title'] = " ".join(
                        [word for word in wordpunct_tokenize(row['title']) if word.lower() not in self.stop_words])
                    row['content'] = " ".join(
                        [word for word in wordpunct_tokenize(row['content']) if word.lower() not in self.stop_words])
                    writer.writerow(row)
        return self.file+"new"

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



class ForbiddenAlgorithmException(Exception):
    pass