from DataAnalysis.SentimentAnalysis.max_vote_classifier import mv_classifier
import pickle

f = open('classifier_pickles/mv_classifier.pickle', 'wb')
pickle.dump(mv_classifier, f)
f.close()

