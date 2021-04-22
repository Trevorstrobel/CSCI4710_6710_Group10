#Author:                Trevor Strobel


from flask import request, render_template, flash, redirect, url_for
from mememaker import app
from mememaker.forms import *


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/makeMeme")
def makeMeme():
    return render_template('make_meme.html', title='Make a Meme')

@app.route("/team")
def team():
    return render_template('team.html', title='Team')





if __name__ == '__main__':
    app.run(debug=True)