import csv
import string
import nltk
from hazm import *
from nltk import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')
import xmltodict


def clean_Persion_doc(doc):
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    normalizer = Normalizer()

    doc = normalizer.normalize(doc)
    tokenized=word_tokenize(doc)
    stemmed=[stemmer.stem(w) for w in tokenized]
    new_words = [word for word in stemmed if word.isalnum()]
    lemmatized=[lemmatizer.lemmatize(w) for w in new_words]

    return lemmatized


with open('Persian.xml') as persionfile:
    with open('persian_tokenized_text.csv', 'a', newline='') as fd1:
        with open('persian_text.csv', 'a', newline='') as fd2:
            writer1 = csv.writer(fd1)
            writer2 = csv.writer(fd2)
            doc = xmltodict.parse(persionfile.read())
            writer1.writerow(["text"])
            for i in range(len(doc['mediawiki']['page'])):
                ################
                if i == 5:
                    break
                ################
                clean_text = [list(clean_Persion_doc(doc['mediawiki']['page'][i]['revision']['text']['#text']))]
                text = [(doc['mediawiki']['page'][i]['revision']['text']['#text'])]
                writer1.writerow(clean_text)
                writer2.writerow(text)


#################

Englishfile = open('ted_talks.csv', 'r', newline='')
list_data = list(csv.reader(Englishfile))
Englishfile.close()

Englishfile = open('ted_talks_modified.csv', 'w', newline='')
writer = csv.writer(Englishfile)
writer.writerow(list_data[0])
counter=0
for ld in list_data[1:]:
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    ps = PorterStemmer()

    ld[1] = tokenizer.tokenize(ld[1])
    ld[14]= tokenizer.tokenize(ld[14])
    #stem

    ld[1]=[ps.stem(w) for w in ld[1]]
    ld[14]=[ps.stem(w) for w in ld[14]]

    writer.writerow(ld)


    counter+=1
    if counter==5:
        break
Englishfile.close()
