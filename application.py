import sqlite3
from flask import Flask, render_template, redirect, request, abort
import os

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/images'
conn = sqlite3.connect("games.db", check_same_thread=False)

# SCORES =["1","2","3","4","5"]
SCORES =[1,2,3,4,5]


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/upload")
def upload():
    return render_template("upload.html",scores=SCORES)


@app.route("/submitted", methods=["POST"])
def collection():
    if not request.form.get("game_name") or not request.form.get("score") not in SCORES:
        return render_template("unsuccessful.html")
    return render_template("submitted.html", game_name=request.form.get("game_name"))


