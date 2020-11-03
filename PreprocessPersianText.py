import pickle
import time
from hazm import *
from nltk import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
import xmltodict
import csv


def ReadFile(filename):
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def CleanPersionDoc(doc):
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    normalizer = Normalizer()
    doc = normalizer.normalize(doc)
    tokenized = word_tokenize(doc)
    stemmed = [stemmer.stem(w) for w in tokenized]
    new_words = [word for word in stemmed if word.isalnum()]
    lemmatized = [lemmatizer.lemmatize(w) for w in new_words]
    return lemmatized


def Preprocess():
    st = time.time()
    all_persion_tokens = []
    persion_file = open('./PersianFiles/Persian.xml')
    doc = xmltodict.parse(persion_file.read())
    persian_tokenized_text = {}  # docid : []
    for i in range(len(doc['mediawiki']['page'])):
        clean_text = list(CleanPersionDoc(doc['mediawiki']['page'][i]['revision']['text']['#text']))
        all_persion_tokens = all_persion_tokens + clean_text
        persian_tokenized_text[i] = clean_text
    with open('./PersianFiles/persian_tokenized_text.pickle', 'wb') as f:
        pickle.dump(persian_tokenized_text, f)
    return all_persion_tokens


def PlotPersianStopwords(all_persion_tokens):
    fdist = FreqDist(all_persion_tokens)
    most_common = fdist.most_common(40)
    stopwords_persion = []
    for w in most_common:
        stopwords_persion.append(w[0])
    fdist.plot(30, cumulative=False)
    plt.show()
    f = open("./PersianFiles/stopwords_persion.txt", "a")
    f.write(str(stopwords_persion))
    f.close()


def GetStopwords():
    f = open("./PersianFiles/stopwords_persion.txt", "r")
    stop_words = f.read()
    stop_words = stop_words.replace('\'', '')
    stop_words = stop_words.replace('[', '')
    stop_words = stop_words.replace(']', '')
    stop_words = stop_words.replace(' ', '')
    stop_words = stop_words.split(",")
    return stop_words


def RemoveStopwordDoc(doc, stop_words, csv_file):
    writer1 = csv.writer(csv_file)
    for token in doc:
        if token in stop_words:
            doc.remove(token)
    writer1.writerow([list(doc)])
    return doc


def RemoveStopwordsAllPersianFile():
    persian_tokenized_file = open('./PersianFiles/persian_tokenized_text.pickle', 'rb')
    persian_tokenized_file = pickle.load(persian_tokenized_file)
    persian_remove_stopwords_file = open('./PersianFiles/persian_without_stopwords.csv', 'a', newline='')
    stop_words = GetStopwords()
    for doc_id in persian_tokenized_file.keys():
        RemoveStopwordDoc(persian_tokenized_file[doc_id], stop_words, persian_remove_stopwords_file)


def PreprocessPersianText(doc):
    clean_text = list(CleanPersionDoc(doc['mediawiki']['page']['revision']['text']['#text']))
    persian_remove_stopwords_file = open('./PersianFiles/persian_without_stopwords.csv', 'a', newline='')
    doc_without_stopwords = RemoveStopwordDoc(clean_text, GetStopwords(), persian_remove_stopwords_file)
    return doc_without_stopwords , clean_text


def PreprocessAllPersianFile():
    all_persion_tokens = Preprocess()
    PlotPersianStopwords(all_persion_tokens)
    RemoveStopwordsAllPersianFile()

