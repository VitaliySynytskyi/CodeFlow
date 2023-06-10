# blog.py
import datetime
import emoji
from flask import render_template, flash, redirect, request, url_for, abort
from flask_login import current_user, login_required

from app import app, db
from models import Post
from forms import PostForm, SearchForm

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
        
        post = Post(
            title=title_text,
            date=datetime.now(),
            content=content_text,
            user_id=current_user.id
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
    return redirect(url_for('home'))


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    
    if post.author != current_user:
        abort(403)

    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
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

