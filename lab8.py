from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_, func
from db import db
from db.models import users, articles


lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    if not login_form or not password_form:
        return render_template('lab8/login.html', error='Заполните все поля')
    
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
        session['login'] = login_form
        return redirect('/lab8')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Заполните все поля')
    
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    login_user(new_user, remember=False)
    session['login'] = login_form
    
    return redirect('/lab8')


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    session.pop('login', None)
    return redirect('/lab8')


@lab8.route('/lab8/articles')
def articles_list():
    search_query = request.args.get('search', '').strip()
    
    if current_user.is_authenticated:
        base_query = articles.query.filter(
            or_(
                articles.login_id == current_user.id,
                articles.is_public == True
            )
        )
    else:
        base_query = articles.query.filter_by(is_public=True)
    
    if search_query:
        # Регистронезависимый поиск по заголовку и тексту
        search_filter = or_(
            articles.title.ilike(f'%{search_query}%'),
            articles.article_text.ilike(f'%{search_query}%')
        )
        user_articles = base_query.filter(search_filter).order_by(articles.id.desc()).all()
    else:
        user_articles = base_query.order_by(articles.id.desc()).all()
    
    return render_template('lab8/articles.html', 
                         articles=user_articles, 
                         search_query=search_query)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create.html', error='Заполните заголовок и текст статьи')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    flash('Статья успешно создана!', 'success')
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        flash('Статья не найдена', 'error')
        return redirect('/lab8/articles')
    
    if article.login_id != current_user.id:
        flash('Вы не можете редактировать чужую статью', 'error')
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    is_favorite = request.form.get('is_favorite') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error='Заполните заголовок и текст статьи')
    
    article.title = title
    article.article_text = article_text
    article.is_public = is_public
    article.is_favorite = is_favorite
    
    db.session.commit()
    
    flash('Статья успешно обновлена!', 'success')
    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        flash('Статья не найдена', 'error')
        return redirect('/lab8/articles')
    
    if article.login_id != current_user.id:
        flash('Вы не можете удалить чужую статью', 'error')
        return redirect('/lab8/articles')
    
    db.session.delete(article)
    db.session.commit()
    
    flash('Статья успешно удалена!', 'success')
    return redirect('/lab8/articles')


@lab8.route('/lab8/like/<int:article_id>', methods=['POST'])
@login_required
def like_article(article_id):
    article = articles.query.get(article_id)
    
    if not article:
        flash('Статья не найдена', 'error')
        return redirect('/lab8/articles')
    
    if article.login_id == current_user.id:
        flash('Вы не можете лайкать свою статью', 'warning')
        return redirect('/lab8/articles')
    
    article.likes += 1
    db.session.commit()
    
    flash('Спасибо за лайк!', 'success')
    return redirect('/lab8/articles')