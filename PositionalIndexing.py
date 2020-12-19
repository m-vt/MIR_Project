import csv
import pickle
import sys

from PreprocessEnglishText import PreprocessEnglishDoc, AddEnglishDoc, DeleteEnglishDoc
from PreprocessPersianText import PreprocessPersianText, AddPersianDoc, DeletePersianDoc
from vbcode import encode
from gammaCode import encode_Gamma

positional_index_english_address = "./EnglishFiles/positional_index.pickle"
positional_english_vcode_address = "./EnglishFiles/positional_vbcode.pickle"
positional_english_gamma_address = "./EnglishFiles/positional_gamma.pickle"
positional_index_persian_address = "./PersianFiles/positional_index.pickle"
positional_persian_vcode_address = "./PersianFiles/positional_vbcode.pickle"
positional_persian_gamma_address = "./PersianFiles/positional_gamma.pickle"

def ReadFile(filename):
    # csv.field_size_limit(sys.maxsize)
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


def EncodePositionalIndex(term_dict, type):
    compressed_positional = {}
    compressed_amount = 0
    for term in term_dict:
        compressed_positional[term] = {}
        for docid in term_dict[term]:
            if type == "gamma":
                positions = encode_Gamma(docid[1])
            else:
                positions = encode(docid[1])
            compressed_amount += sys.getsizeof(docid[1]) - sys.getsizeof(positions)
            compressed_positional[term].update({docid[0]: positions})
    print("reduction of size after compress by" , type , ":" , compressed_amount)
    return compressed_positional


def CreatePersianPositionalIndex():
    persian_tokenized_file = open('./PersianFiles/persian_tokenized_text.pickle', 'rb')
    persian_with_stopwords = pickle.load(persian_tokenized_file)
    persian_without_stopwords = ReadFile("./PersianFiles/persian_without_stopwords.csv")
    term_dict = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(len(persian_with_stopwords)):
        SetDocIDAndPositions(term_dict, doc_id + 1, ReadStrToList(persian_without_stopwords[doc_id][1]),
                             persian_with_stopwords[doc_id])
    compressed_positional_gamma = EncodePositionalIndex(term_dict, "gamma")
    WriteIndex(term_dict, "./PersianFiles/positional_index.pickle")
    compressed_positional_vbcode = EncodePositionalIndex(term_dict, "vbcode")
    WriteIndex(compressed_positional_vbcode, positional_persian_vcode_address)
    WriteIndex(compressed_positional_gamma, positional_persian_gamma_address)


def CreateEnglishPositionalIndex():
    list_without_stopwords = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    list_with_stopwords = ReadFile("./EnglishFiles/ted_talks_with_stopwords.csv")
    term_dict_total = {}
    for doc_id in range(1, len(list_with_stopwords)):
        total_list_without_stopword = ReadStrToList(list_without_stopwords[doc_id][2]) + ReadStrToList(
            list_without_stopwords[doc_id][15])
        total_list_with_stopword = ReadStrToList(list_with_stopwords[doc_id][2]) + ReadStrToList(
            list_with_stopwords[doc_id][15])
        SetDocIDAndPositions(term_dict_total, doc_id, total_list_without_stopword,
                             total_list_with_stopword)
    compressed_positional_gamma = EncodePositionalIndex(term_dict_total, "gamma")
    compressed_positional_vbcode = EncodePositionalIndex(term_dict_total, "vbcode")
    WriteIndex(term_dict_total, positional_index_english_address)
    # WriteIndex(compressed_positional_vbcode, positional_english_vcode_address)
    # WriteIndex(compressed_positional_gamma, positional_english_gamma_address)
    return term_dict_total


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
    for term in list_without_stopwords:
        if term in term_dict.keys():
            for doc_index in term_dict[term]:
                if doc_index[0] == doc_id:
                    term_dict[term].remove(doc_index)
            if not term_dict[term]:
                del term_dict[term]
    WriteIndex(term_dict, address)


def AddPersianDocument(doc):
    details = [doc['mediawiki']['page']['title'], doc['mediawiki']['page']['id'],
               doc['mediawiki']['page']['revision']['text']['#text']]
    doc_id = AddPersianDoc(details)
    doc_without_stopwords, doc_with_stopwords = PreprocessPersianText(
        doc['mediawiki']['page']['revision']['text']['#text'])
    term_dict = LoadPositionalIndex(positional_index_persian_address)
    AddPositionalIndexForNewDoc(term_dict, doc_id, doc_without_stopwords, doc_with_stopwords,
                                positional_index_persian_address)
    return doc_without_stopwords


def AddEnglishDocument(doc):
    new_doc = doc.copy()
    doc_without_stopwords, doc_with_stopwords_desp, doc_with_stopwords_title = PreprocessEnglishDoc(doc)
    doc_with_stopwords = doc_with_stopwords_desp + doc_with_stopwords_title
    doc_without_stopwords_all = doc_without_stopwords[1] + doc_without_stopwords[14]
    doc_id = AddEnglishDoc(new_doc)
    term_dict = LoadPositionalIndex(positional_index_english_address)
    AddPositionalIndexForNewDoc(term_dict, doc_id, doc_without_stopwords_all, doc_with_stopwords,
                                positional_index_english_address)
    return doc_without_stopwords_all


def DeleteEnglishDocument(doc_id):
    doc = DeleteEnglishDoc(doc_id)
    if doc != "NO DOC_ID MATCHED!":
        doc, _, _ = PreprocessEnglishDoc(doc[1:])
        positional_index_english = LoadPositionalIndex(positional_index_english_address)
        all_tokens = doc[1] + doc[14]
        DeletePositionalIndexForNewDoc(positional_index_english, doc_id, all_tokens, positional_index_english_address)
    else:
        print(doc)
        return doc
    return doc[1] + doc[14]


def DeletePersianDocument(doc_id):
    doc = DeletePersianDoc(doc_id)
    if doc != "NO DOC_ID MATCHED!":
        doc_without_stopwords, _ = PreprocessPersianText(doc[3])
        positional_index_persian = LoadPositionalIndex(positional_index_persian_address)
        DeletePositionalIndexForNewDoc(positional_index_persian, doc_id, doc_without_stopwords,
                                       positional_index_persian_address)
    else:
        print(doc)
        return doc
    return doc_without_stopwords

