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

print(db_host)
print(db_port)
print(db)