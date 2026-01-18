from flask import Blueprint, render_template, request, redirect, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

def get_db_connection():
    return psycopg2.connect(
        host='127.0.0.1',
        database='tuyana_lombocyrenova_knowledge_base',
        user='tuyana_lombocyrenova_knowledge_base',
        password='799034'
    )

@lab8.route('/lab8')
def lab():
    login = session.get('login')
    return render_template('lab8/lab8.html', login=login)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    return redirect('/lab8')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    return redirect('/lab8')

@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles.html')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    return redirect('/lab8')