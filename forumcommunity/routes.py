
from forumcommunity import app, db, bcrypt
from forumcommunity.forms import FormLogin, FormRegister, FormEdit, FormPost
from forumcommunity.models import User, Post
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from PIL import Image


@app.route('/')
def home():
   
    return render_template('home.html')

@app.route('/forum')
@login_required
def forum():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('forum.html', posts=posts)


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_register = FormRegister()

    if form_login.validate_on_submit() and 'btn_login' in request.form:
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_login.password.data):
            login_user(user, remember=form_login.remember.data) 
            flash(" Login successful !! ", "alert-success")

            next_par = request.args.get('next')
            if next_par:
                return redirect(next_par)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login failed, incorrect email or password.', 'alert-danger')
        

    if form_register.validate_on_submit() and 'btn_register' in request.form:
        password_crypt = bcrypt.generate_password_hash(form_register.password.data)             # Hash of password
        user = User(username=form_register.username.data, email=form_register.email.data, password=password_crypt)
        db.session.add(user)
        db.session.commit()

        flash(f'Welcome {form_register.username.data}, your account has been created successfully!', "alert-success")
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_register=form_register)



@app.route('/profile')
@login_required
def profile():
    picture = url_for('static', filename=f'pictures/{current_user.profile_picture}')
    return render_template('profile.html', picture=picture)


def save_image(image):
    # Create a random code
    cod = secrets.token_hex(5)
    name, extension = os.path.splitext(image.filename)
    name_file = name + cod + extension

    path = os.path.join(app.root_path, 'static/pictures', name_file)

    # Reduce image size
    size = (200,200)
    new_image = Image.open(image)
    new_image.thumbnail(size)

    # Save Image
    new_image.save(path)
    return name_file


def update_courses(form):
    list_courses = []
    for field in form:
        if 'sk_' in field.name:
            if field.data:
                list_courses.append(field.label.text)
    return ';'.join(list_courses)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = FormEdit()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.picture.data:
             name_image = save_image(form.picture.data)
             current_user.profile_picture = name_image  
        current_user.courses = update_courses(form)
        db.session.commit()
        flash('Profile updated successfully', "alert-success")
        return redirect(url_for('profile'))
    
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    picture = url_for('static', filename=f'pictures/{current_user.profile_picture}')
    return render_template('edit.html', picture=picture, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful !!', 'alert-success')
    return redirect(url_for('home'))



@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = FormPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created successfully.', 'alert-success')
        return redirect(url_for('forum'))
    return render_template('new_post.html', form=form)


@app.route('/post/<post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('posts.html', post=post)
