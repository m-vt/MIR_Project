import csv
import string
import nltk
from hazm import *
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
import matplotlib.pyplot as plt
from PreprocessEnglishText import PlotStopwords, RemoveStopwordsAllEnglishFile, PreprocessAllEnglishFile
from PositionalIndexing import CreatePositionalIndex, WriteFile, LoadFile
# from BigramIndexing import CreateBigramIndex
from BigramIndexing import make_bigram_index
import xmltodict


# nltk.download('punkt')


def ReadFile(filename):
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def PreprocessEnglishText():
    list_data = ReadFile("ted_talks.csv")
    all_english_tokens = PreprocessAllEnglishFile(list_data, "ted_talks_with_stopwords.csv")
    stop_words = PlotStopwords(all_english_tokens)
    list_data = ReadFile("ted_talks.csv")
    RemoveStopwordsAllEnglishFile(stop_words, list_data, "ted_talk_without_stopwords.csv")
#
#
# def clean_Persion_doc(doc):
#     stemmer = Stemmer()
#     lemmatizer = Lemmatizer()
#     normalizer = Normalizer()
#     doc = normalizer.normalize(doc)
#     tokenized = word_tokenize(doc)
#     stemmed = [stemmer.stem(w) for w in tokenized]
#     new_words = [word for word in stemmed if word.isalnum()]
#     lemmatized = [lemmatizer.lemmatize(w) for w in new_words]
#     return lemmatized
#
#
# All_persion_text = []
# with open('Persian.xml') as persionfile:
#     with open('persian_tokenized_text.csv', 'a', newline='') as fd1:
#         with open('persian_text.csv', 'a', newline='') as fd2:
#             writer1 = csv.writer(fd1)
#             writer2 = csv.writer(fd2)
#             doc = xmltodict.parse(persionfile.read())
#             writer1.writerow(["text"])
#             for i in range(len(doc['mediawiki']['page'])):
#                 ################
#                 # if i == 5:
#                 #     break
#                 ################
#                 clean_text = [list(clean_Persion_doc(doc['mediawiki']['page'][i]['revision']['text']['#text']))]
#                 text = [(doc['mediawiki']['page'][i]['revision']['text']['#text'])]
#                 All_persion_text = All_persion_text + clean_text[0]
#                 print(type(clean_text))
#                 writer1.writerow(clean_text)
#                 writer2.writerow(text)
#
# # ################################################################## find stopword
# fdist = FreqDist(All_persion_text)
# most_common = fdist.most_common(40)
# stopwords_persion = []
# for w in most_common:
#     stopwords_persion.append(w[0])
# fdist.plot(30, cumulative=False)
# plt.show()
# print(most_common)
# f = open("stopwords_persion.txt", "a")
# f.write(str(stopwords_persion))
# f.close()

# #####################################################################
#
PreprocessEnglishText()
CreatePositionalIndex()

LoadFile("positional_index.pickle")
make_bigram_index()


