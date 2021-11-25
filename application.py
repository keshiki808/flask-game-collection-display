import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, abort, session
from flask_session import Session
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['UPLOAD_PATH'] = 'static/images'
conn = sqlite3.connect("games_test.db", check_same_thread=False)

SCORES =["1","2","3","4","5"]
# SCORES =[1,2,3,4,5]


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
    return render_template("upload.html",scores=SCORES)


@app.route("/submitted", methods=["POST"])
def submission():
    # if not request.form.get("game_name") or not request.form.get("score") not in SCORES:
    #     return render_template("error.html")
    # return render_template("submitted.html", game_name=request.form.get("game_name"))
    game_name = request.form.get("game_name")
    if not game_name:
        return render_template("error.html", error_message="You must enter a game name")
    score = request.form.get('score')
    if not score:
        return render_template("error.html", error_message="You must enter a score")
    if score not in SCORES:
        return render_template("error.html", error_message="Score must not be empty")
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




