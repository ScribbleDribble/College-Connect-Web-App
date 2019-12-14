from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email
from flask_login import current_user



def validate_age(form, field):
    if field.data < 13:
        raise ValidationError("Invalid age")

def validate_string_length1(form, field):
    if len(field.data) > 15 :
        raise ValidationError('Maximum character length 15')

def validate_string_length2(form, field):
    if len(field.data) > 30 :
        raise ValidationError('Maximum character length 30')

class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    # submit = SubmitField('Sign In')

class RegisterForm(Form):
    name = StringField(validators=[DataRequired(), validate_string_length1])
    username = StringField(validators=[DataRequired(), validate_string_length1])
    email = StringField(validators=[DataRequired(), Email(), validate_string_length2])
    age = IntegerField("e.g. 18", validators=[DataRequired(), validate_age])
    university = StringField(validators=[DataRequired(), validate_string_length1])
    course = SelectField('Course', choices=[('Accounting', 'Accounting'), ('Computer Science', 'Computer Science'),
                                            ('Economics', 'Economics'), ('Geology', 'Geology'), ('German', 'German'),
                                            ('Law', 'Law'), ('Medicine', 'Medicine'), ('Physics', 'Physics')])
    password = PasswordField(validators=[DataRequired()])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])
    new_password2 = PasswordField(validators=[DataRequired()])

class PostForm(Form):
    message = StringField(validators=[DataRequired()])

class FindUserForm(Form):
    username = StringField(validators=[DataRequired()])

class MessageForm(Form):
    username = StringField(validators=[DataRequired()])
    message = StringField(validators=[DataRequired()])


