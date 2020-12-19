import pickle
import pandas as pd
import numpy
from sklearn import svm, metrics


def read_train_and_test_data(tf_idf_file, lable):
    dataset_train = pd.read_csv(tf_idf_file)
    X = dataset_train.iloc[:, 1:].values
    with open(lable, 'rb') as f:
        y = pickle.load(f)
    y = [int(x) for x in y]
    X_train = X[:2295]
    y_train = y[:2295]
    X_test = X[2295:]
    y_test = y[2295:]
    return X_train, y_train, X_test, y_test


def predicted(x_train, y_train, x_test, c):
    classifier = svm.SVC(C=c, kernel='rbf', cache_size=8000, probability=False)
    classifier.fit(x_train, y_train)
    predicted_list = classifier.predict(x_test)
    return predicted_list, classifier


def show_report_for_part_one(y_test, predicted_list, classifier):
    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(y_test, predicted_list)))


def save_predict_views_in_ted_talk_csv(file, predicted_list):
    ted_talk = pd.read_csv(file)
    for i in range(len(ted_talk)-1):
        ted_talk.at[i, "views"] = predicted_list[i]
        ted_talk.to_csv("./EnglishFiles/ted_talks.csv", index=False)


def train_svm_for_test(tf_idf_file, lable,c):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list, classifier = predicted(X_train, y_train, X_test,c)
    show_report_for_part_one(y_test, predicted_list, classifier)


def train_svm_for_classify_ted_talk(tf_idf_file, lable, c):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list, classifier = predicted(X_train, y_train, X_test, c)
    save_predict_views_in_ted_talk_csv("./EnglishFiles/TedTalks.csv", predicted_list)
