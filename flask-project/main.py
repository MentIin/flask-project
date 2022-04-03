from flask import Flask, render_template, request
from data import db_session
from data.users import User
from data.posts import Post

app = Flask(__name__)
app.debug = True


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
    last_page =  request.args.get("last_page")

    return render_template("profile.html", last_page=last_page)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
