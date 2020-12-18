import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle


def read_train_and_test_data(tf_idf_file, lable):
    dataset_train = pd.read_csv(tf_idf_file)
    X = dataset_train.iloc[:, 1:].values

    with open(lable, 'rb') as f:
        y = pickle.load(f)
    y = [int(x) for x in y]

    X_train = X[:2296]
    y_train = y[:2296]
    X_test = X[2296:]
    y_test = y[2296:]
    return X_train, y_train, X_test, y_test


def predicted(X_train, y_train, X_test):
    # sc = StandardScaler()
    # X_train = sc.fit_transform(X_train)
    # y_train = sc.transform(y_train)
    regressor = RandomForestRegressor(n_estimators=1, random_state=10)
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    return y_pred


def show_report_for_part_one(y_pred, y_test):
    print(accuracy_score(y_test, y_pred.round(), normalize=False))
    print(classification_report(y_test, y_pred.round()))


def save_predict_views_in_ted_talk_csv(file, predicted_list):
    ted_talk = pd.read_csv(file)
    for i in range(len(ted_talk) - 1):
        ted_talk.at[i, "views"] = predicted_list[i]
        ted_talk.to_csv("./EnglishFiles/classify_with_random_forest.csv", index=False)


def train_random_forest_for_test(tf_idf_file, lable):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list = predicted(X_train, y_train, X_test)
    show_report_for_part_one(predicted_list, y_test)


def train_random_forest_for_classify_ted_talk(tf_idf_file, lable):
    X_train, y_train, X_test, y_test = read_train_and_test_data(tf_idf_file, lable)
    predicted_list = predicted(X_train, y_train, X_test)
    save_predict_views_in_ted_talk_csv("./EnglishFiles/TedTalks.csv", predicted_list)
