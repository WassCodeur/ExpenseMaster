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
app = Flask(__name__)
app.config["MYSQL_HOST"] = db_host
app.config["MYSQL_USER"] = db_user
app.config["MYSQL_PASSWORD"] = db_password
app.config["MYSQL_DB"] = db
mysql = MySQL(app)

@app.route("/")
def users():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM Users""")
    rv = cur.fetchall()
    return str(rv)

if __name__ == "__main__":
    app.run(debug=True)