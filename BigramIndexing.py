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


def SetDocIDAndPositions(bigram_term_dict, doc_id, index_col, bigram_terms, list_data_with_stopwords):
    list_data_with_stopwords[doc_id][index_col] = ReadStrToList(list_data_with_stopwords[doc_id][index_col])
    for bigram_term in bigram_terms:
        positions = []
        for term2_id in range(len(list_data_with_stopwords[doc_id][index_col]) - 1):
            if list_data_with_stopwords[doc_id][index_col][term2_id] == bigram_term[0] and \
                    list_data_with_stopwords[doc_id][index_col][term2_id + 1] == bigram_term[1]:
                positions.append(term2_id + 1)
        if len(positions) != 0:
            if str(bigram_term) not in bigram_term_dict.keys():
                bigram_term_dict[str(bigram_term)] = [[doc_id, positions]]
            elif [doc_id, positions] not in bigram_term_dict[str(bigram_term)]:
                bigram_term_dict[str(bigram_term)].append([doc_id, positions])


def CreateBigramIndex():
    list_data_with_stopwords = ReadFile("ted_talks_with_stopwords.csv")
    bigram_terms = []
    CreateBigramTerms(1, bigram_terms)
    CreateBigramTerms(14, bigram_terms)
    bigram_term_dict = {}  # term : [[Docid , [Pos1 , ...] ], ... ]
    for doc_id in range(1, len(list_data_with_stopwords)):
        SetDocIDAndPositions(bigram_term_dict, doc_id, 1, bigram_terms, list_data_with_stopwords)
        SetDocIDAndPositions(bigram_term_dict, doc_id, 14, bigram_terms, list_data_with_stopwords)
    return bigram_term_dict
def CreateBigramTerms(index_col, bigram_terms):
    list_data_without_stopwords = ReadFile("ted_talk_without_stopwords.csv")
    for doc_id in range(1, len(list_data_without_stopwords)):
        list_data_without_stopwords[doc_id][index_col] = ReadStrToList(list_data_without_stopwords[doc_id][index_col])
        for i in range(len(list_data_without_stopwords[doc_id][index_col]) - 1):
            bigram_terms.append([list_data_without_stopwords[doc_id][index_col][i],
                                 list_data_without_stopwords[doc_id][index_col][i + 1]])
    return bigram_terms
