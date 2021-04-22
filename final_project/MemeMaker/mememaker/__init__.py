#Author:                Trevor Strobel
#Date:                  4/22/2021

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#create Flask instance
app = Flask(__name__)


from mememaker import routes