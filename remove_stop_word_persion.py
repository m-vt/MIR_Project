import sys
import csv

csv.field_size_limit(sys.maxsize)
count = 0
token_list = []
f = open("stopwords_persion.txt", "r")
stop_words = f.read()
stop_words = stop_words.replace('\'', '')
stop_words = stop_words.replace('[', '')
stop_words = stop_words.replace(']', '')
stop_words = stop_words.replace(' ', '')
stop_words = stop_words.split(",")
print(stop_words)
count = 0
with open('persian_tokenized_text.csv', newline='') as csvfile:
    with open('persian_remove_stop_word.csv', 'a', newline='') as fd1:
        writer1 = csv.writer(fd1)
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            a = ''.join(row)
            a = a.replace('\'', '')
            a = a.replace('\"', '')
            a = a.replace(']', '')
            a = a.replace('[', '')
            c = a.split(',')
            print(c)
            if count == 100:
                break;
            for w in c:
                if w in stop_words:
                    c.remove(w)
            print(type(c))
            count = count + 1
            writer1.writerow(list(c))
