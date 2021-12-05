import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, abort, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, PasswordField
from wtforms.validators import DataRequired
from flask_session import Session
import flask_login

import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)
app.config['UPLOAD_PATH'] = 'static/images'
conn = sqlite3.connect("games.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

users = {'ericstock@gmail.com': {'password': 'terminator2fan'}}

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect("/upload")

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


class GameForm(FlaskForm):
    game_name = StringField("Enter the game name:", render_kw={'style': 'width: 100%'})
    game_developer = StringField("Enter the developer name:")
    console = StringField("Enter the console name:")
    release_year = IntegerField("Enter a release year:")
    game_description = StringField("Enter a brief description of the game: ")
    image_file = FileField("Upload the game cover: ")
    image_caption = StringField("Enter a caption for the image: ")
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField('Email:')
    password = PasswordField('Password:')
    submit = SubmitField('Login:')


    # game_name = StringField("Enter the game name:", validators=[DataRequired()],  render_kw={'style': 'width: 100%'})
    # game_developer = StringField("Enter the developer name:", validators=[DataRequired()])
    # console = StringField("Enter the console name:", validators=[DataRequired()])
    # release_year = IntegerField("Enter a release year:", validators=[DataRequired()])
    # game_description = StringField("Enter a brief description of the game: ", validators=[DataRequired()])
    # image_file = FileField("Upload the game cover: ")
    # image_caption = StringField("Enter a caption for the image: ", validators=[DataRequired()])
    # submit = SubmitField("Submit")


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")

# @app.route("/login", methods=["GET","POST"])
# def login():
#     form = LoginForm()
#     if request.method == "POST":
#         if request.form.get("email").lower() == "ericstock@gmail.com" and request.form.get("password") == "terminator2fan":
#             session["email"] = request.form.get("email")
#             return redirect("/")
#     return render_template("login.html", form=form)

# @app.route("/logout")
# def logout():
#     session["name"] = None
#     return redirect("/")

@app.route("/upload")
@flask_login.login_required
def upload():
    name = None
    form = GameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data= ''
    return render_template("upload.html", name=name, form=form)

# @app.route("/upload")
# def upload():
#     form = GameForm()
#     return render_template("upload.html", form=form)



@app.route("/submitted", methods=["GET","POST"])
@flask_login.login_required
def submission():
    game_name = request.form.get("game_name")
    game_developer = request.form.get("game_developer")
    console = request.form.get("console")
    release_year = request.form.get("release_year")
    game_description = request.form.get("game_description")
    image_file = request.form.get("image_file")
    image_caption = request.form.get("image_caption")
    score = request.form.get("scoreRating")
    # if not game_name:
    #     return render_template("error.html", error_message="You must enter a game name")
    # score = request.form.get("scoreRating")
    # if score not in SCORES:
    #     return render_template("error.html", error_message="You must enter a score")
    with closing(conn.cursor()) as c:
        query = f"INSERT into games(image_filename, image_caption, game_name, console, release_year, game_description,developer, score_rating) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(query, (image_file, image_caption, game_name, console, release_year, game_description, game_developer,score))
        conn.commit()
    return redirect("/collection")

@app.route("/collection")
@flask_login.login_required
def collection():
    with closing(conn.cursor()) as c:
        query = f"SELECT * from games"
        c.execute(query)
        game_collection = c.fetchall()
    return render_template("collection.html", game_collection=game_collection)




