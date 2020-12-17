import csv
import math
import pickle


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


def ClassifyTrainSet(list_data):
    class_c = []
    class_cbar = []
    total_number_cbar = 0
    total_number_c = 0
    for ld_id in range(1, len(list_data)):
        if list_data[ld_id][-1] == "-1":
            for term in ReadStrToList(list_data[ld_id][1]) + ReadStrToList(list_data[ld_id][14]):
                class_cbar.append(term)
            total_number_cbar += 1
        else:
            for term in ReadStrToList(list_data[ld_id][1]) + ReadStrToList(list_data[ld_id][14]):
                class_c.append(term)
            total_number_c += 1
    return class_c, class_cbar, total_number_c, total_number_cbar


def ClassifyTestSet(list_test, prob_class_c, prob_class_cbar, total_terms, class_c, class_cbar, total_distinct_vocabs):
    c_positive = 0
    c_negative = 0
    cbar_positive = 0
    cbar_negative = 0
    for ld_id in range(len(list_test)):
        to_be_c = math.log(prob_class_c)
        to_be_cbar = math.log(prob_class_cbar)
        for term in ReadStrToList(list_test[ld_id][1]) + ReadStrToList(list_test[ld_id][14]):
            if term in total_terms.keys():
                to_be_c += math.log((total_terms[term][0] + 1) / (len(class_c) + total_distinct_vocabs))
                to_be_cbar += math.log((total_terms[term][1] + 1) / (len(class_cbar) + total_distinct_vocabs))
            else:
                to_be_c += math.log(1 / (len(class_c) + total_distinct_vocabs))
                to_be_cbar += math.log(1 / (len(class_cbar) + total_distinct_vocabs))
        if to_be_c > to_be_cbar:
            ans = "1"
        else:
            ans = "-1"

        if ans == list_test[ld_id][-1]:
            if ans == "-1":
                cbar_positive += 1
            else:
                c_positive += 1
        else:  # ans != list_test[ld_id][-1]
            if ans == "-1":  # and list_test[ld_id][-1] == 1
                c_negative += 1
            else:
                cbar_negative += 1
    return c_positive, cbar_positive, c_negative, cbar_negative


def TrainNaiveBayes():
    list_data = ReadFile("./Train/preprocessed_train.csv")
    class_c, class_cbar, Total_Number_C, Total_Number_CBar = ClassifyTrainSet(list_data[:2296])
    prob_class_c = len(class_c) / (len(class_c) + len(class_cbar))
    prob_class_cbar = len(class_cbar) / (len(class_c) + len(class_cbar))
    total_distinct_vocabs = len(set(class_c + class_cbar))
    total_terms = {}
    for term in set(class_c + class_cbar):
        total_in_c = class_c.count(term)
        total_in_c_bar = class_cbar.count(term)
        total_terms[term] = [total_in_c, total_in_c_bar]

    NaiveBayesInfo = {'class_c': class_c,
                      'class_cbar': class_cbar,
                      'prob_class_c': prob_class_c,
                      'prob_class_cbar': prob_class_cbar,
                      'total_distinct_vocabs': total_distinct_vocabs,
                      'total_terms': total_terms
                      }
    WriteInfo(NaiveBayesInfo, "./Train/NaiveBayesInfo.pickle")


def WriteInfo(info, address):
    with open(address, 'wb') as f:
        pickle.dump(info, f)


def LoadInfo(filename):
    with open(filename, 'rb') as f:
        info = pickle.load(f)
    return info


def GetNaiveBayesInfo():
    list_data = ReadFile("./Train/preprocessed_train.csv")
    list_test = list_data[2296:]
    info = LoadInfo("./Train/NaiveBayesInfo.pickle")
    c_positive, cbar_positive, c_negative, cbar_negative = ClassifyTestSet(list_test,
                                                                           info["prob_class_c"],
                                                                           info["prob_class_cbar"],
                                                                           info["total_terms"],
                                                                           info["class_c"],
                                                                           info["class_cbar"],
                                                                           info["total_distinct_vocabs"])
    print("Evaluation Naive Bayes:")
    print("Accuracy = ", (c_positive + cbar_positive) / (c_positive + cbar_positive + c_negative + cbar_negative))
    precision_class_c = c_positive / (c_positive + cbar_negative)
    recall_class_c = c_positive / (c_positive + c_negative)
    print("Precision Class 1 = ", precision_class_c)
    print("Recall Class 1 = ", recall_class_c)
    precision_class_cbar = cbar_positive / (cbar_positive + c_negative)
    recall_class_cbar = cbar_positive / (cbar_positive + cbar_negative)
    print("Precision Class -1 = ", precision_class_cbar)
    print("Recall Class -1 = ", recall_class_cbar)
    print("F1 = ", (2 * precision_class_c * recall_class_c) / (precision_class_c + recall_class_c))
    #print("F1 Class -1 = ", (2 * precision_class_cbar * recall_class_cbar) / (precision_class_cbar + recall_class_cbar))
