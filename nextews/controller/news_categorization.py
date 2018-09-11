import re, string, os
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from keras.models import load_model
import tensorflow as tf
from tensorflow.python.keras.preprocessing import sequence

from flask import current_app
from .. import db

"""
This file contains functions and a class that permit
to do text-classification throw neural networks.

@author:    Alericcardi
@version:   1.0.0
"""

nltk.download("punkt", quiet=True)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
PATH_FILES = 'static/util/'
FILE_MODEL = 'news_cnn_model.h5'
FILE_TOKENIZER = 'tokenizer.pickle'


def load_my_model():
    """
    That function permit to load only one time the model and the
    graph to store them in the global variables.
    (Resolve a bug that flask present with the keras library)

    @author:    Alericcardi
    @version:   1.0.0
    """
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
    """
    The class do text-classification on news contents and permit
    to return the specific category. It uses a model that were alredy
    trained in the past with an high accuracy.

    @author:    Alericcardi
    @version:   1.0.0
    """
    MAX_SEQ_LENGTH = 200

    m_model = None
    m_tokenizer = None
    m_news = pd.DataFrame()

    def __init__(self, news):
        """
        The cunstructor loads the model, the tokenizer and store the news .
        :param news: data-frame news (pandas)
        """
        if not news.empty:
            self.m_news = news
            # Load model
            load_my_model()
            # Load tokenizer
            if os.path.getsize(get_tokenizer_path()) > 0:
                with open(get_tokenizer_path(), 'rb') as handle:
                    self.m_tokenizer = pickle.load(handle)

    def make_predictions(self):
        """
        This function is triggered when we want to start the text
        classification on the news that were given in the constructor.

        :return: the news with the id_category column filled, else a None
         value if presents problems.
        """
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

        :return: cleaned text.
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
        """
        Permit to retrieve the words of the specific category
        (and not a number) for a better visualization.

        :return: the news data-frame with the category column,
         else a None value if presents
        problems.
        """
        if not self.m_news.empty:
            news_to_return = self.m_news
            categories = db.get_categories_df()
            news_to_return['category'] = [categories.iloc[index]['name'] for index in self.m_news['id_category']]
            return news_to_return
        else:
            return None
