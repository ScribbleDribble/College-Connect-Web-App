from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, LoginManager, login_required, login_manager
from app import app, db
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PostForm, FindFriendForm
from .models import User, Posts, Friends
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timezone, datetime

# in order to make sure users cant access pages unless logged in
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Friends, db.session))
admin.add_view(ModelView(Posts, db.session))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # will return None if username doesn't exist. good for querying one result
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            return redirect(url_for('login'))

        login_user(user)

        return redirect(url_for('index'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # check if email and username are taken. redirect if so
        if not User.query.filter_by(email=form.email.data).first() is None and not User.query.filter_by(username=form.username.data) is None:
            redirect(url_for('register'))

        u = User(id=User.query.count() + 1, username=form.username.data, name=form.name.data, email=form.email.data, age=form.age.data,
                 university=form.university.data, course=form.course.data,
                 password=(generate_password_hash(form.password.data)))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    css_file = 'css/index.css'

    # get data of users friends in a list format
    friend_objs = Friends.query.filter_by(friend_id=current_user.id).all()
    friend_objs = friend_objs + Friends.query.filter_by(id=current_user.id).all()
    print(friend_objs)

    # the data contained within each post
    posts = []
    try:
        for friend_obj in friend_objs:

            # friend_ids can come under the 'friend_id' or 'id' fields so query for both
            if not friend_obj.id == current_user.id:
                posts = posts + Posts.query.filter_by(sender_id=friend_obj.id).all()

            else:
                posts = posts + Posts.query.filter_by(sender_id=friend_obj.friend_id).all()

    except (Exception):
        print("no more posts")

    post_segments = []

    for post in posts:
        post_segments.append((User.query.filter_by(id=post.sender_id).first().name, post.message, post.date))

    form = PostForm()
    if form.validate_on_submit():
        p = Posts(id=Posts.query.count() + 1, sender_id=current_user.id, date=datetime.now(timezone.utc), message=form.message.data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', current_user=current_user, form=form, post_segments=post_segments, css_file=css_file)

@app.route('/add_friend', methods=['GET', 'POST'])
@login_required
def add_friend():
    form = FindFriendForm()
    form.password = None

    if form.validate_on_submit():
        friend = User.query.filter_by(username=form.username.data).first()
        if friend is None:
            flash("User was not found")
            return redirect(url_for('add_friend'))

        f = Friends(id=current_user.id, friend_id=friend.id)
        db.session.add(f)
        db.session.commit()
        flash("You are now friends with" + friend.username)
        return redirect(url_for('add_friend'))

    return render_template('add_friend.html', form=form)

@app.route('/options', methods=['GET', 'POST'])
@login_required
def options():
    form = ChangePasswordForm()

    if form.validate_on_submit():

        if check_password_hash(current_user.password, form.old_password.data):
            if form.new_password.data == form.new_password2.data:
                # generate new hash code for user password
                current_user.password = generate_password_hash(form.new_password.data)
                db.session.add(current_user)
                db.session.commit()
                return redirect(url_for('options'))

            else:
                print('Either password entered was wrong or new passwords dont match')
                return redirect(url_for('options'))

    return render_template('options.html', current_user=current_user, form=form)
