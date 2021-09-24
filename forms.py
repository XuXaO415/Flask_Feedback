from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms import validators
from wtforms.validators import Email, InputRequired, Email

# https: //wtforms.readthedocs.io/en/2.3.x/fields/

class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email Address", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form"""

