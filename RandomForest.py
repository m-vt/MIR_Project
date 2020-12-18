import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
import pickle


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


def predicted(X_train, y_train, X_test):
    classifier = RandomForestClassifier(n_estimators=100, random_state=10)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    return y_pred


def show_report_for_part_one(y_pred, y_test):
    print(accuracy_score(y_test, y_pred, normalize=False))
    print(classification_report(y_test, y_pred))


def save_predict_views_in_ted_talk_csv(file, predicted_list):
    ted_talk = pd.read_csv(file)
    for i in range(len(ted_talk) - 1):
        ted_talk.at[i, "views"] = predicted_list[i]
        ted_talk.to_csv("./EnglishFiles/ted_talks.csv", index=False)


def train_random_forest_for_test(tf_idf_file, lable):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list = predicted(X_train, y_train, X_test)
    show_report_for_part_one(predicted_list, y_test)


def train_random_forest_for_classify_ted_talk(tf_idf_file, lable):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list = predicted(X_train, y_train, X_test)
    save_predict_views_in_ted_talk_csv("./EnglishFiles/TedTalks.csv", predicted_list)
