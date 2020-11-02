import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt


# nltk.download('punkt')


def RemoveStopwordsAllEnglishFile(stop_words, list_data, filename):
    filename = open(filename, 'w', newline='')
    writer = csv.writer(filename)
    writer.writerow(list_data[0])
    for ld in list_data[1:]:
        ld = PreprocessLine(ld)
        ld = RemoveStopwordLine(ld , stop_words)
        writer.writerow(ld)
    filename.close()


def PreprocessAllEnglishFile(list_data, filename):
    filename = open(filename, 'w', newline='')
    writer = csv.writer(filename)
    writer.writerow(list_data[0])
    all_english_tokens = []
    for ld in list_data[1:]:
        ld = PreprocessLine(ld)
        writer.writerow(ld)
        all_english_tokens = all_english_tokens + ld[1] + ld[14]
    filename.close()
    return all_english_tokens


def PlotStopwords(all_english_tokens):
    fdist = FreqDist(all_english_tokens)
    most_common = fdist.most_common(30)
    stop_words = []
    for w in most_common:
        stop_words.append(w[0])
    fdist.plot(30, cumulative=False)
    plt.show()
    return stop_words


def PreprocessLine(line):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    line[1] = tokenizer.tokenize(line[1])
    line[14] = tokenizer.tokenize(line[14])
    line[1] = [ps.stem(w) for w in line[1]]
    line[14] = [ps.stem(w) for w in line[14]]
    return line


def RemoveStopwordLine(line, stop_words):
    for w in line[1][:]:
        if w in stop_words:
            line[1].remove(w)
    for w in line[14][:]:
        if w in stop_words:
            line[14].remove(w)
    return line
