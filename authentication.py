# authentication.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user

from app import app, bcrypt, db
from models import User
from forms import login_form, register_form

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
