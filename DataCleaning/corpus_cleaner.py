import DataCleaning.dictionary.dict as dictionary
from DataCleaning.config import continuous_characters_config, contractions, expressions_to_remove, emoticons
from DataCleaning.SpellChecker.spell_checker import correction as spelling_corrector
from DataCleaning.predict_word_split.predict_word_split import infer_spaces
from DataCleaning.POSTagger import tagger
from html.parser import HTMLParser
import nltk.data
import sys
import re
from nltk.corpus import stopwords

english_stops = set(stopwords.words('english'))
html_parser = HTMLParser()
punctuation_list = ['?', '.', ',', '!', ';', ':']


# def predict_word_splits(word):
#     longest_word = ""
#     suggestion_words = []
#     current_word = ""
#     remaining_word_chunk = word
#     while len(remaining_word_chunk)>0:
#         for char in remaining_word_chunk:
#             current_word = current_word + char
#             if dictionary.is_english_word(current_word):
#                 longest_word = current_word
#         if longest_word != "":
#             suggestion_words.append(longest_word)
#             current_word = ""
#             remaining_word_chunk = remaining_word_chunk[len(longest_word):]
#         else:
#             break
#     return suggestion_words


def continuous_character_counts(word):
    print(len(word))
    last_character = ""
    continuous_character_count = 0
    continuous_characters = []
    for index, char in enumerate(word):
        if index > 0:
            continuous_character_count += 1
            if char != last_character:
                character_meta = {}
                character_meta['character'] = last_character
                character_meta['count'] = continuous_character_count
                character_meta['index'] = index
                continuous_characters.append(character_meta)
                continuous_character_count = 0
            elif index == len(word) - 1:
                if char != last_character:
                    character_meta = {}
                    character_meta['character'] = char
                    character_meta['count'] = 1
                    character_meta['index'] = index + 1
                    continuous_characters.append(character_meta)
                else:
                    continuous_character_count += 1
                    character_meta = {}
                    character_meta['character'] = char
                    character_meta['count'] = continuous_character_count
                    character_meta['index'] = index + 1
                    continuous_characters.append(character_meta)
        last_character = char

    print(continuous_characters)


def delete_continuous_characters(word, deleting_frequency):
    last_character = ""
    continuous_character_count = 0
    continuous_characters = []
    for index, char in enumerate(word):
        if index > 0:
            continuous_character_count += 1
            if char != last_character:
                character_meta = {}
                character_meta['character'] = last_character
                character_meta['count'] = continuous_character_count
                character_meta['index'] = index
                continuous_characters.append(character_meta)
                continuous_character_count = 0
            elif index == len(word) - 1:
                if char != last_character:
                    character_meta = {}
                    character_meta['character'] = char
                    character_meta['count'] = 1
                    character_meta['index'] = index + 1
                    continuous_characters.append(character_meta)
                else:
                    continuous_character_count += 1
                    character_meta = {}
                    character_meta['character'] = char
                    character_meta['count'] = continuous_character_count
                    character_meta['index'] = index + 1
                    continuous_characters.append(character_meta)
        last_character = char
    suggested_word = word
    for index_main, character_meta in enumerate(continuous_characters):
        if character_meta['count'] >= deleting_frequency:
            removed_characters_count = 0
            for index in range(character_meta['count'] - 1):
                suggested_word = suggested_word[:character_meta['index']-1] + suggested_word[character_meta['index']:]
                character_meta['index'] -= 1
                removed_characters_count += 1
            for index, subsequent_character_meta in enumerate(continuous_characters):
                if index > index_main:
                    subsequent_character_meta['index'] = subsequent_character_meta['index'] - removed_characters_count

    return suggested_word


def escape_html_characters(text):
    return html_parser.unescape(text)


def tokenize_corpus(corpus):
    return re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s|\r\n|\n", corpus)


def tokenize_sentence(sentence):
    return re.findall(r"[\w']+|[.,!?:;]+", sentence)

# def remove_unnecessary_punctuations(word):
#     return re.sub(r'[^\w\?!\.,;"]', "", word)


