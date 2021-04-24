#Author:                Trevor Strobel
#Date:                  4/22/21

from mememaker import db


#Image model describes a meme template image in the database
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(20), unique=True, nullable = False)
    imageFile = db.Column(db.String(), nullable=False)
    memes = db.relationship('Meme', backref='img_template', lazy=True)

    def __repr__(self):
        return f"Image('{self.imageName}', '{self.imageFile}')"

#The Meme model describes a template image with top and bottom text. 
class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topText = db.Column(db.String(20))
    bottomText = db.Column(db.String(20))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)

    def __repr__(self):
        return f"Meme('{self.topText}', '{self.bottomText}')"



