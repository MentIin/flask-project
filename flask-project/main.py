from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, \
    SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed
from data import db_session
from data.users import User
from data.posts import Post
from data.likes import Likes
from flask_login import *
import os
import datetime
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aba43urg4d78g2983g_key'

app.debug = True
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


@app.route("/", methods=['GET'])
@app.route("/main", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    page = request.args.get("page")
    if page.isnumeric():
        page = int(page)
    else:
        page = 1

    db_sess = db_session.create_session()
    posts = list(db_sess.query(Post).filter())
    posts.sort(key=lambda x: x.create_time, reverse=True)

    posts_data = []
    for post in posts:
        post: Post
        d = {}
        d["title"] = post.title
        d["img"] = post.image_path
        d["likes"] = post.liked
        posts_data.append(d)

    print(posts_data)

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
        file = avatar
        current_time = datetime.datetime.now()
        path = Path("static", "avatars")
        folder = str(current_time.date())
        filename = str(current_user.id) \
                   + str(current_time.time()).replace(":", "-").replace(".", "-") \
                   + ".png"
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)

        # сохраняем файл
        path = Path("static", "avatars", folder)
        if not os.path.exists(path):
            os.makedirs(path)
        file.save(os.path.join(path, filename))

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.avatar_im_path = os.path.join(folder, filename)
        db_sess.commit()
        return redirect(request.url)

    if current_user.is_authenticated:
        last_page = request.args.get("last_page")
        avatar_path = Path("static", "avatars", current_user.avatar_im_path)
        return render_template("profile.html", avatar=avatar_path,
                               last_page=last_page, title="Профиль " + current_user.login)
    else:
        return redirect("/login")


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    form = CreatePostForm(request.form)
    if request.method == "POST":
        if len(form.text.data) > 0 or len(form.image.data) > 0:
            db_sess = db_session.create_session()
            post = Post()
            post.user_id = current_user.id
            post.title = form.text.data
            db_sess.add(post)
            db_sess.commit()
            return render_template("create_post.html", title="Создать публикацию",
                                   form=form, message="Успешно")
    if form.validate_on_submit():
        flash('Success')
        for i in range(10 ** 10):
            print(1)
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
    form = RegistrationForm()
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
