#Author:                Trevor Strobel


from flask import request, render_template, flash, redirect, url_for
from mememaker import app, db
from mememaker.models import Img, Meme
from mememaker.forms import *
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import base64
import os



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

    img_templates = Img.query.with_entities(Img.id, Img.imageName, Img.imageFile)

    return render_template('select_template.html', title='Make a Meme', img_html = img_templates)


#makeMeme Route
@app.route("/makeMeme/<int:img_id>", methods=['GET', 'POST'])
def makeMeme(img_id):
    img = Img.query.filter_by(id=img_id).first()

    form = TextInsertForm()

    if form.validate_on_submit():

        topText = form.topText.data
        bottomText = form.bottomText.data

        imgData = img.imageFile[22:]

        img = Image.open(BytesIO(base64.b64decode(imgData))) #converts the image to a png image format.

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("mememaker/static/Gidole-Regular.ttf", size=72)

        

        #for positioning purposes.
        W,H = img.size
        w1,h1 = draw.textsize(topText, font=font)  
        w2,h2 = draw.textsize(bottomText, font=font)        

        draw.text(((W-w1)/2, (H/20)), topText, fill=(255,255,255), font=font)
        draw.text(((W-w2)/2 ,(H-h2-30)), bottomText, fill=(255,255,255), font=font)
        
        buffered = BytesIO()
        img.save(buffered, format='PNG')

        

        img = base64.b64encode(buffered.getvalue())
        img = 'data:image/png;base64,' + str(img.decode('utf-8'))

        meme = Meme(imageFile=img, topText=topText, bottomText =bottomText)


        img = meme
        








    return render_template('make_meme.html', title="Make a Meme", img_html = img, form=form)









if __name__ == '__main__':
    app.run(debug=True)