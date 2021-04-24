#Author:                Trevor Strobel


from flask import request, render_template, flash, redirect, url_for
from mememaker import app, db
from mememaker.models import Image, Meme
from mememaker.forms import *



#creates tables if they dont exist
try:
    db.create_all()
    print("Tables created successfully.")
except:
    print("Table creation failed.")



#------------------------------Static Routes--------------------------------

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')
@app.route("/team")
def team():
    return render_template('team.html', title='Team')



#------------------------------Meme Routes--------------------------------
#selectTemplate Route
@app.route("/selectTemplate")
def selectTemplate():

    img_templates = Image.query.with_entities(Image.id, Image.imageName, Image.imageFile)

    return render_template('select_template.html', title='Make a Meme', img_html = img_templates)


#makeMeme Route
@app.route("/makeMeme/<int:img_id>", methods=['GET', 'POST'])
def makeMeme(img_id):
    img = Image.query.filter_by(id=img_id).first()

    form = TextInsertForm()


    return render_template('make_meme.html', title="Make a Meme", img_html = img, form=form)









if __name__ == '__main__':
    app.run(debug=True)