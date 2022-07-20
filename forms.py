from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, TextAreaField
from wtforms.validators import InputRequired

class User_form(FlaskForm):
    user_name=TextField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])
    email=TextField('email', validators=[InputRequired()])
    f_name=TextField('First name', validators=[InputRequired()])
    l_name=TextField('Last name', validators=[InputRequired()])

class Login_form(FlaskForm):
    user_name=TextField('Username', validators=[InputRequired()])
    password=PasswordField('Password', validators=[InputRequired()])

class Feedback_form(FlaskForm):
    title=TextField('Title', validators=[InputRequired()])
    content=TextAreaField('Content', validators=[InputRequired()])