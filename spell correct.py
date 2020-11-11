import math
import pickle
from nltk.probability import FreqDist


def correct_spell_word(incorrect_word, dict_byword):
    main_word = incorrect_word
    size = len(main_word)
    all_word_condid = []
    for i in range(size - 1):
        bigram = main_word[0] + main_word[1]
        if dict_byword.__contains__(bigram):
            temp = dict_byword.get(bigram)
            for x in temp:
                all_word_condid.append(x)
        main_word = main_word[1:]

    fdist = FreqDist(all_word_condid)
    most_common = dict(fdist.most_common(30))

    contain_jacard = {}
    for x in most_common:
        number_bigram = len(x) - 1
        jacard = most_common.get(x) / (number_bigram + size - most_common.get(x))
        contain_jacard.update({x: jacard})
    print("jaccard" + contain_jacard)

    sort_jacard = {k: v for k, v in sorted(contain_jacard.items(), key=lambda item: item[1], reverse=True)}

    def editDistance(str1, str2, m, n):
        if m == 0:
            return n
        if n == 0:
            return m
        if str1[m - 1] == str2[n - 1]:
            return editDistance(str1, str2, m - 1, n - 1)
        return 1 + min(editDistance(str1, str2, m, n - 1),  # Insert
                       editDistance(str1, str2, m - 1, n),  # Remove
                       editDistance(str1, str2, m - 1, n - 1))  # Replace

    min1 = math.inf

    for x in sort_jacard:
        if editDistance(x, incorrect_word, len(x), len(incorrect_word)) < min1:
            min1 = editDistance(x, incorrect_word, len(x), len(incorrect_word))
            print(min1)
            correct_word = x

    return correct_word
