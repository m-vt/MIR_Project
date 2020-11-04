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
    ted_talk_terms = open("./EnglishFiles/ted_talk_terms.csv", 'w', newline='')
    writer = csv.writer(filename)
    writer2 = csv.writer(ted_talk_terms)
    writer.writerow(list_data[0])
    for ld in list_data[1:]:
        ld = PreprocessDoc(ld)
        ld = RemoveStopwordDoc(ld , stop_words)
        doc_terms = ld[1] + ld[14]
        writer.writerow(ld)
        writer2.writerow([doc_terms])
    filename.close()


def Preprocess():
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    filename = open("./EnglishFiles/ted_talks_with_stopwords.csv", 'w', newline='')
    writer = csv.writer(filename)
    writer.writerow(list_data[0])
    all_english_tokens = []
    for ld in list_data[1:]:
        ld = PreprocessDoc(ld)
        writer.writerow(ld)
        all_english_tokens = all_english_tokens + ld[1] + ld[14]
    with open('./EnglishFiles/AllEnglishToken', 'wb') as filehandle:
        # store the data as binary data stream
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


def PreprocessEnglishText(doc  ):
    preprocessed_doc = PreprocessDoc(doc)
    doc_with_stopwords_desription = preprocessed_doc[1][:]
    doc_with_stopwords_title = preprocessed_doc[14][:]
    doc_without_stopwords = RemoveStopwordDoc(preprocessed_doc, GetStopwords() )
    return doc_without_stopwords , doc_with_stopwords_desription , doc_with_stopwords_title



def AddEnglishDoc(doc_without_stopwords):
    filename = open("./EnglishFiles/ted_talk_without_stopwords.csv", 'a', newline='')
    writer = csv.writer(filename)
    writer.writerow(doc_without_stopwords)
    filename.close()
    list_data = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    return len(list_data)


def DeleteEnglishDoc(doc):
    list_data = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    lines = list()
    doc_id = -1
    for ld in range(1, len(list_data)):
        if list_data[ld][7] != doc[7]:
            lines.append(list_data[ld])
        else:
            doc_id = ld
    writeFile = open('./EnglishFiles/new_ted_talks.csv', 'w')
    writer = csv.writer(writeFile)
    writer.writerow(list_data[0])
    writer.writerows(lines)
    return doc_id + 1

