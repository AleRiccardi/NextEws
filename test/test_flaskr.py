import os
import tempfile
import pytest

import pandas as pd

from nextews import get_app


def test_config():
    assert not get_app().testing
    assert get_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'


def test_ajax_news(client):
    response = client.get('/ajax_scan_news')
    print(response.data)
    assert response.data == b'true'
