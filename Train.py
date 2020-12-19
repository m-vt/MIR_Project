import csv
import math
import pickle
#from typing import Final
from typing import Final

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import RandomForest
import Svm
import knn
#import Svm,RandomForest

stop_words = set(stopwords.words('english'))
#from NaiveBayes import TrainNaiveBayes, GetNaiveBayesInfo, ClassifyTedTalkNaiveBayes
from PreprocessAndMakeTfIdf import MainMakeTfIdf



###################### preprocess   ############################
# MainMakeTfIdf("./Train/train.csv", "./Test/test.csv", "./Train/tf_idf.csv", './Train/label',"./Train/preprocessed_train.csv")
# MainMakeTfIdf("./Train/train.csv", "./EnglishFiles/TedTalks.csv", "./EnglishFiles/tf_idf_ted_talks.csv",
#               './EnglishFiles/label_ted_talks','./EnglishFiles/preprocessed_ted_talk.csv')

###################### naive bayes  ###################
# TrainNaiveBayes()
#GetNaiveBayesInfo()
# ClassifyTedTalkNaiveBayes()
###################### svm and randomForest  ###################
# c: Final = 1
# Svm.train_svm_for_test("./Train/tf_idf.csv", './Train/label',c)
# Svm.train_svm_for_classify_ted_talk("./EnglishFiles/tf_idf_ted_talks.csv", './EnglishFiles/label_ted_talks', c)
#
RandomForest.train_random_forest_for_test("./Train/tf_idf.csv", './Train/label')
RandomForest.train_random_forest_for_classify_ted_talk("./EnglishFiles/tf_idf_ted_talks.csv", './EnglishFiles/label_ted_talks')
######################## knn ######################

# k=input("k :")
# clf,x_test,y_target,x_train,y_train=knn.TrainKnn(int(k))
# y_test_predicted= knn.PredictTestData(x_test,clf)
# y_train_predicted= knn.PredictTestData(x_train,clf)
# print("for test data:")
# knn.EvaluationKnn(1,y_test_predicted,y_target)
# print("for train data:")
# knn.EvaluationKnn(1,y_train_predicted,y_train)
# predicted= knn.ClassifyTedTalkKnn(clf)
# knn.SaveViews(predicted)
