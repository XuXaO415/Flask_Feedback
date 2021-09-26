from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import TextAreaField
from wtforms import validators
from wtforms.validators import Email, InputRequired, Optional, Email

# https: //wtforms.readthedocs.io/en/2.3.x/fields/

class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    
    


class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback form"""
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])