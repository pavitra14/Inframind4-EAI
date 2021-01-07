from TextSentiment.utils import *

saveModel = "social_model.data"

def analyse_sentiment(text):
    classifier = loadModel(saveModel)
    custom_tokens = remove_noise(word_tokenize(text))
    data = classifier.classify(dict([token, True] for token in custom_tokens))
    print(text, data)
    return data