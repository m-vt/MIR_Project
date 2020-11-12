import csv
import pickle

import nltk
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt


# nltk.download('punkt')

def ReadFile(filename):
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def RemoveStopwordsAllEnglishFile(stop_words):
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    filename = open("./EnglishFiles/ted_talk_without_stopwords.csv", 'w', newline='')
    writer = csv.writer(filename)
    list_data[0].insert(0, "docid")
    writer.writerow(list_data[0])
    for ld_id in range(1, len(list_data)):
        list_data[ld_id] = PreprocessDoc(list_data[ld_id])
        list_data[ld_id] = RemoveStopwordDoc(list_data[ld_id], stop_words)
        list_data[ld_id].insert(0, ld_id)
        writer.writerow(list_data[ld_id])
    filename.close()


def Preprocess():
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    filename = open("./EnglishFiles/ted_talks_with_stopwords.csv", 'w', newline='')
    writer = csv.writer(filename)
    list_data[0].insert(0, "docid")
    writer.writerow(list_data[0])
    all_english_tokens = []
    for ld_id in range(1, len(list_data)):
        list_data[ld_id] = PreprocessDoc(list_data[ld_id])
        all_english_tokens = all_english_tokens + list_data[ld_id][1] + list_data[ld_id][14]
        list_data[ld_id].insert(0, ld_id)
        writer.writerow(list_data[ld_id])
    with open('./EnglishFiles/AllEnglishToken', 'wb') as filehandle:
        pickle.dump(all_english_tokens, filehandle)
    filename.close()
    return all_english_tokens


def PlotEnglishStopwords(all_english_tokens):
    fdist = FreqDist(all_english_tokens)
    most_common = fdist.most_common(30)
    stop_words = []
    for w in most_common:
        stop_words.append(w[0])
    fdist.plot(30, cumulative=False)
    plt.show()
    f = open("./EnglishFiles/stopwords_english.txt", "a")
    f.write(str(stop_words))
    f.close()
    return stop_words


def PreprocessDoc(doc):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    doc[1] = tokenizer.tokenize(doc[1])
    doc[14] = tokenizer.tokenize(doc[14])
    doc[1] = [ps.stem(w) for w in doc[1]]
    doc[14] = [ps.stem(w) for w in doc[14]]
    return doc


def RemoveStopwordDoc(doc, stop_words):
    for w in doc[1][:]:
        if w in stop_words:
            doc[1].remove(w)
    for w in doc[14][:]:
        if w in stop_words:
            doc[14].remove(w)
    return doc


def GetStopwords():
    f = open("./EnglishFiles/stopwords_english.txt", "r")
    stop_words = f.read()
    stop_words = stop_words.replace('\'', '')
    stop_words = stop_words.replace('[', '')
    stop_words = stop_words.replace(']', '')
    stop_words = stop_words.replace(' ', '')
    stop_words = stop_words.split(",")
    return stop_words


def PreprocessAllEnglishFile():
    all_english_tokens = Preprocess()
    stop_words = PlotEnglishStopwords(all_english_tokens)
    RemoveStopwordsAllEnglishFile(stop_words)
    AddDocidToTed()


def PreprocessEnglishDoc(doc):
    preprocessed_doc = PreprocessDoc(doc)
    doc_with_stopwords_desription = preprocessed_doc[1][:]
    doc_with_stopwords_title = preprocessed_doc[14][:]
    doc_without_stopwords = RemoveStopwordDoc(preprocessed_doc, GetStopwords())
    return doc_without_stopwords, doc_with_stopwords_desription, doc_with_stopwords_title


def AddEnglishDoc(doc_without_stopwords):
    list_data = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    doc_id = len(list_data)
    filename = open("./EnglishFiles/ted_talk_without_stopwords.csv", 'a', newline='')
    writer = csv.writer(filename)
    doc_without_stopwords.insert(0, doc_id)
    writer.writerow(doc_without_stopwords)
    filename.close()
    return doc_id


def DeleteEnglishDoc(doc_id):
    list_data = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    lines = list()
    doc = "NO DOC_ID MATCHED!"
    for ld in range(1, len(list_data)):
        if list_data[ld][0] != str(doc_id):
            lines.append(list_data[ld])
        else:
            doc = list_data[ld]
    writeFile = open("./EnglishFiles/ted_talk_without_stopwords.csv", 'w')
    writer = csv.writer(writeFile)
    writer.writerow(list_data[0])
    writer.writerows(lines)
    return doc


def PreprocessEnglishQuery(query):
    preprocessed_query = PreprocessQuery(query)
    query_without_stopwords = RemoveStopwordQuery(preprocessed_query, GetStopwords())
    return query_without_stopwords


def PreprocessQuery(query):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    query = tokenizer.tokenize(query)
    query = [ps.stem(w) for w in query]
    return query


def RemoveStopwordQuery(query, stop_words):
    for w in query:
        if w in stop_words:
            query.remove(w)
    return query


def AddDocidToTed():
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    ted_talk = open("./EnglishFiles/ted_talks.csv", 'w', newline='')
    writer = csv.writer(ted_talk)
    list_data[0].insert(0, "docid")
    writer.writerow(list_data[0])
    for ld_id in range(1, len(list_data)):
        list_data[ld_id].insert(0, ld_id)
        writer.writerow(list_data[ld_id])
    ted_talk.close()
