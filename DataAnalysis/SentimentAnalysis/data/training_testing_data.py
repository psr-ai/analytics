from DataAnalysis.SentimentAnalysis.feature_extractions import high_information_words, \
    bag_of_words_in_set, label_feats_from_corpus,label_feats_from_corpus_with_bigrams, split_label_feats, \
    bag_of_words_with_counts, bag_of_words_in_set_with_count
from nltk.corpus import movie_reviews
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus import CategorizedPlaintextCorpusReader

polarity = LazyCorpusLoader('polarity', CategorizedPlaintextCorpusReader, r'(?!\.).*\.txt',
                            cat_pattern=r'(polar|nonpolar)/.*', encoding='latin-1')
corpus = movie_reviews


def high_information_wordset():
    labels = corpus.categories()
    labelled_words = [(l, corpus.words(categories=[l])) for l in labels]
    high_info_words = set(high_information_words(labelled_words))
    feat_det = lambda words: bag_of_words_in_set_with_count(words, high_info_words)
    lfeats = label_feats_from_corpus_with_bigrams(corpus, feature_detector=feat_det)
    return split_label_feats(lfeats)


def wordset():
    lfeats = label_feats_from_corpus(corpus, feature_detector=bag_of_words_with_counts)
    return split_label_feats(lfeats, split=0.75)

high_information_wordset()