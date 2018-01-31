import csv
import urllib.request
import random
from giphypop import translate, upload
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

def apology(message):
    return render_template("apology.html", message = message)

def user_id(username):
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
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
        return apology("Username already in use!")
    return result

def get_username(user_id):
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id = user_id)
    return username[0]["username"]

def get_user_id(username):
    user_id = db.execute("SELECT id FROM users WHERE username = :username", username = username)
    return user_id[0]["id"]

def select_username(username):
    return db.execute("SELECT * FROM users WHERE username = :username", username=username)

def rate(rating, photo_id):

    photo = db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)
    rated_amount = photo[0]["rated"]

    old_rating = photo[0]["rating"]
    new_rating = (old_rating * rated_amount + rating) /(rated_amount + 1)
    photo_id = photo[0]["photo_id"]

    db.execute("UPDATE photo SET rating = :rating, rated = :rated WHERE photo_id = :photo_id", rating = new_rating, rated = rated_amount + 1, photo_id = photo_id)

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

def get_picture_info(photo_id):
    return db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

def add_comment(comment, photo_id):
    comment = comment
    return db.execute("INSERT INTO comments(photo_id, comments, username) VALUES(:photo_id, :comments, :username)",photo_id = photo_id ,comments = comment,username=get_username(session["user_id"]))

def add_gif(gif, photo_id):
    return db.execute("INSERT INTO gifs(photo_id, photo_path, username) VALUES(:photo_id, :photo_path, :username)",photo_id = photo_id ,photo_path = gif,username=get_username(session["user_id"]))

def show_gifs(photo_id):
    gifs = db.execute("SELECT * FROM (SELECT * FROM gifs WHERE photo_id = :photo_id ORDER BY time DESC LIMIT 2) t ORDER BY time ASC", photo_id = photo_id)
    reversed_gifs = list(reversed(gifs))
    return reversed_gifs

def show_comments(photo_id):
    comments = db.execute("SELECT * FROM (SELECT * FROM comments WHERE photo_id = :photo_id ORDER BY time DESC LIMIT 2) t ORDER BY time ASC", photo_id = photo_id)
    reversed_comments = list(reversed(comments))
    return reversed_comments

def featured_photos():
    featured = db.execute("SELECT * FROM(SELECT * FROM photo ORDER BY rating DESC LIMIT 10) t ORDER BY rating ASC")
    return featured

#def select_comments(picture_inf):
    #photo = picture_inf
    #select_comments = db.execute("SELECT * FROM comments WHERE photo_id = :photo_id", photo_id = photo)
    #return select_comments

def report():
    "deze fucntie zorgt ervoor dat een user een andere user kan reporten"
    return apology("Pagina is nog niet af!")

def search():
    user = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("search_username"))
    return user

def upload_photo(photo_path, caption):
    photo_path = photo_path
    add_photo = db.execute("INSERT INTO photo(id, photo_path, caption) VALUES(:id, :photo_path, :caption)", id = session["user_id"] , photo_path = photo_path, caption = caption)
    return add_photo

def upload_profile_pic(photo_path):
    photo_path = photo_path
    rows = db.execute("SELECT * FROM profile_pic WHERE id = :id", id = session["user_id"])
    if len(rows) != 0:
        db.execute("DELETE FROM profile_pic WHERE id = :id", id = session["user_id"])
        db.execute("INSERT INTO profile_pic(id, photo_path) VALUES(:id, :photo_path)", id = session["user_id"] , photo_path = photo_path)
    else:
        db.execute("INSERT INTO profile_pic(id, photo_path) VALUES(:id, :photo_path)", id = session["user_id"] , photo_path = photo_path)

def select_profile_pic(user_id):
    profile_pics = db.execute("SELECT * FROM profile_pic WHERE id = :id", id = user_id)
    if len(profile_pics) == 0:
        return "/static/profile_pic/stock.png"
    else:
        return profile_pics[0]['photo_path']

def reset_history(id):
    db.execute("DELETE FROM history WHERE id = :id", id = id)

def add_to_history(photo_id, user_id):
    db.execute("INSERT INTO history(user_id,id,photo_id) VALUES(:user_id,:id,:photo_id)", id = session["user_id"], user_id = user_id, photo_id = photo_id)

def history_check(photo_id):
    rows = db.execute("SELECT * FROM history WHERE photo_id = :photo_id AND id = :id", photo_id = photo_id, id = session["user_id"])
    if len(rows) == 0:
        return 0
    else:
        return 1

def none_left():
    history = db.execute("SELECT photo_id FROM history WHERE id = :id", id = session["user_id"])
    photo = db.execute("SELECT photo_id FROM photo WHERE id != :id", id = session["user_id"] )
    if len(photo)==len(history):
        return 1

def total_photos():
    total = db.execute("SELECT photo_id FROM photo")
    return len(total)

def report(photo_id, user_id):
    report_count = db.execute("SELECT reports FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)
    if report_count == 4:
        db.execute("DELETE * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)
    else:
        db.execute("UPDATE photo SET reports = :reports WHERE photo_id = :photo_id", reports = report_count + 1, photo_id = photo_id)

    user_report_count = db.execute("SELECT reports FROM users WHERE id = :user_id", user_id = user_id)

    if user_report_count == 14:
        db.execute("DELETE * FROM users WHERE id = :user_id", user_id = user_id)
    else:
        db.execute("UPDATE users SET reports = :reports WHERE id = :user_id", reports = user_report_count + 1, user_id = user_id)
