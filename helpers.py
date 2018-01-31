from cs50 import SQL
import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps

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

def get_right_picture(request_photo_id, rate, check_comment):
    request_photo_id = 0
    if request_photo_id != None:
        request_photo_id = int(request_photo_id)

    select_picture = False
    while(select_picture == False):
        picture_info = picture()
        user_id = picture_info[0]["id"]
        photo_id = int(picture_info[0]["photo_id"])

        if rate != None:
            add_to_history(user_id, photo_id)

        if none_left() == 1:
            return "apology"
        elif history_check(photo_id) != 0:
            select_picture = False

        elif check_comment == "True":
            return get_picture_info(request_photo_id)
        elif user_id == session["user_id"]:
            select_picture = False
        elif photo_id == request_photo_id:
            select_picture = False
        else:
            return picture_info

def get_picture_info(photo_id):
    return db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

def add_comment(comment, photo_id, user_id):
    comment = comment
    return db.execute("INSERT INTO comments(photo_id, comments, username, id) VALUES(:photo_id, :comments, :username, :user_id)",photo_id = photo_id ,comments = comment,username=get_username(user_id), user_id = user_id)

def add_gif(gif, photo_id, user_id):
    return db.execute("INSERT INTO gifs(photo_id, photo_path, username, id) VALUES(:photo_id, :photo_path, :username, :user_id)",photo_id = photo_id ,photo_path = gif,username=get_username(user_id), user_id = user_id)

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

def report():
    "deze fucntie zorgt ervoor dat een user een andere user kan reporten"
    return apology("Pagina is nog niet af!")


def search_user(username):
    user = db.execute("SELECT * FROM users WHERE username = :username", username = username)
    return user

def upload_photo(photo_path, caption):

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

def change_password():

    rows = db.execute("SELECT * FROM users WHERE id = :id",  id = session["user_id"])
    # ensure all fields are filled in
    if not request.form.get("current_password"):
        return apology("must provide your current password")

    elif not request.form.get("new_password"):
        return apology("must provide a new password")

    elif not request.form.get("new_password_again"):
        return apology("must re-enter new password")

    # ensure the passwords match
    elif request.form.get("new_password_again") != request.form.get("new_password"):
        return apology("passwords do not match")

    # ensure the old password was correct
    elif not pwd_context.verify(request.form.get("current_password"), rows[0]["hash"]):
        return apology("current password is not correct")

    # ensure the user creates a new password
    elif request.form.get("new_password") == request.form.get("current_password"):
        return apology("must provide a password that is diffrent from your current password")

    # update users password
    hash = pwd_context.hash(request.form.get("new_password"))
    db.execute("UPDATE users SET hash = :hash WHERE id = :id",id= session["user_id"], hash = hash)

    # let the user know the password is changed
    return render_template("feed.html")

def delete_picture(photo_id):
    db.execute("DELETE FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

def report(photo_id, user_id):
    report_count = db.execute("SELECT reports FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)
    report_count = report_count[0]["reports"]
    if report_count == 4:
        delete_picture(photo_id)
    else:
        new_reports = report_count + 1
        db.execute("UPDATE photo SET reports = :reports WHERE photo_id = :photo_id", reports = new_reports, photo_id = photo_id)

    user_report_count = db.execute("SELECT reports FROM users WHERE id = :user_id", user_id = user_id)
    user_report_count = user_report_count[0]["reports"]
    if user_report_count == 14:
        db.execute("DELETE * FROM users WHERE id = :user_id", user_id = user_id)
    else:
        new_user_reports = user_report_count + 1
        db.execute("UPDATE users SET reports = :reports WHERE id = :user_id", reports = new_user_reports, user_id = user_id)

