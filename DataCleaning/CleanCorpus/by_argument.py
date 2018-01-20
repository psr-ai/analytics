from DataCleaning.corpus_cleaner import clean_text
import sys, os, re

path_to_file = sys.argv[1]
dir_path = os.path.dirname(path_to_file)
file_name = os.path.basename(path_to_file)
output_file_pattern = os.path.splitext(file_name)[0]
output_path_patten = dir_path + "/cleaned/" + output_file_pattern


def split_tweets(corpus):
    return re.split(r"\r\n|\n", corpus)

with open(path_to_file, "rb") as file:
    output_corpus = file.read().decode('utf-8')

tweets = split_tweets(output_corpus)

if not os.path.exists(dir_path + "/cleaned"):
    os.makedirs(dir_path + "/cleaned")

file_number = 1
for tweet in tweets:
    output_path = output_path_patten + str(file_number) + ".txt"
    output_file = open(output_path, "w")
    output_file.write(clean_text(tweet)['cleaned_corpus'])
    output_file.close()
    file_number += 1







