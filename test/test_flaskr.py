import os
import tempfile
import pytest

import pandas as pd
from nextews import app, db


def test_ajax_news_process(client):
    response = client.get('/ajax_news_process')
    print(response.data)
    assert response.data == b'true'

#
# def test_ajax_news_cat(client):
#     with app.app_context():
#         old_news = db.get_news_df()
#
#     print(old_news)
#     assert old_news == b'true'
