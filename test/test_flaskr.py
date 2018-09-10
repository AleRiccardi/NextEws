import os
import tempfile
import pytest

import pandas as pd


def test_ajax_news(client):
    response = client.get('/ajax_scan_news')
    print(response.data)
    assert response.data == b'true'


def test_ajax_news_cat(client):
    response = client.get('/ajax_categorize_news')
    print(response.data)
    assert response.data == b'true'
