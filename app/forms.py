from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired()])
    submit = SubmitField('Sign In')

