# home.py
from flask import render_template

from app import app, telemetry_client

@app.route("/", methods=("GET", "POST"), strict_slashes=False)
@app.route("/home", methods=("GET", "POST"), strict_slashes=False)
def home():
    telemetry_client.track_trace("Home page requested")  # Логування Application Insights
    return render_template("home.html", title="Home")

@app.route("/about/", methods=("GET", "POST"), strict_slashes=False)
def about():
    telemetry_client.track_trace("About page requested")  # Логування Application Insights
    return render_template('about.html')
