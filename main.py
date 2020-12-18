import operator
import time
import os
from pathlib import Path
import nltk


nltk.download('stopwords')
from PreprocessEnglishText import PreprocessAllEnglishFile, PreprocessEnglishQuery
from PreprocessPersianText import PreprocessAllPersianFile
from PositionalIndexing import *
# from BigramIndexing import *
from Search import *
# from SpellCorrect import *

positional_index_english_address = "./EnglishFiles/positional_index.pickle"
positional_index_persian_address = "./PersianFiles/positional_index.pickle"


def GetNumberOfDocs(filename):
    list_data = ReadFile(filename)
    return len(list_data)


# ####################### preprocess english :
# PreprocessAllEnglishFile()
#
# ####################### positionl index :
# print("English Positional Index:")
# CreateEnglishPositionalIndex()
# make_bigram_index_English()
#
# ####################### preprocess persian :
# PreprocessAllPersianFile()
#
# # ####################### positional index persian :
# print("Persian Positional Index:")
# CreatePersianPositionalIndex()
# make_bigram_index_Persion()


def printCommands():
    print("Commands:\n")
    print("- add english document")
    print("- delete english document")
    print("- add persian document")
    print("- delete persian document")
    print("- english query")
    print("- persian query")
    print("- get english word bigram")
    print("- get persian word bigram")
    print("- get distance of two words")
    print("- get english word posting")
    print("- get persian word posting")
    print("- commands")
    print("- quit")


def AddEnglishDoc(path):
    list_data = ReadFile(path)
    new_english_doc = list_data[1]
    all_token_English = AddEnglishDocument(new_english_doc)
    add_new_doc_bigram_English(all_token_English)


def DeleteEnglishDoc(deleted_docid):
    all_token_English = DeleteEnglishDocument(deleted_docid)
    if all_token_English != "NO DOC_ID MATCHED!":
        delete_new_doc_bigram_English(all_token_English)


def AddPersianDoc(path):
    new_persion_file = open(path)
    doc = xmltodict.parse(new_persion_file.read())
    all_persion_token = AddPersianDocument(doc)
    add_new_doc_bigram_persion(all_persion_token)


def DeletePersianDoc(deleted_docid):
    all_persion_token = DeletePersianDocument(deleted_docid)
    if all_persion_token != "NO DOC_ID MATCHED!":
        add_new_doc_bigram_persion(all_persion_token)


def EnglishSearch(query, selected_class):
    # sir is the best and in the world I do love him sir google sir
    query_terms = PreprocessEnglishQuery(query)
    total_number_of_docs = GetNumberOfDocs("./EnglishFiles/ted_talks.csv")
    total_docs = [i for i in range(1, total_number_of_docs + 1)]
    positional_index = LoadPositionalIndex(positional_index_english_address)
    tf_idf_query = CreateTF_IDFquery(query_terms, total_number_of_docs, positional_index)
    weights = Search(tf_idf_query, total_docs, positional_index)
    docids = [str(doc[0]) for doc in sorted(weights.items(), key=operator.itemgetter(1), reverse=True)[:10]]
    list_data = ReadFile("./EnglishFiles/ted_talks.csv")
    print("\nRESULT\n:")
    for docid in docids:
        for data in list_data:
            # TODO
            if data[0] == docid and data[-1] == selected_class:
                print("name: ", data[8])
                print("title: ", data[15])
                print("description: ", data[2])
                print("#################################")


def PersianSearch(query):
    # # مهارت‌های من در مهارت او است و ما با کیفیت تمام این کار را می‌ کنیم
    query_terms, _ = PreprocessPersianText(query)
    total_number_of_docs = GetNumberOfDocs("./PersianFiles/PersianTexts.csv")
    total_docs = [i for i in range(1, total_number_of_docs + 1)]
    positional_index = LoadPositionalIndex(positional_index_persian_address)
    tf_idf_query = CreateTF_IDFquery(query_terms, total_number_of_docs, positional_index)
    weights = Search(tf_idf_query, total_docs, positional_index)
    docids = [str(doc[0]) for doc in sorted(weights.items(), key=operator.itemgetter(1), reverse=True)[:10]]
    list_data = ReadFile("./PersianFiles/PersianTexts.csv")
    for docid in docids:
        for data in list_data:
            if data[0] == docid:
                print("title: ", data[1])
                print("id: ", data[2])
                print("text: ", data[3])
                print("#################################")


