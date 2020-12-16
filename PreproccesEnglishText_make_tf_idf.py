import copy
import csv
import math

import nltk
from nltk.stem import PorterStemmer
import pickle
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


# nltk.download('punkt')

def ReadFile(filename):
    #csv.field_size_limit(sys.maxsize)
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data



def Preprocess_And_Make_Dictionary_Whit_Df_Of_Word(list_data):
    filename = open("./EnglishFiles/ted_talks_without_stopwords.csv", 'w', newline='')
    writer = csv.writer(filename)
    list_data[0].insert(0, "docid")
    writer.writerow(list_data[0])
    preprocess_description_and_title = []
    all_word = []
    label = []
    for ld_id in range(1, len(list_data)):
        list_data[ld_id] = PreprocessDoc(list_data[ld_id])
        temp = list_data[ld_id][1] + list_data[ld_id][14]
        preprocess_description_and_title.append(temp)
        temp = set(temp)
        all_word = all_word + list(temp)
        label.append(list_data[ld_id][16])
        list_data[ld_id].insert(0, ld_id)
        writer.writerow(list_data[ld_id])
    filename.close()
    dict_all_word_with_df = nltk.FreqDist(all_word)
    return dict_all_word_with_df, preprocess_description_and_title,label

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


def MakeIdf(dict_df, number_of_doc):
    for x in dict_df.keys():
        dict_df[x] = math.log(number_of_doc / dict_df[x])
    return dict_df


def saveLabel(label):
    with open('./EnglishFiles/label', 'wb') as filehandle:
        pickle.dump(label, filehandle)



def MakeTfIdf(idf_list, preprocess_description_and_title):
    with open('./EnglishFiles/tf_idf.csv', mode='w') as tf_idf_file:
        tf_idf_writer = csv.writer(tf_idf_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        tf_idf_writer.writerow(list(idf_list.keys()))
        for doc_word in preprocess_description_and_title:
            dict_tf_doc = nltk.FreqDist(doc_word)
            tf_idf = copy.deepcopy(idf_list)
            for x in tf_idf.keys():
                if x in dict_tf_doc.keys():
                    tf_idf[x] = tf_idf[x] * dict_tf_doc[x]
                else:
                    tf_idf[x] = 0
            tf_idf_writer.writerow(tf_idf.values())


def main_MakeTfIdf():
    train_data = ReadFile("train.csv")
    test_data = ReadFile("test.csv")
    total_data = train_data + test_data[1:]
    dict_whit_df, preprocess_description_and_title, lable = Preprocess_And_Make_Dictionary_Whit_Df_Of_Word(total_data)
    saveLabel(lable)
    dict_whit_idf = MakeIdf(dict_whit_df, len(total_data))
    MakeTfIdf(dict_whit_idf, preprocess_description_and_title)

main_MakeTfIdf()



########### TODO : make diffrence in Preprocess All EnglishFile
# def PreprocessAllEnglishFile():
#     all_english_tokens = Preprocess()
#     stop_words = PlotEnglishStopwords(all_english_tokens)
#     RemoveStopwordsAllEnglishFile(stop_words)
#     AddDocidToTed()

########### TODO : make diffrence in Preprocess All EnglishFile PreprocessEnglishDoc()
# def PreprocessEnglishDoc(doc):
#     preprocessed_doc = PreprocessDoc(doc)
#     doc_with_stopwords_desription = preprocessed_doc[1][:]
#     doc_with_stopwords_title = preprocessed_doc[14][:]
#     doc_without_stopwords = RemoveStopwordDoc(preprocessed_doc, GetStopwords())
#     return doc_without_stopwords, doc_with_stopwords_desription, doc_with_stopwords_title


def AddEnglishDoc(doc):
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    doc_id = len(list_data)
    filename = open("./EnglishFiles/ted_talks.csv", 'a', newline='')
    writer = csv.writer(filename)
    doc.insert(0, doc_id)
    writer.writerow(doc)
    filename.close()
    return doc_id


def DeleteEnglishDoc(doc_id):
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    lines = list()
    doc = "NO DOC_ID MATCHED!"
    for ld in range(1, len(list_data)):
        if list_data[ld][0] != str(doc_id):
            lines.append(list_data[ld])
        else:
            doc = list_data[ld]
    writeFile = open("./EnglishFiles/ted_talks.csv", 'w')
    writer = csv.writer(writeFile)
    writer.writerow(list_data[0])
    writer.writerows(lines)
    return doc

########### TODO
# def PreprocessEnglishQuery(query):
#     preprocessed_query = PreprocessQuery(query)
#     query_without_stopwords = RemoveStopwordQuery(preprocessed_query, GetStopwords())
#     return query_without_stopwords

####### I change it
def PreprocessQuery(query):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()
    query = tokenizer.tokenize(query)
    query = [ps.stem(w) for w in query]
    for w in query[:]:
        if w in stop_words:
            query.remove(w)
    return query


# def RemoveStopwordQuery(query, stop_words):
#     for w in query:
#         if w in stop_words:
#             query.remove(w)
#     return query


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


# def RemoveStopwordsAllEnglishFile(stop_words):
#     list_data = ReadFile("./EnglishFiles/ted_talks.csv")
#     filename = open("./EnglishFiles/ted_talk_without_stopwords.csv", 'w', newline='')
#     writer = csv.writer(filename)
#     list_data[0].insert(0, "docid")
#     writer.writerow(list_data[0])
#     for ld_id in range(1, len(list_data)):
#         list_data[ld_id] = PreprocessDoc(list_data[ld_id])
#         list_data[ld_id] = RemoveStopwordDoc(list_data[ld_id], stop_words)
#         list_data[ld_id].insert(0, ld_id)
#         writer.writerow(list_data[ld_id])
#     filename.close()



# def PlotEnglishStopwords(all_english_tokens):
#     fdist = FreqDist(all_english_tokens)
#     most_common = fdist.most_common(30)
#     stop_words = []
#     for w in most_common:
#         stop_words.append(w[0])
#     fdist.plot(30, cumulative=False)
#     plt.show()
#     f = open("./EnglishFiles/stopwords_english.txt", "a")
#     f.write(str(stop_words))
#     f.close()
#     return stop_words


# def RemoveStopwordDoc(doc, stop_words):
#     for w in doc[1][:]:
#         if w in stop_words:
#             doc[1].remove(w)
#     for w in doc[14][:]:
#         if w in stop_words:
#             doc[14].remove(w)
#     return doc


# def GetStopwords():
#     f = open("./EnglishFiles/stopwords_english.txt", "r")
#     stop_words = f.read()
#     stop_words = stop_words.replace('\'', '')
#     stop_words = stop_words.replace('[', '')
#     stop_words = stop_words.replace(']', '')
#     stop_words = stop_words.replace(' ', '')
#     stop_words = stop_words.split(",")
#     return stop_words






