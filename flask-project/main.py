from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
from data.posts import Post
from data.likes import Likes
from flask_login import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aba43urg4d78g2983g_key'
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init(f"db/nedogram.sqlite")
user = User()

class LoginForm(FlaskForm):
    login = EmailField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route("/", methods=['GET'])
@app.route("/main", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    page = request.args.get("page")
    if page:
        page = int(page)
    else:
        page = 1
    posts_list = {
        "posts": [
            {
                "title": "Сегодня хорошая погода",
                "img": "static/img/i.jpeg",
                "likes": 3
            },
            {
                "title": "Завтра хорошая погода",
                "img": "static/img/i.jpeg",
                "likes": 4
            },
            {
                "title": "Послезавтра дождь",
                "img": "static/img/i.jpeg",
                "likes": 1
            },
            {
                "title": "Цветочек",
                "img": "static/img/img.png",
                "likes": 6666
            }
        ]
    }
    return render_template("index.html", posts=posts_list, page=page)


@app.route("/profile", methods=['GET'])
def profile():
    if current_user.is_authenticated:
        last_page = request.args.get("last_page")

        return render_template("profile.html", last_page=last_page)
    else:
        return redirect("/login")


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
    return render_template('login.html', form=form)


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
