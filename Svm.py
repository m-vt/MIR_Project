import pickle

import pandas as pd
from sklearn import svm, metrics


dataset_train = pd.read_csv("tf_idf.csv")
X_train = dataset_train.iloc[:, 1:].values

with open('label', 'rb') as f:
    y_train = pickle.load(f)

y_train = [int(x) for x in y_train]

classifier = svm.SVC(C=2, kernel='linear', cache_size=8000, probability=False)
classifier.fit(X_train[:2296], y_train[:2296])
predicted = classifier.predict(X_train[2296:])


print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(y_train[2296:], predicted)))
