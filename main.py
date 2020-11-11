import operator
import time

from PreprocessEnglishText import PreprocessAllEnglishFile, PreprocessEnglishQuery
from PreprocessPersianText import PreprocessAllPersianFile
from PositionalIndexing import *
from Search import *

positional_index_description_address = "./EnglishFiles/positional_index_description.pickle"
positional_index_title_address = "./EnglishFiles/positional_index_title.pickle"
positional_index_english_address = "./EnglishFiles/positional_index.pickle"
positional_index_persian_address = "./PersianFiles/positional_index.pickle"


def GetNumberOfDocs(filename):
    list_data = ReadFile(filename)
    return len(list_data)


####################### preprocess english :
# PreprocessAllEnglishFile()

####################### positionl index :
# CreateEnglishPositionalIndex()


####################### add doc + positionl index :
# new_english_doc = ['4577',
#                    'Sir Ken Robinson makes an entertaining and profoundly moving case for creating an education system that nurtures (rather than undermines) creativity.',
#                    '1164', 'TED2006', '1140825600', '60', 'Ken Robinson', 'Ken Robinson: Do schools kill creativity?',
#                    '1', '1151367060',
#                    "[{'id': 7, 'name': 'Funny', 'count': 19645}, {'id': 1, 'name': 'Beautiful', 'count': 4573}, {'id': 9, 'name': 'Ingenious', 'count': 6073}, {'id': 3, 'name': 'Courageous', 'count': 3253}, {'id': 11, 'name': 'Longwinded', 'count': 387}, {'id': 2, 'name': 'Confusing', 'count': 242}, {'id': 8, 'name': 'Informative', 'count': 7346}, {'id': 22, 'name': 'Fascinating', 'count': 10581}, {'id': 21, 'name': 'Unconvincing', 'count': 300}, {'id': 24, 'name': 'Persuasive', 'count': 10704}, {'id': 23, 'name': 'Jaw-dropping', 'count': 4439}, {'id': 25, 'name': 'OK', 'count': 1174}, {'id': 26, 'name': 'Obnoxious', 'count': 209}, {'id': 10, 'name': 'Inspiring', 'count': 24924}]",
#                    '[{\'id\': 865, \'hero\': \'https://pe.tedcdn.com/images/ted/172559_800x600.jpg\', \'speaker\': \'Ken Robinson\', \'title\': \'Bring on the learning revolution!\', \'duration\': 1008, \'slug\': \'sir_ken_robinson_bring_on_the_revolution\', \'viewed_count\': 7266103}, {\'id\': 1738, \'hero\': \'https://pe.tedcdn.com/images/ted/de98b161ad1434910ff4b56c89de71af04b8b873_1600x1200.jpg\', \'speaker\': \'Ken Robinson\', \'title\': "How to escape education\'s death valley", \'duration\': 1151, \'slug\': \'ken_robinson_how_to_escape_education_s_death_valley\', \'viewed_count\': 6657572}, {\'id\': 2276, \'hero\': \'https://pe.tedcdn.com/images/ted/3821f3728e0b755c7b9aea2e69cc093eca41abe1_2880x1620.jpg\', \'speaker\': \'Linda Cliatt-Wayman\', \'title\': \'How to fix a broken school? Lead fearlessly, love hard\', \'duration\': 1027, \'slug\': \'linda_cliatt_wayman_how_to_fix_a_broken_school_lead_fearlessly_love_hard\', \'viewed_count\': 1617101}, {\'id\': 892, \'hero\': \'https://pe.tedcdn.com/images/ted/e79958940573cc610ccb583619a54866c41ef303_2880x1620.jpg\', \'speaker\': \'Charles Leadbeater\', \'title\': \'Education innovation in the slums\', \'duration\': 1138, \'slug\': \'charles_leadbeater_on_education\', \'viewed_count\': 772296}, {\'id\': 1232, \'hero\': \'https://pe.tedcdn.com/images/ted/0e3e4e92d5ee8ae0e43962d447d3f790b31099b8_800x600.jpg\', \'speaker\': \'Geoff Mulgan\', \'title\': \'A short intro to the Studio School\', \'duration\': 376, \'slug\': \'geoff_mulgan_a_short_intro_to_the_studio_school\', \'viewed_count\': 667971}, {\'id\': 2616, \'hero\': \'https://pe.tedcdn.com/images/ted/71cde5a6fa6c717488fb55eff9eef939a9241761_2880x1620.jpg\', \'speaker\': \'Kandice Sumner\', \'title\': "How America\'s public schools keep kids in poverty", \'duration\': 830, \'slug\': \'kandice_sumner_how_america_s_public_schools_keep_kids_in_poverty\', \'viewed_count\': 1181333}]',
#                    'Author/educator',
#                    "['children', 'creativity', 'culture', 'dance', 'education', 'parenting', 'teaching']",
#                    'Do schools kill creativity?',
#                    'https://www.ted.com/talks/ken_robinson_says_schools_kill_creativity\n', '47227110']
# AddEnglishDocument(new_english_doc)


####################### delete doc + positionl index :
# deleted_docid = 2
# DeleteEnglishDocument(deleted_docid)


####################### preprocess persian :
# PreprocessAllPersianFile()
#
# ####################### positional index persian :
# CreatePersianPositionalIndex()
#
####################### add to positional + doc :
# new_persion_file = open('./PersianFiles/new_persian_doc.xml')
# doc = xmltodict.parse(new_persion_file.read())
# AddPersianDocument(doc)
#
####################### delete to positional + doc :
# deleted_docid = 1
# DeletePersianDocument(deleted_docid)

####################### English Query
# query = input("query : ")
# # sir is the best and in the world I do love him sir google sir
# query_terms = PreprocessEnglishQuery(query)
# total_number_of_docs = GetNumberOfDocs("./EnglishFiles/ted_talk_without_stopwords.csv")
# positional_index = LoadPositionalIndex(positional_index_english_address)
# tf_idf_query = CreateTF_IDFquery(query_terms, total_number_of_docs, positional_index)
# weights = Search(tf_idf_query, total_number_of_docs, positional_index)
# docids = [str(doc[0]) for doc in sorted(weights.items(), key=operator.itemgetter(1), reverse=True)[:10]]
# list_data = ReadFile("./EnglishFiles/ted_talks.csv")
# for docid in docids:
#     for data in list_data:
#         if data[0] == docid:
#             print(data[0])



# query = input("query : ")
# # مهارت‌های من در مهارت او است و ما با کیفیت تمام این کار را می‌ کنیم
# query_terms , _ = PreprocessPersianText(query)
# total_number_of_docs = GetNumberOfDocs("./PersianFiles/persian_without_stopwords.csv")
# positional_index = LoadPositionalIndex(positional_index_persian_address)
# tf_idf_query = CreateTF_IDFquery(query_terms, total_number_of_docs, positional_index)
# weights = Search(tf_idf_query, total_number_of_docs, positional_index)
# docids = [str(doc[0]) for doc in sorted(weights.items(), key=operator.itemgetter(1), reverse=True)[:10]]
########################### TODO : write results
# list_data = ReadFile("???")
# for docid in docids:
#     for data in list_data:
#         if data[0] == docid:
#             print(data[0])

# make_bigram_index()
