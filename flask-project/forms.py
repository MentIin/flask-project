from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import EmailField, PasswordField, BooleanField, \
    SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


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
