import datetime
import os
from pathlib import Path
from waitress import serve

from flask import Flask, render_template, request, redirect, flash
from flask_login import *

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, \
    SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired

from data import db_session
from data.posts import Post
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aba43urg4d78g2983g_key'

# app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init(f"db/nedogram.sqlite")


class LoginForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Создать аккаунт')


class CreatePostForm(FlaskForm):
    text = TextAreaField('text', validators=[])
    image = FileField("image", validators=[FileAllowed(["png", "jpg", "bmp"], "Image only")])
    # image = FileField("image", validators=[])
    submit = SubmitField('Опубликовать')


def save_image(image, folder="avatars"):
    file = image
    current_time = datetime.datetime.now()
    path = Path("static", folder)  # static чтобы браузер не ругался
    date_folder = str(current_time.date())
    filename = str(current_user.id) \
               + str(current_time.time()).replace(":", "-").replace(".", "-") \
               + ".png"

    # сохраняем файл
    path = Path("static", folder, date_folder)
    if not os.path.exists(path):
        os.makedirs(path)
    file.save(os.path.join(path, filename))
    return os.path.join(date_folder, filename)


def save_avatar(image):
    return save_image(image, folder="avatars")


def save_post_image(image):
    return save_image(image, folder="post-images")


@app.route("/", methods=['GET'])
@app.route("/main", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    page = request.args.get("page")
    if page:
        if page.isnumeric():
            page = int(page)
        else:
            page = 1
    else:
        page = 1

    db_sess = db_session.create_session()
    n = 4
    posts = list(db_sess.query(Post).filter(Post.is_deleted == False))
    posts.sort(key=lambda x: x.create_time, reverse=True)
    posts = posts[(page - 1) * n:(page) * n]

    posts_data = []
    for post in posts:
        post: Post

        d = {}
        d["id"] = post.id
        d["title"] = post.title
        if post.image_path:
            img_path = Path("static", "post-images", post.image_path)
            d["img"] = img_path
            d["has_image"] = True
        else:
            d["has_image"] = False

        d["likes"] = len(post.liked)

        d["author_login"] = post.user.login
        avatar_path = post.user.get_avatar_full_path()
        d["author_avatar"] = avatar_path

        posts_data.append(d)
    posts_json = {}
    posts_json["posts"] = posts_data
    return render_template("index.html", posts=posts_json, page=page, title="Главная")


@app.route("/profile", methods=['GET', "POST"])
def profile():
    if request.method == "POST":
        avatar = request.files["avatar"]
    else:
        avatar = None

    if avatar:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.avatar_im_path = save_avatar(avatar)
        db_sess.commit()
        return redirect(request.url)

    if current_user.is_authenticated:
        last_page = request.args.get("last_page")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        avatar_path = user.get_avatar_full_path()
        return render_template("profile.html", avatar=avatar_path,
                               last_page=last_page, title="Профиль " + current_user.login)
    else:
        return redirect("/login")


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == "POST":
        image = request.files["post_im"]
    else:
        image = None

    if request.method == "POST":
        if len(form.text.data) > 0 or image:
            db_sess = db_session.create_session()
            post = Post()
            post.user_id = current_user.id
            post.title = form.text.data
            db_sess.add(post)
            if image:
                post.image_path = save_post_image(image)
                db_sess.commit()

            db_sess.commit()

            flash('Success')
            return redirect("/profile")
    return render_template("create_post.html", title="Создать публикацию",
                           form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form, title="Вход")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()  # надо зашифровать пароль!
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user_with_same_login = db_sess.query(User).filter(User.login == form.login.data).first()

        if not user_with_same_login:
            if form.password.data == form.confirm_password.data:
                user.login = form.login.data
                user.password = form.password.data
                db_sess.add(user)
                db_sess.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            else:
                return render_template('registration.html',
                                       message="Пароли не совпадают",
                                       form=form)
        else:
            return render_template('registration.html',
                                   message="Пользователь с таким логином уже существует",
                                   form=form)
    return render_template('registration.html', form=form, title="Регистрация")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


prodaction = False
if __name__ == '__main__':
    if prodaction:
        serve(app, port=8080, host='127.0.0.1')
    else:
        app.run(port=8080, host='127.0.0.1')
