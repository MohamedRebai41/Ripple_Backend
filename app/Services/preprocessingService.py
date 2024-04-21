import re
import emoji
from googletrans import Translator
from pinecone import Index
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect


class PreprocessingService:
    def __init__(self, translator:Translator):
        self.translator = translator
        self.stop_words = set(stopwords.words('english'))
    def preprocess_query(self,query:str):
        if(detect(query) != 'en'):
            query = self.translator.translate(query).text
        query = query.lower()
        #Remove URLs
        query = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', query)
        #Remove Emails
        query = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', query)
        # Remove emojis
        query = emoji.replace_emoji(query, ' ')
        # Remove any non standard character
        pattern = '[^a-z0-9 ]'
        query = re.sub(pattern, ' ', query)
        # Replace any white spaces with a single space
        query = re.sub(r'\s+', ' ', query)    
        #tokenize and remove stop_words
        words = word_tokenize(query)
        words = [word for word in words if word not in self.stop_words]
        query = ' '.join(words)
        return query
