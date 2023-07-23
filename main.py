#!/usr/bin/python3
from dotenv import load_dotenv
import os
from flask import Flask, render_template, make_response, request, redirect, url_for, session
from flask_mysqldb import MySQL

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db = os.getenv('DB_DATABASE')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_DB'] = "expensemaster"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
mysql = MySQL(app)

# Fetch form data
with app.app_context():
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT * from Users")
    user = cursor.fetchone()

print(user)
