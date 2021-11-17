import sqlite3
from flask import Flask, render_template, redirect, request, abort
import os

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/images'
conn = sqlite3.connect("games.db", check_same_thread=False)


@app.route("/")
def index():
    return render_template("index.html")