def is_url(text):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return regex.match(text)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_emoticon(token):
    for emoticon_category in emoticons:
        for emoticon in emoticons[emoticon_category]:
            if token == emoticon:
                return emoticon_category
    return None

# def quotations_in_beginning_and_end(token):
#     return re.findall(r"[']+|[\w']+", token)
# print(tokenize_corpus("Gas by my house hit $3.39!!!! I'm going to Chapel Hill on Sat :)"))


def clean_text(corpus):
    output = {
        'cleaned_sentences': [],
        'cleaned_corpus': '',
        'urls': [],
        'user_mentions': [],
        'hashtags': [],
        'emoticons': []
    }
    corpus = escape_html_characters(corpus)
    sentences = tokenize_corpus(corpus)
    for sentence in sentences:
        # splitting sentences on white spaces
        tokens = sentence.split()
        # splitting punctuations out of tokens
        index = 0
        while index < len(tokens):
            # Remove any prospective URLS
            if is_url(tokens[index]):
                output['urls'].append(tokens[index])
                del tokens[index]
                continue

            # Recognizing emoticons
            emoticon_category = is_emoticon(tokens[index])
            if emoticon_category is not None:
                output['emoticons'].append(tokens[index])
                tokens[index] = emoticon_category

            splitted_words_and_punctuations = tokenize_sentence(tokens[index])
            if len(splitted_words_and_punctuations) > 1:
                first = True
                temp_index = index
                for token in splitted_words_and_punctuations:
                    if first:
                        first = False
                        del tokens[index]
                        index -= 1
                    tokens.insert(temp_index, token)
                    temp_index += 1
            index += 1
        cleaned_sentence = ''
        index = 0

        if len(tokens) > 0 and tokens[0] == 'RT':
            del tokens[0]

        while index < len(tokens):

            # Finding user mentions in text (specifically for twitter and facebook):
            if tokens[index].startswith("@"):
                output['user_mentions'].append(tokens[index])
                tokens[index] = tokens[index][1:]

            if tokens[index].startswith("#"):
                output['hashtags'].append(tokens[index])
                tokens[index] = tokens[index][1:]

            if not is_number(tokens[index]) and len(tokens[index]) > 1:
                # Contraction removal
                if tokens[index] in contractions:
                    contraction_list = contractions[tokens[index]].split()
                    del tokens[index]
                    temp_index = index
                    for contraction in contraction_list:
                        tokens.insert(temp_index, contraction)
                        temp_index += 1
                    continue

                # Stop word removal
                # if tokens[index] in english_stops:
                #     del tokens[index]
                #     continue

                if tokens[index] in expressions_to_remove:
                    del tokens[index]
                    continue

                # Standardizing words

                if not dictionary.is_english_word(tokens[index]):
                    tokens[index] = delete_continuous_characters(tokens[index], continuous_characters_config['minimum_frequency'])

                # Split Attached Words
                if not dictionary.is_english_word(tokens[index]):
                    predicted_words = infer_spaces(tokens[index])
                    if len(predicted_words) > 1:
                        temp_index = index
                        del tokens[index]
                        for predicted_word in predicted_words:
                            tokens.insert(temp_index, predicted_word)
                            temp_index += 1
                        continue

                # Spelling Correction

                if not dictionary.is_english_word(tokens[index]) and tokens[index] not in punctuation_list:
                    tags = tagger.tag(tokens)
                    if tags[index][1] != 'NNP' and tags[index][1] != 'NP':
                        tokens[index] = spelling_corrector(tokens[index])

            output['cleaned_corpus'] += (" " if tokens[index] not in punctuation_list else "") + tokens[index]
            cleaned_sentence += (" " if tokens[index] not in punctuation_list else "") + tokens[index]
            index += 1

        if cleaned_sentence and not cleaned_sentence[0] in punctuation_list:
            cleaned_sentence = cleaned_sentence[1:]
        output['cleaned_sentences'].append(cleaned_sentence)

    if output['cleaned_corpus'] and not output['cleaned_corpus'][0] in punctuation_list:
        output['cleaned_corpus'] = output['cleaned_corpus'][1:]

    return output

