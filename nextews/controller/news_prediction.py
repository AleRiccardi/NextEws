import numpy as np
import pandas as pd
import pickle
from keras.models import load_model
from flask import current_app, flash

from .. import db

CLASSIFIER_FILENAME = "review_classifier.pkl"


class NewsPrediction:
    m_model = None

    def __init__(self):
        model = load_model("news_cnn_model.h5")

    def predict(self):
        return 0
