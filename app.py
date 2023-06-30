#!/usr/bin/python3
from dotenv import load_dotenv
import os
from flask import Flask, render_template, make_response

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db = os.getenv('DB_DATABASE')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(500)
def not_found(error):
    resp = make_response(render_template('error500.html'), 500)
    resp.headers['X-Something'] = 'A value'
    return resp
