import spacy
import os
import sys
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

for x in ["/home/samir/Desktop/ARIMA/colab/server"]:
    if os.path.isdir(x):
        sys.path.insert(0, x)

class ImageMaster:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def compare_caption_with_keywords(self, keywords, caption):
        caption_doc = self.nlp(caption)
        keyword_docs = [self.nlp(keyword) for keyword in keywords]        
        similarity_scores = []
        for keyword_doc in keyword_docs:
            similarity_scores.append(max([token.similarity(keyword_token) for token in caption_doc for keyword_token in keyword_doc]))
        if similarity_scores:
            normalized_score = sum(similarity_scores) / len(similarity_scores)
        else:
            normalized_score = 0
        return normalized_score

    def sentiment_analyze(self, caption):
        blob = TextBlob(caption)
        polarity = blob.sentiment.polarity
        return polarity
    