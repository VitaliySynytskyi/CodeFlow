# cats.py
from flask import render_template

from app import app
from utils import get_random_cat, get_random_cat_fact

@app.route("/cats", methods=("GET", "POST"), strict_slashes=False)
def cats():
    random_cat_url = get_random_cat()
    random_cat_fact = get_random_cat_fact()
    return render_template("cats.html", title="Cats", random_cat_url=random_cat_url, random_cat_fact=random_cat_fact)

@app.route("/api_cats_fact")
def api_cats_fact():
    random_cat_fact = get_random_cat_fact()
    return random_cat_fact

@app.route("/api_cats_picture")
def api_cats_picture():
    random_cat_url = get_random_cat()
    return random_cat_url
