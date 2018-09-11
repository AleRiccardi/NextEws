from flask import Flask
import os

# ===================================================================
# Creation of App
# ===================================================================

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='3f9rwhv0e8ht9c49y5437ytc9',
)

# load the instance config, if it exists, when not testing
app.config.from_pyfile('config.py', silent=True)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

from . import db

db.init_app(app)
from . import pages


def get_app(test_config=None):
    """
    Return the application from outside this scope.
    """
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    return app
