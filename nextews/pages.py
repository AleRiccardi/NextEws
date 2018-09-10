from os import path
import os
from flask import Flask, jsonify, render_template, current_app
from keras.models import load_model
from . import app, db
from .controller.news_scanner import NewsScanner
from .controller.news_categorization import NewsCategorization
import pandas as pd

@app.route("/")
def home():
    news = db.get_last_news()
    if news and len(news) > 3:
        first_news = news[0]
        next_news = news[1:3]
        last_news = news[3:]
    else:
        first_news = None
        next_news = None
        last_news = None
    categories = db.get_categories()
    sources = db.get_sources()
    return render_template("index.html", sources=sources, source=None, categories=categories, first_news=first_news,
                           next_news=next_news, last_news=last_news)


@app.route("/category/<slug>")
def category(slug):
    # Static information required
    sources = db.get_sources()
    categories = db.get_categories()
    # ________

    the_category = [cat for cat in categories if cat['slug'] == slug][0]
    news = db.get_last_news()
    return render_template("category.html", sources=sources, source=None, categories=categories, category=the_category,
                           news=news)


@app.route("/source/<slug>")
def source(slug):
    # Static information required
    sources = db.get_sources()
    categories = db.get_categories()
    # ________

    the_source = [cat for cat in sources if cat['slug'] == slug][0]
    news = db.get_last_news()
    sources = db.get_sources()
    return render_template("source.html", sources=sources, categories=categories, source=the_source, news=news)


@app.route("/news/<id>")
def news(id):
    # Static information required
    sources = db.get_sources()
    # ________

    the_news = db.get_news_by_id(id)
    return render_template("news.html", sources=sources, source=None, news=the_news)


@app.route("/author/<id>")
def author(id):
    # Static information required
    sources = db.get_sources()
    categories = db.get_categories()
    authors = db.get_authors()
    news = db.get_last_news()
    # ________

    the_author = [auth for auth in authors if auth['id'] == int(id)]
    if the_author:
        the_author = the_author[0]
    else:
        the_author = None

    return render_template("author.html", sources=sources, categories=categories, source=None, author=the_author,
                           news=news)


@app.route("/admin")
def admin():
    sources = db.get_sources()

    return render_template("admin.html", sources=sources, source=None)


@app.route('/ajax_scan_news')
def ajax_scan_news():
    scanner = NewsScanner()
    scanner.run_scraper()
    news = db.get_news_no_category_df()
    json_response = jsonify({
        'success': True,
        'num_new_authors': scanner.m_num_new_authors,
        'num_total_news': scanner.m_num_total_news,
        'num_new_news': scanner.m_num_new_news,
        'num_news_to_categorize': news.shape[0]
    })

    return json_response


@app.route('/ajax_categorize_news')
def ajax_categorize_news():
    news = db.get_news_no_category_df()
    news_cat = NewsCategorization(news)
    news_predicted = news_cat.make_predictions()

    json_response = "{}"
    if news_predicted is not None:
        news_predicted = news_cat.get_predictions_with_name_categories()
        json_response = news_predicted.to_json(orient='index')

    return json_response
