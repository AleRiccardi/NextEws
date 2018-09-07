import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import pandas as pd
from .model.news import News

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


def query_df(sql, *params):
    return pd.read_sql(sql, get_db(), params=params)


def query_dict(sql, *params):
    return pd.read_sql(sql, get_db(), params=params).to_dict('records')


def save_df(name, df):
    print(df)
    df.to_sql(name, get_db(), if_exists='append', index=False)


def query_one_dict(sql, *params):
    results = query_dict(sql, *params)
    if len(results) == 1:
        return results[0]
    elif len(results) == 0:
        return None
    else:
        raise Exception("More than one row")


def get_news_by_id(id):
    return query_one_dict("SELECT * FROM news WHERE id=?", id)


def get_news_by_ids(ids):
    query_news = query_dict("SELECT * FROM news WHERE id in ({})".format(",".join("?" * len(ids))), *ids)
    news = [News(the_news) for the_news in query_news]
    return news


def get_news():
    """
    Get all news in dictionary format.
    :return: dictionary
    """
    query_news = query_dict("SELECT * FROM news ORDER BY published_at DESC")
    news = [News(the_news) for the_news in query_news]
    return news


def get_news_df():
    """
    Get all news in data-frame format.
    :return: Pandas data-frame
    """
    query_news = query_df("SELECT * FROM news ORDER BY published_at DESC")
    news = [News(the_news) for the_news in query_news]
    return news


def get_last_news_single():
    query_news = query_one_dict("SELECT * FROM news ORDER BY published_at DESC LIMIT 1")
    return query_news

def get_last_news(limit_num=20):
    query_news = query_dict("SELECT * FROM news ORDER BY published_at DESC LIMIT ?", limit_num)
    news = [News(the_news) for the_news in query_news]
    return news


def get_categories():
    """
    Get all sources in dictionary format.
    :return: dictionary
    """
    return query_dict("SELECT * FROM categories")


def get_categories_df():
    """
    Get all categories in data-frame format.
    :return: data-frame
    """
    return query_df("SELECT * FROM categories")


def get_sources():
    """
    Get all sources in dictionary format.
    :return: dictionary
    """
    return query_dict("SELECT * FROM sources")


def get_sources_df():
    """
    Get all sources in data-frame format.
    :return: Pandas data-frame
    """
    return query_df("SELECT * FROM sources")


def get_authors():
    """
    Get all authors in dictionary format.
    :return: dictionary
    """
    return query_dict("SELECT * FROM authors")


def get_authors_df():
    """
    Get all authors in data-frame format.
    :return: Pandas data-frame
    """
    return query_df("SELECT * FROM authors")
