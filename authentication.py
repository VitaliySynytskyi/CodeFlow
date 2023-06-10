# authentication.py
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user
from app import app, bcrypt, db, oauth
from models import User
from forms import login_form, register_form
import os
import secrets

@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Invalid Username or password!", "danger")

    return render_template("auth.html", form=form, text="Login", title="Login", btn_action="Login")

@app.route('/login/google/')
def google():
    GOOGLE_CLIENT_ID = os.getenv('FN_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('FN_CLIENT_SECRET')

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    print(" Google User ", user)
    return redirect('/')

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        username = form.username.data
        
        newuser = User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password),
        )

        db.session.add(newuser)
        db.session.commit()
        flash("Account Successfully created", "success")
        return redirect(url_for("login"))

    return render_template("auth.html", form=form, text="Create account", title="Register", btn_action="Register account")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
