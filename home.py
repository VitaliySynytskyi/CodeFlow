# home.py
from flask import render_template

from app import app

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
@app.route("/home", methods=("GET", "POST"), strict_slashes=False)
def home():
    return render_template("home.html", title="Home")

@app.route("/about/", methods=("GET", "POST"), strict_slashes=False)
def about():
    return render_template('about.html')