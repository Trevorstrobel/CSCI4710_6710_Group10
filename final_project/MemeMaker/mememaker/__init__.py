#Author:                Trevor Strobel
#Date:                  4/22/2021

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = '22ed86cf8f09a5e907b70d9ee2013504'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mmadmin:csci4710@localhost/mememaker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



from mememaker import routes