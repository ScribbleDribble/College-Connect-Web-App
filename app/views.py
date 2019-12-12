from flask import render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, LoginManager, login_required, login_manager
from app import app, db, tasks
from .forms import LoginForm, RegisterForm, ChangePasswordForm, PostForm, FindUserForm, MessageForm
from .models import User, Posts, Message, friends
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timezone, datetime

import logging

# in order to make sure users cant access pages unless logged in
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Posts, db.session))
admin.add_view(ModelView(Message, db.session))




@app.route('/login', methods=['GET', 'POST'])
def login():
    css_file = 'css/login.css'

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # will return None if username doesn't exist. good for querying one result
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password, form.password.data):
            flash('Invalid username or password')
            logging.warning('test')
            return redirect(url_for('login'))

        login_user(user)

        return redirect(url_for('index'))

    return render_template('login.html', form=form, css_file=css_file)


@app.route('/register', methods=['GET', 'POST'])
def register():

    css_file = 'css/register.css'

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        # check if email and username are taken. redirect if so
        if not User.query.filter_by(email=form.email.data).first() is None and not User.query.filter_by(username=form.username.data) is None:
            redirect(url_for('register'))

        u = User(id=User.query.count() + 1, username=form.username.data, name=form.name.data, email=form.email.data,
                 age=form.age.data, university=form.university.data, course=form.course.data,
                 password=(generate_password_hash(form.password.data)))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form, css_file=css_file)


@app.route('/logout')
@login_required
def logout():
    # assume moderator has
    if current_user.is_moderator:
        logging.warning(f'Moderator {current_user.id} has logged out')

    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():


    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    logging.basicConfig(filename='logs.txt', filemode='w',
                        format='%(asctime)s - %(message)s - %(levelname)s', datefmt='%d-%b-%y %H:%M:%S')

    logging.info(f' {current_user.username} has logged in')

    css_file = 'css/index.css'

    # get data of users friends in a list format

    posts = []

    for friend in current_user.connections:
        posts = posts + Posts.query.filter_by(sender_id=friend.id).all()

    # friend_objs = friends.query.filter_by(friend_id=current_user.id).all()
    # friend_objs = friend_objs + friends.query.filter_by(id=current_user.id).all()

    # the data contained within each post
    # posts = []
    # try:
    #     for friend_obj in friend_objs:
    #
    #         # friend_ids can come under the 'friend_id' or 'id' fields so query for both
    #         if not friend_obj.id == current_user.id:
    #             posts = posts + Posts.query.filter_by(sender_id=friend_obj.id).all()
    #
    #         else:
    #             posts = posts + Posts.query.filter_by(sender_id=friend_obj.friend_id).all()

    # except Exception:
    #     print("no more posts")

    post_segments = []

    for post in posts:
        post_segments.append((User.query.filter_by(id=post.sender_id).first().name, post.message, post.date))

    form = PostForm()
    if form.validate_on_submit():
        p = Posts(id=Posts.query.count() + 1, sender_id=current_user.id,
                  date=datetime.now(timezone.utc), message=form.message.data)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', current_user=current_user, form=form,
                           post_segments=post_segments, css_file=css_file)


@app.route('/add_friend', methods=['GET', 'POST'])
@login_required
def add_friend():
    form = FindUserForm()
    form.password = None

    if form.validate_on_submit():
        friend = User.query.filter_by(username=form.username.data).first()
        if friend is None:
            flash("User was not found")
            return redirect(url_for('add_friend'))

        current_user.connections.append(friend)
        friend.connections.append(current_user)
        # print(current_user.connections)
        # print(friend.connections)
        db.session.commit()
        flash("You are now friends with " + friend.name)
        return redirect(url_for('add_friend'))

    return render_template('add_friend.html', form=form)


@app.route('/message', methods=['GET', 'POST'])
def message():

    messages = Message.query.filter_by(uid_receiver=current_user.id).all()

    form = MessageForm()
    if form.validate_on_submit():

        # parse input and iterate through each user, message them if they exist
        for username in form.username.data.split(','):
            receiver = User.query.filter_by(username=username).first()
            if receiver is None:
                flash(username + ' was not found')
                return redirect(url_for('message'))

            # each user will be sent a message via a background task
            tasks.send_messages(current_user, receiver, form.message.data)
        flash('Message(s) sent')
        return redirect(url_for('message'))

    return render_template('message.html', form=form, messages=messages)


@app.route('/options', methods=['GET', 'POST', 'DELETE'])
@login_required
def options():
    form = ChangePasswordForm()

    delete_form = FindUserForm()


    if form.validate_on_submit():
        try:
            if check_password_hash(current_user.password, form.old_password.data):
                if form.new_password.data == form.new_password2.data:
                    # generate new hash code for user password
                    current_user.password = generate_password_hash(form.new_password.data)
                    db.session.add(current_user)
                    db.session.commit()
                    flash('Password change successful')
                    return redirect(url_for('options'))

                else:
                    flash('Either password entered was wrong or new passwords dont match')
                    return redirect(url_for('options'))


        except Exception as e:
            # instances when users are created via rdbms and no password hashing has been used or some other reason
            logging.error('User password and potentially other information are not encrypted.', exc_info=True)


    if delete_form.validate_on_submit():
        print("here")
        u = User.query.filter_by(username=delete_form.username.data).first()

        if u is None:
            flash(f'User with user id {u.id} does not exist')
            return redirect(url_for('options'))

        if u.is_moderator:
            logging.error(f'Moderator {current_user.id} attempted to delete moderator {u.id}')
            flash('Permission denied')
            return redirect(url_for('options'))

        return redirect(url_for('deleteUser', id=u.id))

    return render_template('options.html', current_user=current_user, form=form, delete_form=delete_form)

@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
@login_required
def deleteUser(id):
    if not current_user.is_moderator:
        logging.critical(f' User {current_user.username} with id: {current_user.id} attempted delete operation '
                         f'without moderator level access')
        return redirect(url_for('login'))

    u = User.query.filter_by(id=id).first()
    print(u)
    db.session.delete(u)
    db.session.commit()

    flash('User has been successful been terminated')
    logging.warning(f'Moderator {current_user.username} has deleted user {id}')

    return redirect(url_for('options'))


@app.route('/<string:username>', methods=['GET', 'POST'])
def profile(username):

    return render_template('profile.html')