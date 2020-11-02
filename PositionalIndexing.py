import csv


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

def SetDocIDAndPositions(term_dict, doc_id, index_col, list_data_without_stopwords, list_data_with_stopwords):
    list_data_without_stopwords[doc_id][index_col] = ReadStrToList(list_data_without_stopwords[doc_id][index_col])
    list_data_with_stopwords[doc_id][index_col] = ReadStrToList(list_data_with_stopwords[doc_id][index_col])
    for term1_id in range(len(list_data_without_stopwords[doc_id][index_col])):
        positions = []
        for term2_id in range(len(list_data_with_stopwords[doc_id][index_col])):
            if list_data_with_stopwords[doc_id][index_col][term2_id] == list_data_without_stopwords[doc_id][index_col][term1_id]:
                positions.append(term2_id + 1)
        print(list_data_without_stopwords[doc_id][index_col][term1_id] , positions)
        if list_data_without_stopwords[doc_id][index_col][term1_id] not in term_dict.keys():
            term_dict[list_data_without_stopwords[doc_id][index_col][term1_id]] = [[doc_id, positions]]
        elif [doc_id, positions] not in term_dict[list_data_without_stopwords[doc_id][index_col][term1_id]]:
            term_dict[list_data_without_stopwords[doc_id][index_col][term1_id]].append([doc_id, positions])


def CreatePositionalIndex():
    list_data_without_stopwords = ReadFile("ted_talk_without_stopwords.csv")
    list_data_with_stopwords = ReadFile("ted_talks_with_stopwords.csv")
    term_dict = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(1, len(list_data_with_stopwords)):
        SetDocIDAndPositions(term_dict, doc_id, 1, list_data_without_stopwords, list_data_with_stopwords)
        SetDocIDAndPositions(term_dict, doc_id, 14, list_data_without_stopwords, list_data_with_stopwords)
    print(term_dict)
