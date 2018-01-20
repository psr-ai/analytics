from math import log
import os
from DataCleaning.dictionary.dict import is_english_word
import re
# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'words-by-frequency-pasted.co.txt')).read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)


def camel(s):
    return (s != s.lower() and s != s.upper())


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""
    suggested_words = []

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s.lower()[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    # if not camel(s) or len(camel_case_split(s)) == 1:
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    out = reversed(out)
    for word in out:
        if not is_english_word(word):
            return [s]
        else:
            suggested_words.append(word)

    # return " ".join(reversed(out))
    return suggested_words

    # else:
    #     camel_case_splitted_words = camel_case_split(s)
    #
    #     for camel_case_splitted_word in camel_case_splitted_words:
    #         if is_english_word(camel_case_splitted_word) or camel_case_splitted_word.upper() == camel_case_splitted_word:
    #             suggested_words.append(camel_case_splitted_word)
    #         else:
    #             more_words = infer_spaces(camel_case_splitted_word)
    #             for word in more_words:
    #                 suggested_words.append(word)
    #
    #     return suggested_words

# print(infer_spaces('iphone7'))