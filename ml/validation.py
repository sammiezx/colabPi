import spacy
import os
import sys
from datetime import datetime, timedelta
import pytz
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

for x in ["/home/samir/Desktop/ARIMA/colab/server"]:
    if os.path.isdir(x):
        sys.path.insert(0, x)
from database.post_adapter import get_post_from_post_id
from utils.parser_util import one_post_row_to_json
import server.ml.image_ml_lib.master as imageMaster
import ml.language_ml_lib.master as languageMaster

class Validation:
    def __init__(self):
        self.imageMaster = imageMaster()
        self.languageMaster = languageMaster()
    
    def _validate_upload_date(self, uploaded_at):        
        current_time = datetime.now(pytz.utc)
        time_difference = current_time - uploaded_at
        if time_difference <= timedelta(hours=3):
            return True
        else:
            raise Exception("Post verification time expired")
        
    def _validate_language(self, comparision, polarity):
        if ((comparision > 0.1) & (polarity > 0.1)):
            return True
        else:
            return False
        
    def _validate_image(self, image, image_context):
        return self.imageMaster.vector_product(image, image_context)
    
    def validate_post(self, campaign, post_id):
        post = one_post_row_to_json(get_post_from_post_id(post_id))
        self._validate_upload_date(post['upload_time'])

        comparision = self.languageMaster.compare_caption_with_keywords(campaign['keywords'], post['caption'])
        polarity = self.languageMaster.sentiment_analyze(post['caption'])

        assert self._validate_image(post['image'], campaign['image_context'])
        assert self._validate_language(comparision, polarity)
    
    def test_eligibility(self, campaign, caption, image):
        comparision = self.languageMaster.compare_caption_with_keywords(campaign['keywords'], caption)
        polarity = self.languageMaster.sentiment_analyze(caption)

        assert self._validate_image(image, campaign['image_context'])
        assert self._validate_language(comparision, polarity)
        
        #NOTE update this to send vector dot product magnitude as score in someway
        return True