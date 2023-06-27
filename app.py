#!/usr/bin/python3
from flask import Flask, render_template, make_response


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/blog/')
def blog():
    return render_template('blog.html')


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(500)
def not_found(error):
    resp = make_response(render_template('error500.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


if __name__ == '__main__':
    app.run(debug=True)
