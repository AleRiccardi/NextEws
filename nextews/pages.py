from os import path

from flask import render_template, request, abort, redirect, url_for

from . import app, db


@app.route("/")
def home():
    news = db.get_all_news()
    last_news = news.iloc[0]
    next_two_news = news.iloc[1:3]
    news = news[3:3 + 5]
    categories = db.get_categories()
    sources = db.get_sources()
    return render_template("index.html", sources=sources, source=None, categories=categories, last_news=last_news,
                           next_two_news=next_two_news,
                           news=news)


@app.route("/category/<slug>")
def category(slug):
    categories = db.get_categories().to_dict('records')
    the_category = [cat for cat in categories if cat['slug'] == slug][0]
    news = db.get_all_news()
    sources = db.get_sources()
    return render_template("category.html", sources=sources, source=None, category=the_category, news=news)


@app.route("/source/<slug>")
def source(slug):
    sources = db.get_sources().to_dict('records')
    the_source = [cat for cat in sources if cat['slug'] == slug][0]
    news = db.get_all_news()
    sources = db.get_sources()
    return render_template("source.html", sources=sources, source=the_source, news=news)
