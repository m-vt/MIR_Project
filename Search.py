import math
import numpy as np

positional_index_description_address = "./EnglishFiles/positional_index_description.pickle"
positional_index_title_address = "./EnglishFiles/positional_index_title.pickle"
positional_index_english_address = "./EnglishFiles/positional_index.pickle"
positional_index_persian_address = "./PersianFiles/positional_index.pickle"


def CreateTF_IDFquery(query_terms, total_doc, positional_index):
    # Itc:
    tf_idf_query = []
    for term in positional_index.keys():
        df_term = math.log(total_doc / len(positional_index[term]), 10)
        num_of_term = query_terms.count(term)
        tf_term = 0
        if num_of_term != 0:
            tf_term = 1 + math.log(num_of_term , 10)
        tf_idf_query.append(tf_term * df_term)
    tf_idf_query = np.array(tf_idf_query)
    tf_idf_query = list(tf_idf_query / np.linalg.norm(tf_idf_query))
    return tf_idf_query


def Search(query, docs, positional_index):
    tf_idf_query = np.array(query)
    weights = {}
    for docid in docs:
        temp_list = []
        for term in positional_index.keys():
            count = 0
            for doc_pos in positional_index[term]:
                if docid in doc_pos:
                    count = len(doc_pos[1])
                    break
            if count != 0:
                temp_list.append(1 + math.log(count, 10))
            else:
                temp_list.append(0)
        tf_idf_doc = np.array(temp_list)
        weights[docid] = 0
        if np.linalg.norm(tf_idf_doc) != 0:
            tf_idf_doc = list(tf_idf_doc / np.linalg.norm(tf_idf_doc))
            w_doc_query = np.dot(tf_idf_doc, tf_idf_query)
            weights[docid] = w_doc_query

    return weights


def CalculateOccurences(term1, term2, distance, positional_index):
    matched_doc = set()
    print(term1 , " : " ,positional_index[term1])
    print(term2 , " : " ,positional_index[term2])
    for posting1 in positional_index[term1]:
        for posting2 in positional_index[term2]:
            if posting1[0] == posting2[0]:  # docid are same
                for pos1 in posting1[1]:
                    for pos2 in posting2[1]:
                        if abs(pos1 - pos2) <= distance:
                            matched_doc.add(posting1[0])

    return matched_doc


