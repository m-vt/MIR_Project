import csv
import math
import pickle
from typing import Final

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

import Svm,RandomForest

stop_words = set(stopwords.words('english'))
from NaiveBayes import TrainNaiveBayes, GetNaiveBayesInfo, ClassifyTedTalkNaiveBayes
from PreprocessAndMakeTfIdf import MainMakeTfIdf



###################### preprocess   ############################
# MainMakeTfIdf("./Train/train.csv", "./Test/test.csv", "./Train/tf_idf.csv", './Train/label',"./Train/preprocessed_train.csv")
# MainMakeTfIdf("./Train/train.csv", "./EnglishFiles/TedTalks.csv", "./EnglishFiles/tf_idf_ted_talks.csv",
#               './EnglishFiles/label_ted_talks','./EnglishFiles/preprocessed_ted_talk.csv')

###################### naive bayes  ###################
# TrainNaiveBayes()
GetNaiveBayesInfo()
# ClassifyTedTalkNaiveBayes()
###################### svm and randomForest  ###################
# c: Final = 1
# Svm.train_svm_for_test("./Train/tf_idf.csv", './Train/label',c)
# Svm.train_svm_for_classify_ted_talk("./EnglishFiles/tf_idf_ted_talks.csv", './EnglishFiles/label_ted_talks', c)
#
# RandomForest.train_random_forest_for_test("./Train/tf_idf.csv", './Train/label')
# RandomForest.train_random_forest_for_classify_ted_talk("./EnglishFiles/tf_idf_ted_talks.csv", './EnglishFiles/label_ted_talks')

