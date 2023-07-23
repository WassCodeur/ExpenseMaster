from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db = os.getenv('DB_DATABASE')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
print(db_host, db_port, db, db_user, db_password)
print(type(db_host))
print(type(db_port))
print(type(db))
print(type(db_user))
app = Flask(__name__)
app.config['MYSQL_HOST'] =db_host
app.config['MYSQL_PORT'] =db_port
app.config['MYSQL_DB'] =db
app.config['MYSQL_USER'] =db_user
app.config['MYSQL_PASSWORD'] = db_password
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CUSTOM_OPTIONS"] = {"ssl": {"ca": "/path/to/ca-file"}}
mysql = MySQL(app)
