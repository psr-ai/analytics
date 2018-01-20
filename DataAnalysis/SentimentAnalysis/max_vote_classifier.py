from DataAnalysis.SentimentAnalysis.native_nltk import classifiers as native_classifiers
from DataAnalysis.SentimentAnalysis.scikit import classifiers as sk_classifiers
from nltk.classify import accuracy
from DataAnalysis.SentimentAnalysis.data import training_testing_data
from DataAnalysis.SentimentAnalysis.feature_extractions import bag_of_words, bag_of_words_with_counts
import itertools
from nltk.classify import ClassifierI
from nltk.probability import FreqDist


class MaxVoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers
        self._labels = sorted(set(itertools.chain(*[c.labels() for c in classifiers])))
        self._cutOffForNeutral = 0.55

    def labels(self):
        return self._labels

    def classify(self, feats):
        counts = FreqDist()
        for classifier in self._classifiers:
            counts[classifier.classify(feats)] += 1
        return counts.max()

    def probability(self, feats):
        classification = dict()
        for classifier in self._classifiers:
            for label in classifier.labels():
                if label in classification:
                    classification[label] += classifier.prob_classify(feats).prob(label)
                else:
                    classification[label] = classifier.prob_classify(feats).prob(label)

        for key in classification:
            classification[key] /= len(self._classifiers)

        return classification

    def classify_with_neutral(self, feats):
        classification = self.probability(feats)
        for label in self._labels:
            if classification[label] > self._cutOffForNeutral:
                return label
        return 'neutral'

train_feats, test_feats = training_testing_data.high_information_wordset()

nb_classifier = native_classifiers.classifier(train_feats)
me_classifier = native_classifiers.classifier(train_feats, model='me_classifier')
multinomial_nb = sk_classifiers.classifier(train_feats)
mv_classifier = MaxVoteClassifier(nb_classifier, me_classifier, multinomial_nb)

#
print(accuracy(nb_classifier, test_feats))
print(accuracy(me_classifier, test_feats))
print(accuracy(multinomial_nb, test_feats))
print(nb_classifier.show_most_informative_features(n=1000))
print(mv_classifier.classify({'enjoyable': 1, 'movie': 1}))
# sentence = "my life has become a hell"
# print(mv_classifier.classify_with_neutral(bag_of_words(sentence.split())))
# multinomial_nb.prob_classify(bag_of_words(sentence.split())).prob('nonpolar')

