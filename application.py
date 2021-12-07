import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, abort, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length
from flask_session import Session
import flask_login
import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
Session(app)
app.config['UPLOAD_PATH'] = 'static/image_uploads'
conn = sqlite3.connect("games.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'test': {'password': '123'}}



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


@app.route('/remove', methods=['GET', 'POST'])
@flask_login.login_required
def remove():
    form = RemoveForm()
    if request.method == "POST":
        game = request.form.get("game_select")
        if game == None:
            flash('No game was removed', 'danger')
        else:
            with closing(conn.cursor()) as c:
                query_filename = f"SELECT image_filename from games where game_name = ?"
                c.execute(query_filename, (game,))
                file_name = c.fetchone()
                try:
                    os.remove(os.path.join(app.config['UPLOAD_PATH'], file_name[0]))
                    flash('Game image deleted from server', 'success')
                except Exception:
                    flash('Could not delete file', 'danger')
                query_delete = f"DELETE from games where game_name = ?"
                c.execute(query_delete, (game,))
                conn.commit()
                flash('Game removed successfully from database and collection', 'success')
                return redirect(url_for('remove'))
    return render_template('remove.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    email = request.form['email']
    if email in users:
        if request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            flash('Login successful. Welcome to the game display web app!', 'success')
            return redirect(url_for('index'))
    else:
        flash('Login Unsuccessful. Please try logging in again', 'danger')
    return render_template('login.html', form=form)

# @app.route('/home', methods=['GET', 'POST'])
# @flask_login.login_required
# def home():
#     return render_template('home.html')


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
@flask_login.login_required
def logout():
    if flask_login.current_user.is_authenticated:
        flask_login.logout_user()
    return render_template('logout.html')

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'


class GameForm(FlaskForm):
    game_name = StringField("Enter the game name:", [Length(min=1)])
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
    submit = SubmitField('Login')

class RemoveForm(FlaskForm):
    game_select = SelectField("Choose a game to remove:")
    submit = SubmitField("Submit")
    def __init__(self, *args, **kwargs):
        super(RemoveForm, self).__init__(*args, **kwargs)
        with closing(conn.cursor()) as c:
            query = f"SELECT game_name from games"
            c.execute(query)
            game_names = c.fetchall()
        self.game_select.choices = [(name["game_name"],name["game_name"]) for name in game_names]

@app.route("/")
@flask_login.login_required
def index():
    return render_template("index.html")

@app.route("/upload")
@flask_login.login_required
def upload():
    form = GameForm()
    if form.validate_on_submit():
        form.name.data= ''
    return render_template("upload.html", form=form)

@app.route("/submitted", methods=["GET","POST"])
@flask_login.login_required
def submission():
    game_name = request.form.get("game_name")
    game_developer = request.form.get("game_developer")
    console = request.form.get("console")
    release_year = request.form.get("release_year")
    game_description = request.form.get("game_description")
    image_caption = request.form.get("image_caption")
    score = request.form.get("scoreRating")
    if request.method == "POST":
        if request.files:
            image_file = request.files['image_file']
            image_file.save(os.path.join(app.config['UPLOAD_PATH'], image_file.filename))
            image_filename = image_file.filename
        with closing(conn.cursor()) as c:
            query = f"INSERT into games(image_filename, image_caption, game_name, console, release_year, game_description,developer, score_rating) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
            c.execute(query, (image_filename, image_caption, game_name, console, release_year, game_description, game_developer,score))
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




