from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
import os

"GEEN IDEE WAT DIT STUK HIERONDER DOET (BEGIN)"
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")
"GEEN IDEE WAT DIT STUK HIERONDER DOET (EINDE)"

@app.route("/login", methods=["GET", "POST"])
def login():
    "HIER LOGT DE USER IN"

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = select_username()

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        user_id(request.form.get("username"))

        # redirect user to home page
        return render_template("index.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    "HIER REGRISTREERT DE USER HET ACCOUNT"
     # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        # ensure password check was submitted
        elif not request.form.get("password_check"):
            return apology("must provide password check")
        # ensure passwords match
        elif request.form.get("password_check") != request.form.get("password"):
            return apology("passwords must match")

        # querry database for username
        rows = select_username()

        # ensure username exists and password is correct
        if rows == None:
            return apology("invalid username and/or password")

        # add user to database
        add_user()

        # redirect user to home page
        return render_template("login.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    "HIER LOGT DE USER UIT"

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/userpage", methods = ["GET", "POST"])
@login_required
def userpage():
    user_id = request.form.get("user_id")
    username = get_username(user_id)

    if request.method == "POST":
        # Volgen van andere gebruiker
        if request.form.get("follow") == "yes":
            if(follow(user_id) == "Already following"):
                return apology("You are alraedy following this account")

        # Ontvolgen van andere gebruiker
        elif request.form.get("unfollow") == "yes":
            if(unfollow(user_id) == "Not following"):
                return apology("You are not following this account")
        followers_following = following_follower(user_id)
        following = followers_following[0]
        followers = followers_following[1]
        return render_template("userpage.html", user_id = user_id, username = username, following_amount = len(followers), follower_amount = len(following))
    else:
        return render_template("userpage.html", users_id = user_id, username = username)


# meer info over de werking: https://medium.com/@antoinegrandiere/image-upload-and-moderation-with-python-and-flask-e7585f43828a
# hier naar kijken alsjeblieft
# het werkt bijna
UPLOAD_FOLDER = os.path.basename('/static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/upload", methods = ["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(f)

        return render_template("index.html")
    else:
        return render_template("upload.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    picture_info = picture()
    user_id = picture_info[0]["id"]
    photo_path = picture_info[0]["photo_path"]
    old_rating = picture_info[0]["rating"]
    username = get_username(user_id)

    if request.method == "POST":

        if(request.form.get("go_to_user")) != None:
            return render_template("userpage.html", user_id = user_id, username = user_username)

        rating = int(request.form.get("rate"))
        rate(rating, picture_info)

        return render_template("index.html", photo_path = photo_path, rating = round(old_rating, 1), username = username, user_id = user_id)
    else:
        return render_template("index.html", photo_path = photo_path, rating = round(old_rating, 1))

@app.route("/userpage", methods = ["GET", "POST"])
@login_required
def search_user():

    if request.method == "POST":
        if not request.form.get("search_username"):
            return apology("must provide a username to search")

        user = search()
        user_id = user[0]["id"]
        user_username = user[0]["username"]

        if len(user) == 0:
            return apology("user does not exist")

        return render_template("userpage.html", user_id = user_id, user_username = user_username)

    else:
        return render_template("userpage.html")
