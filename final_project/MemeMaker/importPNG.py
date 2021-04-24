#Author:                    Trevor Strobel

#This script imports all png images from "image_templates" into the 
# database in the form of base-64
import glob
import os
import base64
from mememaker import db
from mememaker.models import Image


def importImages():
        
    path = 'image_templates/'

    for filename in glob.glob(os.path.join(path, '*.png')):
        with open(os.path.join(os.getcwd(), filename), 'rb') as img_file:
            imageFile = base64.b64encode(img_file.read())
            filename = filename[16:-4]
            imageFile = 'data:image/png;base64,' + str(imageFile.decode('utf-8'))
            img = Image(imageName=filename, imageFile = imageFile)
            db.session.add(img)

    db.session.commit()

# with open("image_templates/duck.png", "rb") as img_file:
#     encoded = base64.b64encode(img_file.read())
# print(encoded.decode('utf-8'))

importImages()