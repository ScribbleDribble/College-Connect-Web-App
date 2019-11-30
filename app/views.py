from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user
from app import app, db
from .forms import LoginForm
from .models import User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.html'))

    form = LoginForm()
    if form.validate_on_submit():
        # will return None if username doesn't exist. good for querying one result
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not User.check_password(user.password):
            flash('Incorrect username or password')
            return redirect(url_for('/login'))

        login_user(user)
        redirect(url_for('index.html'))

    return render_template('login.html', form=form)

@app.route('/')
def index():
    render_template('index.html')