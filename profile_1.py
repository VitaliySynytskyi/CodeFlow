# profile.py
import bcrypt
from flask import flash, redirect, render_template, request, url_for
from app import app, db
from flask_login import current_user, login_required

from forms import UpdateProfileForm

@app.route("/profile/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def profile():
    return render_template('profile.html')

@app.route('/change', methods=['GET', 'POST'])
@login_required
def change_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        if bcrypt.checkpw(form.old_password.data.encode('utf-8'), current_user.password.encode('utf-8')):
            current_user.username = form.username.data
            current_user.password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.session.commit()

            flash('Profile updated successfully', 'success')
            return redirect(url_for('profile'))

        else:
            flash('Invalid old password. Please try again.', 'danger')

    elif request.method == 'GET':
        form.username.data = current_user.username

    return render_template('change_profile.html', form=form, errors=form.errors)