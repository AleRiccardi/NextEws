import os
import tempfile

import pytest
from nextews import get_app
from nextews.db import get_db, init_db


# Temporary Database not available 'data.sql', used the default
# one that you can see in the nextews/db.py file.

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = get_app({
        'TESTING': True,
        #'DATABASE': db_path,
    })

    # Uncomment this if you want to test with a db
    # that you will create at the moment
    #with app.app_context():
        #init_db()
        #get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
