from nltk.tag import pos_tag
import re
import nltk

def tokenize_sentence(sentence):
    return re.findall(r"[\w']+|[.,!+?;]+", sentence)

sentence = "AAPL refuses maintenance, to working woman"
tagged_sent = pos_tag(tokenize_sentence(sentence))
print(tagged_sent)
# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds', 'NNP')]

propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
print(propernouns)
# ['Michael','Jackson', 'McDonalds']

print(nltk.help.upenn_tagset())

# [('Michael', 'NNP'), ('Jackson', 'NNP'), ('likes', 'VBZ'), ('to', 'TO'), ('eat', 'VB'), ('at', 'IN'), ('McDonalds.', 'NNP'), ('How', 'NNP'), ('are', 'VBP'), ('you', 'PRP'), ('doing?', 'VBP')]

#
index = 0
