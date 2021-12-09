import imghdr
import sqlite3
from contextlib import closing
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FileField, PasswordField, SelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, DataRequired
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from werkzeug.utils import secure_filename
import flask_login
import os

app = Flask(__name__)
csrf = CSRFProtect(app)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['UPLOAD_PATH'] = 'static/image_uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG", "JPG", "GIF", "JPEG"]
conn = sqlite3.connect("games.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
Session(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'test': {'password': '123'}}


def image_allowed_check(name_of_file):
    if not "." in name_of_file:
        return False
    extension = name_of_file.rsplit(".",1)[1]
    if extension.upper() in app.config['ALLOWED_IMAGE_EXTENSIONS']:
        return True
    else:
        return False

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')



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



class GameForm(FlaskForm):
    game_name = StringField("Enter the game name:", [Length(min=1)])
    game_developer = StringField("Enter the developer name:" )
    console = StringField("Enter the console name:")
    release_year = IntegerField("Enter a release year:")
    game_description = StringField("Enter a brief description of the game: ")
    image_file = FileField("Upload the game cover: ", validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Only images can be uploaded')
    ])
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
        # form.image_file.data
        redirect("/upload")
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
        if not game_name or not game_developer or not console or not release_year or not image_caption or score == 0:
            error = "All fields required"
            return render_template("submitted.html", error=error)
        if len(game_developer) > 50:
            error = "Game developer field must be less than 50 characters"
            return render_template("submitted.html", error=error)
        if len(console) > 50:
            error = "Console length must be less than 50"
            return render_template("submitted.html", error=error)
        if int(release_year) > 2100 or int(release_year) < 1950:
            error = "Invalid release year"
            return render_template("submitted.html", error=error)
        if len(game_name) > 50:
            error = "Game name must be less than 50 characters"
            return render_template("submitted.html", error=error)
        if len(game_description) > 200:
            error = "Game description must be less than 200 characters"
            return render_template("submitted.html", error=error)
        if len(image_caption) > 50:
            error = "Image caption must be less than 50 characters"
            return render_template("submitted.html", error=error)
        if request.files:
            image_file = request.files['image_file']
            file_ext = os.path.splitext(image_file.filename)[1]
            if image_file.filename == "":
                error = "Image must have a filename"
                return render_template("submitted.html", error=error)
            if not image_allowed_check(image_file.filename):
                error = "Invalid file extensions"
                return render_template("submitted.html", error=error)
            if file_ext != validate_image(image_file.stream):
                error = "Image content is not an image file. Please upload a valid image"
                return render_template("submitted.html", error=error)
            else:
                filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
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




