import csv
import json

import pickle

dict_persion = {"": {}}
dict_English = {"": {}}


def make_bigram_index_English():
    global dict_English
    with open('./EnglishFiles/AllEnglishToken', 'rb') as fp:
        item_list_english = pickle.load(fp)
    item_list_english = list(item_list_english)
    for i in range(len(item_list_english)):
        bigram_one_word(item_list_english[i], dict_English)
        if i == 100:
            break
    with open('./EnglishFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_English, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(dict_English)


def make_bigram_index_Persion():
    global dict_persion
    with open('./PersianFiles/AllPersionToken', 'rb') as fp:
        item_list_persion = pickle.load(fp)
    item_list_persion = list(item_list_persion)
    for i in range(len(item_list_persion)):
        bigram_one_word(item_list_persion[i], dict_persion)
        # if i == 1000:
        #     break
    with open('./PersianFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_persion, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print(dict_persion)


def add_new_doc_bigram_English(list_of_new_token):
    with open('./EnglishFiles/bigram.pickle', 'rb') as handle:
        dict_English = pickle.load(handle)
    for i in range(len(list_of_new_token)):
        bigram_one_word(list_of_new_token[i], dict_English)
    with open('./EnglishFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_English, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return dict_English


def delete_new_doc_bigram_English(list_of_new_token):
    global dict_English
    with open('./EnglishFiles/bigram.pickle', 'rb') as handle:
        dict_English = pickle.load(handle)
    for i in range(len(list_of_new_token)):
        delete_bigram_oneWord(list_of_new_token[i], dict_English)
    with open('./EnglishFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_English, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return dict_English


def add_new_doc_bigram_persion(list_of_new_token):
    with open('./PersianFiles/bigram.pickle', 'rb') as handle:
        dict_persion = pickle.load(handle)
    for i in range(len(list_of_new_token)):
        bigram_one_word(list_of_new_token[i], dict_persion)
    with open('./PersianFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_persion, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return dict_persion


def delete_new_doc_bigram_persion(list_of_new_token):
    with open('./PersianFiles/bigram.pickle', 'rb') as handle:
        dict_persion = pickle.load(handle)
    for i in range(len(list_of_new_token)):
        delete_bigram_oneWord(list_of_new_token[i], dict_persion)
    with open('./PersianFiles/bigram.pickle', 'wb') as handle:
        pickle.dump(dict_persion, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return dict_persion


def bigram_one_word(test_str, dict):
    main_word = test_str
    size = len(test_str)
    for i in range(size - 1):
        bigram = test_str[0] + test_str[1]
        if dict.__contains__(bigram):
            if dict.get(bigram).__contains__(main_word):
                count_word = dict.get(bigram).get(main_word)
                dict.get(bigram).update({main_word: count_word + 1})
            else:
                dict.get(bigram).update({main_word: 1})

        else:
            dict.update({bigram: {main_word: 1}})
        test_str = test_str[1:]


def delete_bigram_oneWord(word, dict):
    main_word = word
    size = len(word)
    for i in range(size - 1):
        bigram = word[0] + word[1]
        if dict.__contains__(bigram):
            if dict.get(bigram).__contains__(main_word):
                word_count = dict.get(bigram).get(main_word)
                dict.get(bigram).update({main_word:word_count-1})
            if dict.get(bigram).get(main_word) == 0:
                dict.get(bigram).pop(main_word)
            if len(dict.get(bigram)) == 0:
                dict.pop(bigram)
        word = word[1:]



make_bigram_index_English()
make_bigram_index_Persion()
# list = ['sir']
# list1 = ['زیزی']
#
# print(add_new_doc_bigram_English(list))
# print(delete_new_doc_bigram_English(list))
# print(delete_new_doc_bigram_English(list))
# list=['crisi']
# print(delete_new_doc_bigram_English(list))
# list=['design']
# print(delete_new_doc_bigram_English(list))
# print(add_new_doc_bigram_persion(list1))
# print(delete_new_doc_bigram_persion(list1))
