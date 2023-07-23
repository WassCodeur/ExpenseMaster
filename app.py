#!/usr/bin/python3
from dotenv import load_dotenv
from datetime import datetime
import os
from flask import Flask, render_template, make_response, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib
app = Flask(__name__)

load_dotenv()
appkey = os.getenv('APP_KEY')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db = os.getenv('DB_DATABASE')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

app.secret_key = appkey
app.config["MYSQL_HOST"] = db_host
app.config["MYSQL_USER"] = db_user
app.config["MYSQL_PASSWORD"] = db_password
app.config["MYSQL_DB"] = db
mysql = MySQL(app)

# login
x = datetime.now()
date = x.year
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if 'loggedin' in session:
        return redirect(url_for('logout'))
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM Users WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user[0]
            # session['id'] = int(user['id'])
            # session['email'] = user['email']
            # msg = 'Logged'
            return redirect(url_for('homelogin'))
        else:
            msg = 'Failed Email or Password Incorrect'

    return render_template('login.html', msg=msg, date=date)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/home')
def homelogin():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('homeuser.html', date=date)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/test')
def test():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    return str(rv)


@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('homeuser.html', date=date)
    return render_template('home.html', date=date)


@app.route('/about')
def about():
    if 'loggedin' in session:
        return render_template('aboutuser.html', date=date)
    return render_template('about.html', date=date)


@app.route('/contact')
def contact():
    if 'loggedin' in session:
        return render_template('contactuser.html', date=date)
    return render_template('contact.html', date=date)


# @app.route('/login')
# def login():
#     return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'loggedin' in session:
        return redirect(url_for('logout'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        fullname = request.form['fullname']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        email = request.form['email']
        device = request.form['device']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        elif password != confirmpassword:
            msg = 'Password is different'
        else:
            # Hash the password
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()
            # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
            cursor.execute('INSERT INTO Users  (name, username, password, email, device) VALUES (%s, %s, %s, %s, %s)',
                           (fullname, username, password, email, device,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('signup.html', msg=msg, date=date)


@app.route('/blog')
def blog():
    if 'loggedin' in session:
        return render_template('bloguser.html', date=date)
    return render_template('blog.html', date=date)


@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        # select all expenses ordered by date
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT *  FROM Expenses AS ex INNER JOIN Categories AS ca ON ex.category_id = ca.id WHERE user_id= %s', (session['id'],))
        expenses = cursor.fetchall()
        cursor.execute("SELECT * FROM Users WHERE id = %s", (session['id'],))
        user = cursor.fetchone()
        balance = user['balance']
        device = user['device']
        if device is None:
            device = "$"
        
        if balance is None:
            balance = 0
        balance = float(balance)
        return render_template('dashboard.html',device=device, expenses=expenses, date=date, balance=balance)
    return render_template('login.html', date=date)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Categories')
        categories = cursor.fetchall()
        if request.method == 'POST':
            expensename = request.form['expensename']
            expensecategory = request.form.get('expensecategory')
            date_str = request.form['expensedate']
            expenseamount = request.form['expenseamount']
            description = request.form['description']
            user_id = session['id']
            expensedate = datetime.strptime(date_str, "%Y-%m-%d")
            category_id = expensecategory
            cursor.execute('INSERT INTO Expenses (expense_name, date, amount, user_id, category_id, description) VALUES (%s, %s, %s, %s, %s, %s)',
                           (expensename, expensedate, expenseamount, user_id, category_id, description ,))
            
        return render_template('addspende.html', categories=categories, date=date)
    return render_template('login.html', date=date)


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        return render_template('profile.html', user=user, date=date)
    return render_template('login.html', date=date)

@app.route('/addmoney', methods=['GET', 'POST'])
def increace():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        current = user['balance']
        if current is None:
            current = 0
        if request.method == 'POST':
            current = float(current)
            amount = float(request.form['amount'])
            balance = amount + current
            cursor.execute("UPDATE Users SET balance = %s WHERE id = %s", (balance, user_id,))
            return render_template('/addmoney.html', date=date, balance=balance)
        return render_template('/addmoney.html', date=date)
        
    return render_template('login.html', date=date)

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error404.html', date=date), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(500)
def not_found(error):
    resp = make_response(render_template('error500.html', date=date), 500)
    resp.headers['X-Something'] = 'A value'
    return resp
