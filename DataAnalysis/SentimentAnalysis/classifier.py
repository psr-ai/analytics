import pickle, os
from DataAnalysis.SentimentAnalysis.feature_extractions import bag_of_words
print("Loading maximum vote classifier for sentiment analysis...")
f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'classifier_pickles/mv_classifier.pickle'), 'rb')
mv_classifier = pickle.load(f)
f.close()
print("Classifier loaded successfully.")
#
# input_sentence_1 = "sun revolves around the earth"
# input_sentence_2 = "my new life has become a hell"
# print(mv_classifier.classify_with_neutral(bag_of_words(input_sentence_1)))
# print(classifier.classify_with_neutral(bag_of_words(input_sentence_2)))
