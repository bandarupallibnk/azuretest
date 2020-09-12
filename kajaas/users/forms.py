from flask import Flask
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,FileField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,EqualTo,length

class clsupload(FlaskForm):
    aboutaudio = TextAreaField("About you:",validators=[length(max=20)])
    audio = FileField("Audio:")
    upload = SubmitField("Upload")
