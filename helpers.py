import csv
import urllib.request
import random

from functools import wraps
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *

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

def apology(message, code=400):
    "returned een excuus als de user een veld leeg of niet correct invult"
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def user_id(username):
    # gebruiker ophalen uit de database
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    # Id van de gebruiker opslaan
    session["user_id"] = rows[0]["id"]


def login_required(f):
    "zorgt ervoor dat een user eers moet inloggen alvorens een actie uit te voeren"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def add_user():
    result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))

    # ensure that username is not already in use
    if not result:
        return apology("username already in use")

    return result

def get_username(user_id):
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id = user_id)
    return username[0]["username"]

def select_username():
    return db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

def post():
    "deze functie zorgt ervoor dat gebruikers foto's kunnen uploaden"
    return apology("pagina is nog niet af")

def rate(rating, picture_info):

    photo = picture_info
    rated_amount = photo[0]["rated"]

    old_rating = photo[0]["rating"]
    new_rating = (old_rating * rated_amount + rating) /(rated_amount + 1)
    photo_id = photo[0]["photo_id"]

    db.execute("UPDATE photo SET rating = :rating, rated = :rated WHERE photo_id = :photo_id"
                        , rating = new_rating, rated = rated_amount + 1, photo_id = photo_id)

def picture():
    photo = db.execute("SELECT * FROM photo ORDER BY RANDOM() LIMIT 1")
    return photo

def follow(user_to_follow):
    "deze functie zorgt ervoor dat een user mensen kan volgen"
    user = session["user_id"]
    username_to_follow = db.execute("SELECT username FROM users WHERE id = :user_to_follow", user_to_follow = user_to_follow)
    username_user = db.execute("SELECT username FROM users WHERE id = :user", user = user)

    check = db.execute("SELECT * FROM following WHERE id = :user AND following_id = :user_to_follow", user = user, user_to_follow = user_to_follow)
    if check:
        check = "Already following"
        return check

    db.execute("INSERT INTO following (id, following_id, following_username) VALUES(:id, :following_id, :following_username)", id = user, following_id = user_to_follow, following_username = username_user[0]["username"])
    return db.execute("INSERT INTO followers (id, follower_id, follower_username) VALUES(:id, :follower_id, :follower_username)", id = user_to_follow, follower_id = user, follower_username = username_to_follow[0]["username"])

def unfollow(user_to_unfollow):
    "deze functie zorgt ervoor dat een user mensen kan onvolgen"
    user = session["user_id"]

    db.execute("SELECT username FROM users WHERE id = :user", user = user)

    check = db.execute("SELECT * FROM following WHERE id = :user AND following_id = :user_to_unfollow", user = user, user_to_unfollow = user_to_unfollow)
    if not check:
        check = "Not following"
        return check

    db.execute("DELETE FROM following WHERE id = :id AND following_id = :following_id", id = user, following_id = user_to_unfollow)
    return db.execute("DELETE FROM followers WHERE id = :id AND follower_id = :follower_id", id = user_to_unfollow, follower_id = user)

def following_follower(user_id):
    follower_following = []
    follower_following += [db.execute("SELECT follower_username FROM followers WHERE id = :id", id = user_id)]
    follower_following += [db.execute("SELECT following_username FROM following WHERE id = :id", id = user_id)]
    return follower_following

def get_pictures(user_id):
    return db.execute("SELECT * FROM photo WHERE id = :user_id", user_id = user_id)



def add_comment(comment, picture_info):
    photo = picture_info[0]["photo_id"]
    comment = comment
    return db.execute("INSERT INTO comments(photo_id, comments) VALUES(:photo_id, :comments)",photo_id = photo,comments = comment)

def show_comments(photo_id):
    comments = db.execute("SELECT * FROM (SELECT * FROM comments WHERE photo_id = :photo_id ORDER BY time DESC LIMIT 3) t ORDER BY time ASC", photo_id = photo_id)
    reversed_comments = list(reversed(comments))
    return reversed_comments
#def select_comments(picture_inf):
    #photo = picture_inf
    #select_comments = db.execute("SELECT * FROM comments WHERE photo_id = :photo_id", photo_id = photo)
    #return select_comments

def report():
    "deze fucntie zorgt ervoor dat een user een andere user kan reporten"
    return apology("pagina is nog niet af")
def sorteer():
    "deze functie zorgt ervoor dat een user zijn feed kan sorteren"
    return apology("pagina is nog niet af")


def search():
    user = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("search_username"))
    return user


def upload():
    session["user_id"] = user_id()
    add_photo = db.execute("INSERT INTO photo (id, photo_path) VALUES (:id, :photo_path)", id = session["user_id"], photo_path = "TODO")
    return add_photo