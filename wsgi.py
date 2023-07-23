#!/usr/bin/python3
from app import app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    appenv = os.getenv('APP_ENV')
    if appenv == "local":
        app.run(debug=True)
    elif appenv == "production":
        app.run()
   