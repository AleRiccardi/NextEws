import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import pandas as pd

DB_FILENAME = "nextews.sql"


def init_db():
    db = get_db()
    with current_app.open_resource('nextews.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def query(sql, *params):
    return pd.read_sql(sql, get_db(), params=params)


def query_one(sql, *params):
    results = query(sql, *params)
    if len(results) == 1:
        return results.iloc[0].to_dict()
    elif len(results) == 0:
        return None
    else:
        raise Exception("More than one row")


def get_news_by_id(id):
    return query_one("SELECT * FROM news WHERE id=?", id)


def get_news_by_ids(ids):
    return query("SELECT * FROM news WHERE id in ({})".format(",".join("?" * len(ids))),
                 *ids)


def get_all_news():
    return query("SELECT * FROM news ORDER BY published_at DESC")


def get_last_news():
    return query("SELECT * FROM news ORDER BY published_at DESC LIMIT 1")
