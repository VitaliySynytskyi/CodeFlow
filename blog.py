# blog.py
from datetime import datetime
import os
import emoji
from flask import render_template, flash, redirect, request, url_for, abort
from flask_login import current_user, login_required
from app import app, db
from models import Post
from forms import PostForm, SearchForm
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(os.getenv('AzureKeyCredential'))
    text_analytics_client = TextAnalyticsClient(
            endpoint=os.getenv('endpoint'), 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis_example(client, text):
    document = [text]
    response = client.analyze_sentiment(documents=document)[0]
    return response.sentiment

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    posts = Post.query.paginate(page=page, per_page=per_page)
    total_pages = posts.pages
    return render_template('blog.html', posts=posts.items, pagination=posts, total_pages=total_pages)

@app.route('/post/<int:post_id>')
def detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('detail.html', post=post)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # Замінюємо емодзі на текст перед збереженням
        title_text = emoji.demojize(title)
        content_text = emoji.demojize(content)
        
        # Додамо аналіз почуттів
        sentiment = sentiment_analysis_example(client, title_text+content_text)

        if sentiment == "negative":
            flash('Your post has negative sentiment! Please modify your post', 'warning')
            return redirect(url_for('blog'))
        
        post = Post(
            title=title_text,
            date=datetime.now(),
            content=content_text,
            user_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))

    return render_template('new_post.html', form=form)



@app.route('/post/<int:post_id>/delete')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted', 'success')
    return redirect(url_for('blog'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    form = PostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # Замінюємо емодзі на текст перед оновленням
        title_text = emoji.demojize(title)
        content_text = emoji.demojize(content)
        
        # Додамо аналіз почуттів
        sentiment = sentiment_analysis_example(client, title_text+content_text)
        
        if sentiment == "negative":
            flash('Your post has negative sentiment! Please modify your post', 'warning')
            return redirect(url_for('blog'))

        post.title = title_text
        post.content = content_text
        db.session.commit()
        flash('Post updated', 'success')
        return redirect(url_for('detail', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('update.html', form=form, post=post)



    
@app.route('/post/search' , methods=['GET', 'POST'])
def search():
    form = SearchForm()  
    if form.validate_on_submit():
        posts = Post.query.filter(Post.title.like(f"%{form.query.data}%")).all()
        if posts:
            return render_template('search.html', posts=posts , form=form)
        else:
            flash('No such post has been found!','danger')
            return render_template('search.html',form=form)    
    return render_template('search.html', form=form)  

