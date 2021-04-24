#Author:                Trevor Strobel
#Date:                  4/22/21

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Optional


# Meme text form 
class TextInsertForm(FlaskForm):
    #fields
    topText = StringField('Top Text', validators=[Length(max=20)])
    bottomText = StringField('Bottom Text', validators=[Length(max=20)])
    
    #buttons
    submit = SubmitField('Submit')