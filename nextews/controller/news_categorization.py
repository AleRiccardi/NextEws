import re, string, os
import numpy as np
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from keras.models import load_model
import tensorflow as tf
from tensorflow.keras import backend
from tensorflow.python.keras.preprocessing import sequence, text

from flask import current_app, flash, g
from .. import db

nltk.download("punkt", quiet=True)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
PATH_FILES = 'static/util/'
FILE_MODEL = 'news_cnn_model.h5'
FILE_TOKENIZER = 'tokenizer.pickle'


def load_my_model():
    global model
    try:
        model
    except NameError:
        if os.path.getsize(get_model_path()) > 0:
            model = load_model(get_model_path())
    # this is key : save the graph after loading the model
    global graph
    try:
        graph
    except NameError:
        graph = tf.get_default_graph()


def get_model_path():
    return os.path.join(current_app.root_path, PATH_FILES + FILE_MODEL)


def get_tokenizer_path():
    return os.path.join(current_app.root_path, PATH_FILES + FILE_TOKENIZER)


class NewsCategorization:
    MAX_SEQ_LENGTH = 200

    m_model = None
    m_tokenizer = None
    m_news = pd.DataFrame()

    def __init__(self, news):
        if not news.empty:
            self.m_news = news
            # Load model
            load_my_model()
            # Load tokenizer
            if os.path.getsize(get_tokenizer_path()) > 0:
                with open(get_tokenizer_path(), 'rb') as handle:
                    self.m_tokenizer = pickle.load(handle)

    def make_predictions(self):
        if not self.m_news.empty:
            texts = [news['content'] if news['content'] is not "" else news['description'] for index, news in
                     self.m_news.iterrows()]

            cleaned = map(self.clean_doc, texts)
            print(cleaned)
            sequences = self.m_tokenizer.texts_to_sequences(cleaned)
            sequences = sequence.pad_sequences(sequences, maxlen=self.MAX_SEQ_LENGTH, padding='post')

            with graph.as_default():
                predictions = model.predict_classes(sequences)
            self.m_news['id_category'] = predictions

            db.save_df(name='news', df=self.m_news)
            return self.m_news
        return None

    def clean_doc(self, doc):
        """
        Cleaning a document by several methods:
            - Strip word
            - Lowercase
            - Removing whitespaces
            - Removing numbers
            - Removing stopwords
            - Removing punctuations
            - Removing short words
        """
        stop_words = set(stopwords.words('english'))

        # Strip word
        doc = doc.strip()
        # Lowercase
        doc = doc.lower()
        # Remove numbers
        doc = re.sub(r"[0-9]+", "", doc)
        # Split in tokens
        tokens = doc.split()
        # Remove Stopwords
        tokens = [w for w in tokens if not w in stop_words]
        # Remove punctuation
        tokens = [w.translate(str.maketrans('', '', string.punctuation)) for w in tokens]
        # Tokens with less then two characters will be ignored
        tokens = [word for word in tokens if len(word) > 1]
        return ' '.join(tokens)

    def get_predictions_with_name_categories(self):
        if not self.m_news.empty:
            news_to_return = self.m_news
            categories = db.get_categories_df()
            news_to_return['category'] = [categories.iloc[index]['name'] for index in self.m_news['id_category']]
            return news_to_return
        else:
            return None
