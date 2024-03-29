from datetime import datetime
import os
import emoji
from flask import flash
from flask_login import current_user, login_required
from app import app, db
from models import Answer, Question
from forms import AnswerForm, QuestionForm
from flask import render_template, request, redirect, url_for
from utils import client, sentiment_analysis_example

@app.route('/question_list')
def question_list():
    questions = Question.query.all()
    return render_template('question_list.html', questions=questions)

@app.route('/new_question', methods=['GET', 'POST'])
@login_required
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(title=form.title.data, details=form.details.data, user_id=current_user.id)

        # Додамо аналіз почуттів
        sentiment = sentiment_analysis_example(client, question.title + question.details)

        if sentiment == "negative":
            flash('Your post has negative sentiment! Please modify your post', 'warning')
            return redirect(url_for('question_list'))

        db.session.add(question)
        db.session.commit()

        return redirect(url_for('question_detail', question_id=question.id))
    return render_template('new_question.html', form=form)

@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    question = Question.query.get(question_id)
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(text=form.text.data, user_id=current_user.id, question_id=question_id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('question_detail', question_id=question_id))
    return render_template('question_detail.html', question=question, form=form)

@app.route('/question/<int:question_id>/new_answer', methods=['GET', 'POST'])
@login_required
def new_answer(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(text=form.text.data, user_id=current_user.id, question_id=question_id)

        # Додамо аналіз почуттів
        sentiment = sentiment_analysis_example(client, answer.text)

        if sentiment == "negative":
            flash('Your answer has negative sentiment! Please modify your answer', 'warning')
            return redirect(url_for('question_detail', question_id=question_id))

        db.session.add(answer)
        db.session.commit()

        return redirect(url_for('question_detail', question_id=question_id))
    return render_template('new_answer.html', form=form)

