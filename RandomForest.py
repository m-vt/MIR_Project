import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pickle

dataset_train = pd.read_csv("tf_idf.csv")
X_train = dataset_train.iloc[:, 1:].values

with open('label', 'rb') as f:
    y_train = pickle.load(f)
y_train = [int(x) for x in y_train]

sc = StandardScaler()
X_train[255:] = sc.fit_transform(X_train[255:])
X_train[:255] = sc.transform(X_train[:255])

regressor = RandomForestRegressor(n_estimators=1, random_state=10)
regressor.fit(X_train[:2296], y_train[:2296])
y_pred = regressor.predict(X_train[2296:])

print(accuracy_score(y_train[2296:], y_pred.round(), normalize=False))
print(classification_report(y_train[2296:], y_pred.round()))
