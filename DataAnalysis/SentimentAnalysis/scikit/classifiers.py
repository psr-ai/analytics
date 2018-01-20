from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import NuSVC, LinearSVC, SVC


def classifier(train_feats, model='multinomial_nb'):

    if model is 'multinomial_nb':
        sk_classifier = SklearnClassifier(MultinomialNB())
    elif model is 'linear_svc':
        sk_classifier = SklearnClassifier(LinearSVC())
    elif model is 'nu_svc':
        sk_classifier = SklearnClassifier(NuSVC())
    elif model is 'svc':
        sk_classifier = SklearnClassifier(SVC())
    else:
        return None
    sk_classifier.train(train_feats)
    return sk_classifier

# print(accuracy(classifier(model='nu_svc'), test_feats))