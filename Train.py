import csv
import math
import pickle

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
from NaiveBayes import TrainNaiveBayes, GetNaiveBayesInfo
from PreprocessAndMakeTfIdf import MainMakeTfIdf


def ReadFile(filename):
    # csv.field_size_limit(sys.maxsize)
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def LoadInfo(filename):
    with open(filename, 'rb') as f:
        info = pickle.load(f)
    return info


def ReadStrToList(linestr):
    linestr = linestr.replace("\'", "")
    linestr = linestr.replace("[", "")
    linestr = linestr.replace("]", "")
    return linestr.split(", ")


def ClassifyTedTalkNaiveBayes():
    preprocessed_ted_data = ReadFile("./EnglishFiles/preprocessed_ted_talk.csv")
    ted_data = ReadFile("./EnglishFiles/TedTalks.csv")
    filename = open("./EnglishFiles/ted_talks.csv", 'w', newline='')
    info = LoadInfo("./Train/NaiveBayesInfo.pickle")
    prob_class_c = info["prob_class_c"]
    prob_class_cbar = info["prob_class_cbar"]
    total_terms = info["total_terms"]
    class_c = info["class_c"]
    class_cbar = info["class_cbar"]
    total_distinct_vocabs = info["total_distinct_vocabs"]
    writer = csv.writer(filename)
    ted_data[0].append("class")
    writer.writerow(ted_data[0])
    for ted_id in range(1, len(preprocessed_ted_data)):
        to_be_c = math.log(prob_class_c)
        to_be_cbar = math.log(prob_class_cbar)
        for term in ReadStrToList(preprocessed_ted_data[ted_id][1]) + ReadStrToList(preprocessed_ted_data[ted_id][14]):
            if term in total_terms.keys():
                to_be_c += math.log((total_terms[term][0] + 1) / (len(class_c) + total_distinct_vocabs))
                to_be_cbar += math.log((total_terms[term][1] + 1) / (len(class_cbar) + total_distinct_vocabs))
            else:
                to_be_c += math.log(1 / (len(class_c) + total_distinct_vocabs))
                to_be_cbar += math.log(1 / (len(class_cbar) + total_distinct_vocabs))
        if to_be_c > to_be_cbar:
            ans = "1"
        else:
            ans = "-1"
        ted_data[ted_id].append(ans)
        writer.writerow(ted_data[ted_id])
        ted_id += 1
    filename.close()


def PreprocessTedTalk():
    list_data = ReadFile("./EnglishFiles/TedTalks.csv")
    filename = open("./EnglishFiles/preprocessed_ted_talk.csv", 'w', newline='')
    writer = csv.writer(filename)
    writer.writerow(list_data[0])
    for ld_id in range(1, len(list_data)):
        list_data[ld_id] = PreprocessDoc(list_data[ld_id])
        writer.writerow(list_data[ld_id])
    filename.close()


def PreprocessDoc(doc):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    doc[1] = tokenizer.tokenize(doc[1])
    doc[14] = tokenizer.tokenize(doc[14])
    doc[1] = [ps.stem(w) for w in doc[1]]
    for w in doc[1][:]:
        if w in stop_words:
            doc[1].remove(w)
    doc[14] = [ps.stem(w) for w in doc[14]]
    for w in doc[14][:]:
        if w in stop_words:
            doc[14].remove(w)
    return doc


MainMakeTfIdf()
TrainNaiveBayes()
GetNaiveBayesInfo()
PreprocessTedTalk()
ClassifyTedTalkNaiveBayes()
