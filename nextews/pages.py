from os import path

from flask import render_template, request, abort, redirect, url_for

from . import app, db


@app.route("/")
def home():
    news = db.get_all_news()
    last_news = news.iloc[0]
    next_two_news = news.iloc[1:3]
    news = news[3:]
    return render_template("index.html", last_news=last_news, next_two_news=next_two_news, news=news)

