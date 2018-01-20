from nltk.corpus import movie_reviews
from DataAnalysis.SentimentAnalysis.data.training_testing_data import polarity
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import TrigramAssocMeasures
from nltk.corpus import stopwords

stop_set = set(stopwords.words('english'))
words = []
for word in movie_reviews.words():
    if len(word) > 2 and word.lower() not in stop_set:
        words.append(word)

bcf = TrigramCollocationFinder.from_words(words)

# filter_stops = lambda w: len(w) < 3 or w in stopset
# bcf.apply_word_filter(filter_stops)
print(bcf.nbest(TrigramAssocMeasures.likelihood_ratio, 200))