def GetPostingEnglish(term):
    positional_index_english = LoadPositionalIndex(positional_index_english_address)
    if term in positional_index_english.keys():
        print(positional_index_english[term])
        return positional_index_english[term]
    return "Term Is Not In Posting!"


def GetPostingPersian(term):
    positional_index_persian = LoadPositionalIndex(positional_index_persian_address)
    if term in positional_index_persian.keys():
        print(positional_index_persian[term])
        return positional_index_persian[term]
    return "Term Is Not In Posting!"


def spell_check_english(query):
    a = getQueryAndReturnCorrectEnglish(query)
    flag = True
    for key in a[0]:
        if len(a[0][key]) > 1:
            flag = False
            print("change the word \"", key, "\" to one of this words and try again:")
            for k in range(len(a[0][key])):
                print(k + 1, "- ", a[0][key][k])
    return flag


def spell_check_persian(query):
    a = getQueryAndReturnCorrectPersion(query)
    flag = True
    for key in a:
        if len(a[key]) > 1:
            flag = False
            print("change the word \"", key, "\" to one of this words and try again:")
            for k in range(len(a[key])):
                print(k + 1, "- ", a[key][k])
    return flag

# print("size of english file before compressing: ")
# print(os.stat('./EnglishFiles/positional_index.pickle').st_size)
# print("size of english file after compressing vb code: ")
# print(os.stat('./EnglishFiles/positional_vbcode.pickle').st_size)
# print("size of english file after compressing gamma code: ")
# print(os.stat('./EnglishFiles/positional_gamma.pickle').st_size)
#
# print("size of persian file before compressing: ")
# print(os.stat('./PersianFiles/positional_index.pickle').st_size)
# print("size of persian file after compressing: ")
# print(os.stat('./PersianFiles/positional_vbcode.pickle').st_size)
# print("size of persian file after compressing gamma code: ")
# print(os.stat('./PersianFiles/positional_gamma.pickle').st_size)
#
# printCommands()
#
# while (True):
#     command = input()
#     if command == "add english document":
#         print("enter file address for ex: ./EnglishFiles/new_doc.csv")
#         temp_path = input()
#         if os.path.isfile(temp_path):
#             AddEnglishDoc(temp_path)
#             print("file added")
#         else:
#             print("path is invalid")
#     elif command == "delete english document":
#         print("enter doc id:")
#         temp_id = input()
#         DeleteEnglishDoc(int(temp_id))
#         print("done!")
#     elif command=="add persian document":
#         print("enter file address for ex: ./PersianFiles/new_persian_doc.xml")
#         temp_path= input()
#         if os.path.isfile(temp_path):
#             AddPersianDoc(temp_path)
#             print("file added")
#         else:
#             print("path is invalid")
#     elif command=="delete persian document":
#         print("enter doc id:")
#         temp_id = input()
#         DeletePersianDoc(int(temp_id))
#         print("done!")
#     elif command=="english query":
#         print("enter the query ex: sir is the best")
#         quey=input()
#         if spell_check_english(quey):
#             EnglishSearch(quey)
#         else:
#             print("enter edited query: ")
#             quey = input()
#             EnglishSearch(quey)
## TODO : ask user to select a specific class
#
#     elif command=="persian query":
#         print("enter the query ex: مهارت‌های من در مهارت او است")
#         quey=input()
#
#         if spell_check_persian(quey):
#             PersianSearch(quey)
#         else:
#             print("enter edited  query: ")
#             quey = input()
#             PersianSearch(quey)
#
#     elif command=="get english word bigram":
#         print("enter bigram. ex: si")
#         word=input()
#         print(showWordOfbigramEnglish(word))
#     elif command == "get persian word bigram":
#         print("enter bigram. ex: مه")
#         word = input()
#         print(showWordOfbigramPersion(word))
#     elif command=="get distance of two words":
#         print("enter words ex: monday sunday")
#         wrd=input()
#         temp=wrd.split(" ")
#         print(editDistance(temp[0],temp[1], len(temp[0]), len(temp[1])))
#
#     elif command =="get english word posting":
#         print("enter word. ex: sir")
#         wrd = input()
#         GetPostingEnglish(wrd)
#     elif command == "get persian word posting":
#         print("enter word. ex: مهارت")
#         wrd = input()
#         GetPostingPersian(wrd)
#     elif command == "quit":
#         break
#     elif command=="commands":
#         printCommands()
#     else:
#         print("Command is invalid. try again")
