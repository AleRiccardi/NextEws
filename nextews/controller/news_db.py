import pandas as pd
import numpy as np

from newsapi import NewsApiClient
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

from os import path

from .. import app, db


class NewsDb:
    m_news = None

    def __init__(self, news):
        self.m_news = news


