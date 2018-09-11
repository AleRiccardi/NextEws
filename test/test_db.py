import os
import tempfile
import pytest
import sqlite3

import pandas as pd

from nextews import db

# def test_get_size_author(app):
#     with app.app_context():
#         authors = db.get_authors_df()
#         print(authors)
#         assert authors.shape[0] != 0
