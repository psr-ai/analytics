import os

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'list_of_english_words.txt')) as word_file:
    english_words = set(word.strip().lower() for word in word_file)


def is_english_word(word):
    return word.lower() in english_words