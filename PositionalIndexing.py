import csv
import pickle


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
            term_dict[term_in_doc] = doc_dict[term_in_doc]


def CreatePersianPositionalIndex():
    persian_tokenized_file = open('./PersianFiles/persian_tokenized_text.pickle', 'rb')
    persian_with_stopwords = pickle.load(persian_tokenized_file)
    persian_without_stopwords = ReadFile("./PersianFiles/persian_without_stopwords.csv")
    term_dict = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(len(persian_with_stopwords)):
        SetDocIDAndPositions(term_dict, doc_id + 1, ReadStrToList(persian_without_stopwords[doc_id][0]),
                             persian_with_stopwords[doc_id])
    print("###")
    WriteIndex(term_dict, "./PersianFiles/positional_index.pickle")


def CreateEnglishPositionalIndex():
    list_without_stopwords = ReadFile("./EnglishFiles/ted_talk_without_stopwords.csv")
    list_with_stopwords = ReadFile("./EnglishFiles/ted_talks_with_stopwords.csv")
    term_dict_description = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    term_dict_title = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(1, len(list_with_stopwords)):
        SetDocIDAndPositions(term_dict_description, doc_id, ReadStrToList(list_without_stopwords[doc_id][1]),
                             ReadStrToList(list_with_stopwords[doc_id][1]))
        SetDocIDAndPositions(term_dict_title, doc_id, ReadStrToList(list_without_stopwords[doc_id][14]),
                             ReadStrToList(list_with_stopwords[doc_id][14]))
    WriteIndex(term_dict_description, "./EnglishFiles/positional_index_description.pickle")
    WriteIndex(term_dict_title, "./EnglishFiles/positional_index_title.pickle")


def WriteIndex(term_dict, address):
    with open(address, 'wb') as f:
        pickle.dump(term_dict, f)


def LoadPositionalIndex(filename):
    with open(filename, 'rb') as f:
        positional_index = pickle.load(f)
    return positional_index
