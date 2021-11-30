import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, abort, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired
from flask_session import Session
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)
app.config['UPLOAD_PATH'] = 'static/images'
conn = sqlite3.connect("games_test.db", check_same_thread=False)

SCORES =["1","2","3","4","5"]

class GameForm(FlaskForm):
    game_name = StringField("Enter the game name:", validators=[DataRequired()])
    game_developer = StringField("Enter the developer name:", validators=[DataRequired()])
    console = StringField("Enter the console name:", validators=[DataRequired()])
    release_year = IntegerField("Enter a release year:", validators=[DataRequired()])
    image_file = FileField("Upload the game cover: ")
    game_description = StringField("Enter a brief description of the game: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/upload")
def upload():
    name = None
    form = GameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data= ''
    return render_template("upload.html", name=name, form=form)



@app.route("/submitted", methods=["POST"])
def submission():
    game_name = request.form.get("game_name")
    if not game_name:
        return render_template("error.html", error_message="You must enter a game name")
    score = request.form.get("scoreRating")
    if score not in SCORES:
        return render_template("error.html", error_message="You must enter a score")
    with closing(conn.cursor()) as c:
        query = f"INSERT into games(game_name, score_rating) VALUES(?, ?)"
        c.execute(query, (game_name, score))
        conn.commit()
    return redirect("/collection")

@app.route("/collection")
def collection():
    with closing(conn.cursor()) as c:
        query = f"SELECT * from games"
        c.execute(query)
        game_collection = c.fetchall()
    return render_template("collection.html", game_collection=game_collection)




