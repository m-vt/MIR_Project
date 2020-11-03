import csv
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


def PreprocessAllEnglishFile():
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    filename = open("./EnglishFiles/ted_talks_with_stopwords.csv", 'w', newline='')
    writer = csv.writer(filename)
    writer.writerow(list_data[0])
    all_english_tokens = []
    for ld in list_data[1:]:
        ld = PreprocessDoc(ld)
        writer.writerow(ld)
        all_english_tokens = all_english_tokens + ld[1] + ld[14]
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


def PreprocessEnglishText():
    all_english_tokens = PreprocessAllEnglishFile()
    stop_words = PlotEnglishStopwords(all_english_tokens)
    RemoveStopwordsAllEnglishFile(stop_words)
