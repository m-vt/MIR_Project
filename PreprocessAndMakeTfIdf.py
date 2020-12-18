import copy
import csv
import math
import nltk
from nltk.stem import PorterStemmer
import pickle
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))


def ReadFile(filename):
    # csv.field_size_limit(sys.maxsize)
    filename = open(filename, 'r', newline='')
    list_data = list(csv.reader(filename))
    filename.close()
    return list_data


def PreprocessAndMakeDictionaryWithDfOfWord(list_data):
    filename = open("./Train/preprocessed_train.csv", 'w', newline='')
    writer = csv.writer(filename)
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
        writer.writerow(list_data[ld_id])
    filename.close()
    dict_all_word_with_df = nltk.FreqDist(all_word)
    return dict_all_word_with_df, preprocess_description_and_title, label


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


def SaveLabel(label, file_for_save_lable):
    with open(file_for_save_lable, 'wb') as filehandle:
        pickle.dump(label, filehandle)


def MakeTfIdf(idf_list, preprocess_description_and_title, file_for_save_tf_idf):
    with open(file_for_save_tf_idf, mode='w') as tf_idf_file:
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


def MainMakeTfIdf(train_data, test_data, file_for_save_tf_idf, file_for_save_lable):
    train_data = ReadFile(train_data)
    test_data = ReadFile(test_data)
    total_data = train_data + test_data[1:]
    dict_with_df, preprocess_description_and_title, label = PreprocessAndMakeDictionaryWithDfOfWord(total_data)
    SaveLabel(label, file_for_save_lable)
    dict_with_idf = MakeIdf(dict_with_df, len(total_data))
    MakeTfIdf(dict_with_idf, preprocess_description_and_title, file_for_save_tf_idf)


MainMakeTfIdf("./Train/train.csv", "./Test/test.csv", "./Train/tf_idf.csv", './Train/label')
