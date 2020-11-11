import csv
import pickle

from PreprocessEnglishText import  PreprocessEnglishText, AddEnglishDoc, DeleteEnglishDoc
from PreprocessPersianText import  PreprocessPersianText, AddPersianDoc, DeletePersianDoc


positional_index_description_address = "./EnglishFiles/positional_index_description.pickle"
positional_index_title_address = "./EnglishFiles/positional_index_title.pickle"
positional_index_persian_address = "./PersianFiles/positional_index.pickle"


def ReadFile(filename):
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def ReadStrToList(linestr):
    linestr = linestr.replace("\'", "")
    linestr = linestr.replace("[", "")
    linestr = linestr.replace("]", "")
    return linestr.split(", ")


def SetDocIDAndPositions(term_dict, doc_id, list_without_stopwords, list_with_stopwords):
    doc_dict = {}
    for term1_id in range(len(list_without_stopwords)):
        positions = []
        if list_without_stopwords[term1_id] not in doc_dict.keys():
            for term2_id in range(len(list_with_stopwords)):
                if list_without_stopwords[term1_id] == list_with_stopwords[term2_id]:
                    positions.append(term2_id + 1)
            doc_dict[list_without_stopwords[term1_id]] = [doc_id, positions]
    for term_in_doc in doc_dict.keys():
        if term_in_doc in term_dict.keys():
            term_dict[term_in_doc].append(doc_dict[term_in_doc])
        else:
            term_dict[term_in_doc] = [doc_dict[term_in_doc]]


def CreatePersianPositionalIndex():
    persian_tokenized_file = open('./PersianFiles/persian_tokenized_text.pickle', 'rb')
    persian_with_stopwords = pickle.load(persian_tokenized_file)
    persian_without_stopwords = ReadFile("./PersianFiles/persian_without_stopwords.csv")
    term_dict = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(len(persian_with_stopwords)):
        SetDocIDAndPositions(term_dict, doc_id + 1, ReadStrToList(persian_without_stopwords[doc_id][1]),
                             persian_with_stopwords[doc_id])
    WriteIndex(term_dict, "./PersianFiles/positional_index.pickle")


def CreateEnglishPositionalIndex():
    list_without_stopwords = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    list_with_stopwords = ReadFile("./EnglishFiles/ted_talks_with_stopwords.csv")
    term_dict_description = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    term_dict_title = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(1, len(list_with_stopwords)):
        SetDocIDAndPositions(term_dict_description, doc_id, ReadStrToList(list_without_stopwords[doc_id][2]),
                             ReadStrToList(list_with_stopwords[doc_id][2]))
        SetDocIDAndPositions(term_dict_title, doc_id, ReadStrToList(list_without_stopwords[doc_id][15]),
                             ReadStrToList(list_with_stopwords[doc_id][15]))
    WriteIndex(term_dict_description, "./EnglishFiles/positional_index_description.pickle")
    WriteIndex(term_dict_title, "./EnglishFiles/positional_index_title.pickle")


def WriteIndex(term_dict, address):
    with open(address, 'wb') as f:
        pickle.dump(term_dict, f)


def LoadPositionalIndex(filename):
    with open(filename, 'rb') as f:
        positional_index = pickle.load(f)
    return positional_index


def AddPositionalIndexForNewDoc(term_dict, doc_id, list_without_stopwords, list_with_stopwords, address):
    SetDocIDAndPositions(term_dict, doc_id, list_without_stopwords, list_with_stopwords)
    WriteIndex(term_dict, address)


def DeletePositionalIndexForNewDoc(term_dict, doc_id, list_without_stopwords, address):
    list_without_stopwords = ReadStrToList(list_without_stopwords)
    for term in list_without_stopwords:
        if term in term_dict.keys():
            for doc_index in term_dict[term]:
                if doc_index[0] == doc_id:
                    term_dict[term].remove(doc_index)
            if not term_dict[term]:
                del term_dict[term]
    WriteIndex(term_dict, address)


def AddPersianDocument(doc):
    doc_without_stopwords, doc_with_stopwords = PreprocessPersianText(
        doc['mediawiki']['page']['revision']['text']['#text'])
    doc_id = AddPersianDoc(doc_without_stopwords)
    term_dict = LoadPositionalIndex(positional_index_persian_address)
    AddPositionalIndexForNewDoc(term_dict, doc_id, doc_without_stopwords, doc_with_stopwords,
                                positional_index_persian_address)


def AddEnglishDocument(doc):
    doc_without_stopwords, doc_with_stopwords_desp, doc_with_stopwords_title = PreprocessEnglishText(doc)
    doc_id = AddEnglishDoc(doc_without_stopwords)
    term_dict = LoadPositionalIndex(positional_index_description_address)
    AddPositionalIndexForNewDoc(term_dict, doc_id, doc_without_stopwords[2], doc_with_stopwords_desp,
                                positional_index_description_address)
    term_dict = LoadPositionalIndex(positional_index_title_address)
    AddPositionalIndexForNewDoc(term_dict, doc_id, doc_without_stopwords[15], doc_with_stopwords_title,
                                positional_index_title_address)


def DeleteEnglishDocument(doc_id):
    doc = DeleteEnglishDoc(doc_id)
    if doc != "NO DOC_ID MATCHED!":
        positional_index_description = LoadPositionalIndex(positional_index_description_address)
        positional_index_title = LoadPositionalIndex(positional_index_title_address)
        DeletePositionalIndexForNewDoc(positional_index_description, doc_id, doc[2],
                                       positional_index_description_address)
        DeletePositionalIndexForNewDoc(positional_index_title, doc_id, doc[15], positional_index_title_address)
    else:
        print(doc)


def DeletePersianDocument(doc_id):
    doc = DeletePersianDoc(doc_id)
    if doc != "NO DOC_ID MATCHED!":
        positional_index_persian = LoadPositionalIndex(positional_index_persian_address)
        DeletePositionalIndexForNewDoc(positional_index_persian, doc_id, doc[1], positional_index_persian_address)
    else:
        print(doc)
