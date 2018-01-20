import nltk, os
from nltk.corpus import brown, treebank
from nltk.tag import tnt, DefaultTagger
from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.classify import MaxentClassifier
from pickle import load, dump

# nltk.data.path.append("E:/Analytics Practice/Social Media Analytics/analyticsPlatform")
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'me_tagger.pkl'), 'rb') as pickle_file:
    tagger = load(pickle_file)


def tag(splitted_sentence):
    return tagger.tag(splitted_sentence)

# brown_tagged_sents = brown.tagged_sents(categories='news')
# size = int(len(brown_tagged_sents) * 0.9)
#
# train_sents = brown_tagged_sents[:size]
# test_sents = brown_tagged_sents[size:]

# t0 = nltk.DefaultTagger('NN')
# t1 = nltk.UnigramTagger(train_sents, backoff=t0)
# t2 = nltk.BigramTagger(train_sents, backoff=t1)
# print(t2.tag("The President said he will ask Congress to increase grants to states for Voldemort rehabilitation".split()))
# print(t2.evaluate(test_sents))
# unk = DefaultTagger('NN')
# tnt_tagger = tnt.TnT(unk=unk, Trained=True, C=True)
# tnt_tagger.train(train_sents)
# print(tnt_tagger.evaluate(test_sents))

# tagger = ClassifierBasedPOSTagger(train=train_sents)
# print(tagger.evaluate(test_sents))

# me_tagger = ClassifierBasedPOSTagger(train=train_sents, classifier_builder=lambda train_feats: MaxentClassifier.train(train_feats, max_iter=15))
# output = open('me_tagger_treebank.pkl', 'wb')
# dump(me_tagger, output, -1)
# output.close()
# print(tagger.tag('My new watch is awesome!'.split()))


