from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,RadioField,DateField,SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired,EqualTo


class clsignup(FlaskForm):
    username = StringField("User Name")
    firstname = StringField("First Name")
    lastname = StringField("Last Name") #currently not using
    email = EmailField("Email Id",validators=[DataRequired()])
    password = PasswordField("Password",validators=[EqualTo('confirmpassword')])
    confirmpassword = PasswordField("Confirm Password",validators=[DataRequired()])
    ageo18 = BooleanField("Confirm your age is over 18 years")
    submit = SubmitField("Submit")

class clslogin(FlaskForm):
    username = StringField("User Name")
    password = PasswordField("Password")
    login = SubmitField("Login")

class clsspongesignup(FlaskForm):
    sfirstname = StringField("First Name")
    smiddlename = StringField("Middle Name")
    slastname = StringField("Last Name")
    sdob = StringField("Date of Birth")
    sgender = SelectField('Gender', choices=[('',''),('F','Female'),('M','Male'),('O','Other')])
    semail = EmailField("Email Id")
    susername = StringField("User Name")
    spassword = PasswordField("Password",validators=[EqualTo('sconfirmpassword')])
    sconfirmpassword = PasswordField("Confirm Password",validators=[DataRequired()])
    ssubmit = SubmitField("Submit")


class clsspongelogin(FlaskForm):
    susername = StringField("User Name")
    spassword = PasswordField("Password")
    slogin = SubmitField("Login")
