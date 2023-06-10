# profile.py
from flask import render_template

from app import app
from flask_login import login_required

@app.route("/profile/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def profile():
    return render_template('profile.html')
