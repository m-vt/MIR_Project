import csv
from hazm import *
from nltk import word_tokenize
# nltk.download('punkt')
import xmltodict


def clean_Persion_doc(doc):
    normalizer = Normalizer()
    doc = normalizer.normalize(doc)
    tokenized = word_tokenize(doc)
    return tokenized


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

##################

Englishfile = open('ted_talks.csv', 'r', newline='')
list_data = list(csv.reader(Englishfile))
Englishfile.close()

Englishfile = open('ted_talks_modified.csv', 'w', newline='')
writer = csv.writer(Englishfile)
writer.writerow(list_data[0])
for ld in list_data[1:]:
    ld[1] = str(word_tokenize(ld[1]))
    ld[14] = str(word_tokenize(ld[14]))
    writer.writerow(ld)
Englishfile.close()
