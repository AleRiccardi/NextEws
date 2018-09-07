from os import path

from flask import Flask, jsonify, render_template, request, abort, redirect, url_for

from . import app, db
from .model.news import News
from .controller.news_scanner import NewsScanner


@app.route("/")
def home():
    news = db.get_last_news()
    first_news = news[0]
    next_news = news[1:3]
    last_news = news[3:]
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
    news = scanner.run_scraper()
    return jsonify(result=news)
