import math
import pickle
from nltk.probability import FreqDist

import math
import pickle

import nltk
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer
from PositionalIndexing import *

from PreprocessPersianText import *


text_file = open('./EnglishFiles/stopwords_english.txt', "r")
stop_words = text_file.read()
stop_words = stop_words.replace('\'', '')
stop_words = stop_words.replace('[', '')
stop_words = stop_words.replace(']', '')
stop_words = stop_words.replace(' ', '')
stop_words = stop_words.split(",")

# print(stop_words[1])
# print(stop_words)
# print(type(stop_words))

text_file1 = open('./PersianFiles/stopwords_persion.txt',"r")
stop_words_persion = text_file1.read()
stop_words_persion = text_file.read()
stop_words_persion = stop_words_persion.replace('\'', '')
stop_words_persion = stop_words_persion.replace('[', '')
stop_words_persion = stop_words_persion.replace(']', '')
stop_words_persion = stop_words_persion.replace(' ', '')
stop_words_persion = stop_words_persion.split(",")



def getQueryAndReturnCorrectEnglish(Query):
    global stop_words_English
    correct_query = {}
    correct_query_string = ""
    mistake_query_string = ""
    with open('./EnglishFiles/bigram.pickle', 'rb') as handle:
        dict_English = pickle.load(handle)
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    query = tokenizer.tokenize(Query)
    query = [ps.stem(w) for w in query]
    for w in query[:]:
        if w not in stop_words :
            correct_query.update({w:correct_spell_word(w, dict_English)})
        else:
            correct_query.update({w:[w]})
    # for w in query:
    #     mistake_query_string = mistake_query_string + w + " "
    # for w in correct_query:
    #     correct_query_string = correct_query_string + w + " "
    return correct_query,mistake_query_string


def getQueryAndReturnCorrectPersion(query):
    correct_query = {}
    correct_query_string = ""
    mistake_query_string = ""
    # print(",,,,,",query)
    query1, query = PreprocessPersianText(query)
    # print(query)
    with open('./PersianFiles/bigram.pickle', 'rb') as handle:
        dict_Persion = pickle.load(handle)
        for w in query[:]:
            if w not in stop_words:
                correct_query.update({w: correct_spell_word(w, dict_Persion)})
            else:
                correct_query.update({w: [w]})

    return correct_query



def correct_spell_word(incorrect_word, dict_byword):
    main_word = incorrect_word
    size = len(main_word)
    all_word_condid = []
    for i in range(size - 1):
        bigram = main_word[0] + main_word[1]
        if dict_byword.__contains__(bigram):
            temp = dict_byword.get(bigram)
            for x in temp:
                all_word_condid.append(x)
        main_word = main_word[1:]

    fdist = FreqDist(all_word_condid)
    most_common = dict(fdist.most_common(30))

    contain_jacard = {}
    for x in most_common:
        number_bigram = len(x) - 1
        jacard = most_common.get(x) / (number_bigram + size - most_common.get(x))
        contain_jacard.update({x: jacard})

    sort_jacard = {k: v for k, v in sorted(contain_jacard.items(), key=lambda item: item[1], reverse=True)}

    # print("jaccard : ",incorrect_word,sort_jacard)

    min1 = math.inf
    editDistanceDict = {}
    correct_word = ""
    for x in sort_jacard:
        ED = editDistance(x, incorrect_word, len(x), len(incorrect_word))
        editDistanceDict.update({x: ED})

    editDistanceDict_sort = {k: v for k, v in sorted(editDistanceDict.items(), key=lambda item: item[1])}
    minval = min(editDistanceDict_sort.values())
    correct_words = [k for k, v in editDistanceDict_sort.items() if v == minval]


    return correct_words


def editDistance(str1, str2, m, n):
    if m == 0:
        return n
    if n == 0:
        return m
    if str1[m - 1] == str2[n - 1]:
        return editDistance(str1, str2, m - 1, n - 1)
    return 1 + min(editDistance(str1, str2, m, n - 1),  # Insert
                   editDistance(str1, str2, m - 1, n),  # Remove
                   editDistance(str1, str2, m - 1, n - 1))  # Replace




