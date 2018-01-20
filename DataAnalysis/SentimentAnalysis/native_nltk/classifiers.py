from nltk.classify import NaiveBayesClassifier, MaxentClassifier, DecisionTreeClassifier, accuracy
from DataAnalysis.SentimentAnalysis.data import training_testing_data


train_feats, test_feats = training_testing_data.high_information_wordset()

def classifier(train_feats, model='nb_classifier'):
    if model is 'nb_classifier':
        return NaiveBayesClassifier.train(train_feats)

    elif model is 'dt_classifier':
        return DecisionTreeClassifier.train(train_feats, binary=True, entropy_cutoff=0.8, depth_cutoff=5,
                                            support_cutoff=30)

    elif model is 'me_classifier':
        return MaxentClassifier.train(train_feats, algorithm='gis', trace=0, max_iter=10, min_lldelta=0.5)

#
# nb_classifier = NaiveBayesClassifier.train(train_feats)
# test_sentence = "The movie was terrible".split()
#
# print(nb_classifier.classify(bag_of_words_with_counts(test_sentence)))



