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
    doc = xmltodict.parse(persionfile.read())
    print(len(doc['mediawiki']['page']))
    clean_texts = []
    for i in range(len(doc['mediawiki']['page'])):
        clean_text = clean_Persion_doc(doc['mediawiki']['page'][0]['revision']['text']['#text'])
        ################
        if i == 5:
            break
        ################
        clean_texts.append(clean_text)
    print(clean_texts)

##############################

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
