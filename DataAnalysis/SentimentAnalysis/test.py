import nltk
from nltk.corpus import LazyCorpusLoader, CategorizedPlaintextCorpusReader
from DataCleaning.POSTagger import tagger
from nltk.corpus.reader import sentiwordnet
movie_reviews123 = LazyCorpusLoader(
    'movie_reviews123', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(neg|pos|neutral)/.*',
    encoding='ascii')

print(movie_reviews123.categories())

print(nltk.tag._pos_tag())
