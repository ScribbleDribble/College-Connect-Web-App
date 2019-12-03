from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email


def validate_age(form, field):
    if field.data < 13:
        raise ValidationError("Invalid age")

class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    # submit = SubmitField('Sign In')

class RegisterForm(Form):
    name = StringField(validators=[DataRequired()])
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    age = IntegerField("e.g. 18", validators=[DataRequired(), validate_age])
    university = StringField(validators=[DataRequired()])
    course = SelectField('Course', choices=[('Accounting', 'Accounting'), ('Computer Science', 'Computer Science'),
                                            ('Economics', 'Economics'), ('Geology', 'Geology'), ('German', 'German'),
                                            ('Law', 'Law'), ('Medicine', 'Medicine'), ('Physics', 'Physics')])
    password = PasswordField(validators=[DataRequired()])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])
    new_password2 = PasswordField(validators=[DataRequired()])
