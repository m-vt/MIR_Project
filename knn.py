import csv

import scipy.spatial
from collections import Counter
import pandas as pd
import pickle


class KNN:
    def __init__(self, k):
        self.k = k

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def distance(self, X1, X2):
        distance = scipy.spatial.distance.euclidean(X1, X2)

    def predict(self, X_test):
        final_output = []
        for i in range(len(X_test)):
            d = []
            votes = []
            for j in range(len(self.X_train)):
                dist = scipy.spatial.distance.euclidean(self.X_train[j], X_test[i])
                d.append([dist, j])
            d.sort()
            d = d[0:self.k]
            for d, j in d:
                votes.append(self.y_train[j])
            ans = Counter(votes).most_common(1)[0][0]
            final_output.append(ans)

        return final_output

    def score(self, X_test, y_test):
        predictions = self.predict(X_test)
        counter = 0
        for i in range(len(y_test)):
            if predictions[i] == y_test[i]:
                counter += 1

        return counter / len(y_test)


def TrainKnn(k):
    dataset_train = pd.read_csv("./Train/tf_idf.csv")
    X_train = dataset_train.iloc[:, 1:].values

    with open('./Train/label', 'rb') as f:
        y_train = pickle.load(f)
    y_train = [int(x) for x in y_train]

    clf = KNN(k)
    clf.fit(X_train[:2296], y_train[:2296])
    return clf,X_train[2296:],y_train[2296:],X_train[:2296],y_train[:2296]

def PredictTestData(X_test,clf):

    prediction = clf.predict(X_test)

    return prediction



def ClassifyTedTalkKnn(clf):
    dataset_train = pd.read_csv("./EnglishFiles/tf_idf_ted_talks.csv")
    X = dataset_train.iloc[:, 1:].values
    with open('./EnglishFiles/label_ted_talks', 'rb') as f:
        y = pickle.load(f)

    # predict
    prediction = clf.predict(X)

    print("prediction is: \n")
    print(prediction)

    return prediction


def SaveViews(prediction):
    ted_talk = pd.read_csv("./EnglishFiles/TedTalks.csv")
    for i in range(len(ted_talk) - 1):
        ted_talk.at[i, "views"] = prediction[i]
        ted_talk.to_csv("./EnglishFiles/ted_talks.csv", index=False)


def EvaluationKnn(input_class, y_predicted, y_target):
    tp = 0  # ++
    fp = 0  # +-
    fn = 0  # -+
    tn = 0  # --

    for i in range(len(y_predicted)):
        if y_predicted[i] == input_class and y_target[i] == input_class:
            tp += 1
        elif y_predicted[i] == input_class and not y_target[i] == input_class:
            fp += 1
        elif not y_predicted[i] == input_class and y_target[i] == input_class:
            fn += 1
        else:
            tn += 1

    Precision=tp/(tp+fp)
    Recall=tp/(tp+fn)

    print("Accuracy is :", (tp + tn) / (tp + tn + fn + fp))
    print("Recall is :",Recall )
    print("Preⅽision is :", Precision)
    print("F1 is : ", 2*Precision*Recall/(Precision+Recall))



