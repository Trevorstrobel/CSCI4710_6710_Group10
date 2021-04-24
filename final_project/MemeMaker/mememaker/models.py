#Author:                Trevor Strobel
#Date:                  4/22/21

from mememaker import db


#Image model describes a meme template image in the database
class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(20), unique=True, nullable = False)
    imageFile = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Image('{self.imageName}', '{self.imageFile}')"

#The Meme model describes a template image with top and bottom text. 
class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageName = db.Column(db.String(20), nullable = True)
    imageFile = db.Column(db.String(), nullable=False)
    topText = db.Column(db.String(20))
    bottomText = db.Column(db.String(20))

    def __repr__(self):
        return f"Meme('{self.imageName}, {self.topText}', '{self.bottomText}')"



