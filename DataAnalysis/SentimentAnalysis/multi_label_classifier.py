from DataAnalysis.SentimentAnalysis.feature_extractions import reuters_high_info_words, \
    reuters_train_test_feats, bag_of_words_in_set

rwords = reuters_high_info_words()
featdet = lambda words: bag_of_words_in_set(words, rwords)
multi_train_feats, multi_test_feats = reuters_train_test_feats(featdet)
