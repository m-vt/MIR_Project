import pickle
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


def CleanPersianDoc(doc):
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
    all_persion_tokens = []
    persion_file = open('./PersianFiles/Persian.xml')
    doc = xmltodict.parse(persion_file.read())
    persian_tokenized_text = {}  # docid : []
    for i in range(len(doc['mediawiki']['page'])):
        clean_text = list(CleanPersianDoc(doc['mediawiki']['page'][i]['revision']['text']['#text']))
        all_persion_tokens = all_persion_tokens + clean_text
        persian_tokenized_text[i] = clean_text
    with open('./PersianFiles/AllPersionToken', 'wb') as filehandle:
        pickle.dump(all_persion_tokens, filehandle)
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


def RemoveStopwordDoc(doc, stop_words):
    for token in doc:
        if token in stop_words:
            doc.remove(token)
    return doc


def RemoveStopwordsAllPersianFile():
    persian_tokenized_file = open('./PersianFiles/persian_tokenized_text.pickle', 'rb')
    persian_tokenized_file = pickle.load(persian_tokenized_file)
    persian_remove_stopwords_file = open('./PersianFiles/persian_without_stopwords.csv', 'w', newline='')
    writer1 = csv.writer(persian_remove_stopwords_file)
    stop_words = GetStopwords()
    for doc_id in persian_tokenized_file.keys():
        doc_without_stopwords = RemoveStopwordDoc(persian_tokenized_file[doc_id], stop_words, )
        writer1.writerow([doc_id + 1, list(doc_without_stopwords)])


def PreprocessPersianText(doc):
    clean_text = list(CleanPersianDoc(doc))
    doc_with_stopwords = clean_text.copy()
    doc_without_stopwords = RemoveStopwordDoc(clean_text, GetStopwords())
    return doc_without_stopwords, doc_with_stopwords


def AddPersianDoc(doc_without_stopwords):
    list_data = ReadFile("./PersianFiles/persian_without_stopwords.csv")
    doc_id = len(list_data) + 1
    persian_remove_stopwords_file = open('./PersianFiles/persian_without_stopwords.csv', 'a', newline='')
    writer1 = csv.writer(persian_remove_stopwords_file)
    writer1.writerow([doc_id, list(doc_without_stopwords)])
    return doc_id


def DeletePersianDoc(doc_id):
    list_data = ReadFile("./PersianFiles/persian_without_stopwords.csv")
    lines = list()
    doc = "NO DOC_ID MATCHED!"
    for ld in range(len(list_data)):
        if list_data[ld][0] != str(doc_id):
            lines.append(list_data[ld])
        else:
            doc = list_data[ld]
    writeFile = open("./PersianFiles/persian_without_stopwords.csv", 'w')
    writer = csv.writer(writeFile)
    writer.writerow(list_data[0])
    writer.writerows(lines)
    return doc


def PreprocessAllPersianFile():
    all_persion_tokens = Preprocess()
    PlotPersianStopwords(all_persion_tokens)
    RemoveStopwordsAllPersianFile()

