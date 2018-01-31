from cs50 import SQL
import csv
import urllib.request
from passlib.apps import custom_app_context as pwd_context
from flask import redirect, render_template, request, session
from functools import wraps

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


def apology(message):
    # apology geven wanneer nodig
    return render_template("apology.html", message = message)


def user_id(username):
    # user id genereren en opslaan in session["user_id"]
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
    session["user_id"] = rows[0]["id"]

def login_required(f):
    # make it required a user has to be logged in at certain pages
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def add_user():
    # add user to the database
    result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=pwd_context.hash(request.form.get("password")))
    return result

def get_username(user_id):
    # get username from database with user id
    username = db.execute("SELECT username FROM users WHERE id = :user_id", user_id = user_id)
    return username[0]["username"]

def get_user_id(username):
    # get user id from database with username
    user_id = db.execute("SELECT id FROM users WHERE username = :username", username = username)
    return user_id[0]["id"]

def select_username(username):
    # return personal data with username
    return db.execute("SELECT * FROM users WHERE username = :username", username=username)

def rate(rating, photo_id):
    # select picture info
    photo = db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

    # store variables
    rated_amount = photo[0]["rated"]
    old_rating = photo[0]["rating"]
    photo_id = photo[0]["photo_id"]

    # calculate new rating
    new_rating = (old_rating * rated_amount + rating) /(rated_amount + 1)

    # update the rating and rating amount
    db.execute("UPDATE photo SET rating = :rating, rated = :rated WHERE photo_id = :photo_id", rating = new_rating, rated = rated_amount + 1, photo_id = photo_id)

def picture():
    # get a random picture from the database
    photo = db.execute("SELECT * FROM photo ORDER BY RANDOM() LIMIT 1")
    return photo

def follow(user_to_follow):
    user = session["user_id"]

    # select the user who follows and the user who is being followed
    username_to_follow = db.execute("SELECT username FROM users WHERE id = :user_to_follow", user_to_follow = user_to_follow)
    username_user = db.execute("SELECT username FROM users WHERE id = :user", user = user)

    # check if user is alreading following the user
    check = db.execute("SELECT * FROM following WHERE id = :user AND following_id = :user_to_follow", user = user, user_to_follow = user_to_follow)
    if check:
        check = "Already following"
        return check

    # insert the new following and follower in database
    db.execute("INSERT INTO following (id, following_id, following_username) VALUES(:id, :following_id, :following_username)", id = user, following_id = user_to_follow, following_username = username_user[0]["username"])
    return db.execute("INSERT INTO followers (id, follower_id, follower_username) VALUES(:id, :follower_id, :follower_username)", id = user_to_follow, follower_id = user, follower_username = username_to_follow[0]["username"])

def unfollow(user_to_unfollow):
    user = session["user_id"]

    # check if user is following the user already
    check = db.execute("SELECT * FROM following WHERE id = :user AND following_id = :user_to_unfollow", user = user, user_to_unfollow = user_to_unfollow)
    if not check:
        check = "Not following"
        return check

    # delete their following and follower from database
    db.execute("DELETE FROM following WHERE id = :id AND following_id = :following_id", id = user, following_id = user_to_unfollow)
    return db.execute("DELETE FROM followers WHERE id = :id AND follower_id = :follower_id", id = user_to_unfollow, follower_id = user)

def following_follower(user_id):
    # get the data from following and follower from a user and return it
    follower_following = []
    follower_following += [db.execute("SELECT follower_username FROM followers WHERE id = :id", id = user_id)]
    follower_following += [db.execute("SELECT following_username FROM following WHERE id = :id", id = user_id)]
    return follower_following

def get_pictures(user_id):
    # get picture data from a user
    return db.execute("SELECT * FROM photo WHERE id = :user_id", user_id = user_id)


def get_picture_info(photo_id):
    return db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

def get_right_picture(request_photo_id, rate, check_comment):
    request_photo_id = 0

    # make int from request_photo_id
    if request_photo_id != None:
        request_photo_id = int(request_photo_id)

    select_picture = False
    # keep trying to find the right picture till it is found
    while(select_picture == False):
        # generate a random picture
        picture_info = picture()
        # get the right data from the picture
        user_id = picture_info[0]["id"]
        photo_id = int(picture_info[0]["photo_id"])

        # if the picture is rated, add it to the history
        if rate != None:
            add_to_history(user_id, photo_id)

        # check if there are pictures left to rate
        if none_left() == 1:
            return "apology"

        # check if picture is already in the history
        elif history_check(photo_id) != 0:
            select_picture = False

        # check if a picture is being commented
        elif check_comment == "True":
            return "comment"

        # check if picture is from the user
        elif user_id == session["user_id"]:
            select_picture = False
        else:
            return picture_info

def get_picture_info(photo_id):
    # get picture info with photo_id
    return db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)


def add_comment(comment, photo_id, user_id):
    # add comments
    return db.execute("INSERT INTO comments(photo_id, comments, username, id) VALUES(:photo_id, :comments, :username, :user_id)",photo_id = photo_id ,comments = comment,username=get_username(user_id), user_id = user_id)

def add_gif(gif, photo_id, user_id):
    # add gif as a comment
    return db.execute("INSERT INTO gifs(photo_id, photo_path, username, id) VALUES(:photo_id, :photo_path, :username, :user_id)",photo_id = photo_id ,photo_path = gif,username=get_username(user_id), user_id = user_id)

def show_gifs(photo_id):
    # select gifs
    gifs = db.execute("SELECT * FROM (SELECT * FROM gifs WHERE photo_id = :photo_id ORDER BY time DESC LIMIT 2) t ORDER BY time ASC", photo_id = photo_id)
    # reverse the list so the newest comments are shown first
    reversed_gifs = list(reversed(gifs))
    return reversed_gifs

def show_comments(photo_id):
    # select comments
    comments = db.execute("SELECT * FROM (SELECT * FROM comments WHERE photo_id = :photo_id ORDER BY time DESC LIMIT 2) t ORDER BY time ASC", photo_id = photo_id)
    # revers comments so the newest comments are shown first
    reversed_comments = list(reversed(comments))
    return reversed_comments

def featured_photos():
    featured = db.execute("SELECT * FROM(SELECT * FROM photo ORDER BY rating DESC LIMIT 10) t ORDER BY rating ASC")
    return featured

def report():
    "deze fucntie zorgt ervoor dat een user een andere user kan reporten"
    return apology("Pagina is nog niet af!")

def search_user(username):
    # select user informatie with username
    user = db.execute("SELECT * FROM users WHERE username = :username", username = username)
    return user

def upload_photo(photo_path, caption):
    # put the new picture in the database
    add_photo = db.execute("INSERT INTO photo(id, photo_path, caption) VALUES(:id, :photo_path, :caption)", id = session["user_id"] , photo_path = photo_path, caption = caption)
    return add_photo

def upload_profile_pic(photo_path):
    # change profile picture
    db.execute("DELETE FROM profile_pic WHERE id = :id", id = session["user_id"])
    db.execute("INSERT INTO profile_pic(id, photo_path) VALUES(:id, :photo_path)", id = session["user_id"] , photo_path = photo_path)

def select_profile_pic(user_id):
    # show the profile picture for in userpage
    profile_pics = db.execute("SELECT * FROM profile_pic WHERE id = :id", id = user_id)
    if len(profile_pics) == 0:
        return "/static/profile_pic/stock.png"
    else:
        return profile_pics[0]['photo_path']

def reset_history(id):
    # reset feed history so you can rate pictures again
    db.execute("DELETE FROM history WHERE id = :id", id = id)

def add_to_history(photo_id, user_id):
    # add a rating to history so you cant rate picture more then once
    db.execute("INSERT INTO history(user_id,id,photo_id) VALUES(:user_id,:id,:photo_id)", id = session["user_id"], user_id = user_id, photo_id = photo_id)

def history_check(photo_id):
    # check if you already seen a picture
    rows = db.execute("SELECT * FROM history WHERE photo_id = :photo_id AND id = :id", photo_id = photo_id, id = session["user_id"])
    if len(rows) == 0:
        return 0
    else:
        return 1

def none_left():
    # check if there are no more pictures left to see
    history = db.execute("SELECT photo_id FROM history WHERE id = :id", id = session["user_id"])
    photo = db.execute("SELECT photo_id FROM photo WHERE id != :id", id = session["user_id"] )
    if len(photo)==len(history):
        return 1

def total_photos():
    #get the total amount of pictures
    total = db.execute("SELECT photo_id FROM photo")
    return len(total)

def change_password(current_password, new_password, new_password_again):

    rows = db.execute("SELECT * FROM users WHERE id = :id",  id = session["user_id"])
    # ensure all fields are filled in
    if not current_password:
        return apology("must provide your current password")

    elif not new_password:
        return apology("must provide a new password")

    elif not new_password_again:
        return apology("must re-enter new password")

    # ensure the passwords match
    elif new_password_again != new_password:
        return apology("passwords do not match")

    # ensure the old password was correct
    elif not pwd_context.verify(current_password, rows[0]["hash"]):
        return apology("current password is not correct")

    # ensure the user creates a new password
    elif new_password == current_password:
        return apology("must provide a password that is diffrent from your current password")

    # update users password
    hash = pwd_context.hash(new_password)
    db.execute("UPDATE users SET hash = :hash WHERE id = :id",id= session["user_id"], hash = hash)

def delete_picture(photo_id):
    # delete a picture
    db.execute("DELETE FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)

def report(photo_id, user_id):
    # select reports from the picture
    report_count = db.execute("SELECT reports FROM photo WHERE photo_id = :photo_id", photo_id = photo_id)
    report_count = report_count[0]["reports"]

    #if the picture has already been reported 4 times it gets deleted otherwise the report_count gets updated
    if report_count == 4:
        delete_picture(photo_id)
    else:
        new_reports = report_count + 1
        db.execute("UPDATE photo SET reports = :reports WHERE photo_id = :photo_id", reports = new_reports, photo_id = photo_id)

    # select reports from the owner of the picture
    user_report_count = db.execute("SELECT reports FROM users WHERE id = :user_id", user_id = user_id)
    user_report_count = user_report_count[0]["reports"]

    # if the user has already been reported 14 times his accounts gets deleted otherwise the report_count gets updated
    if user_report_count == 14:
        db.execute("DELETE * FROM users WHERE id = :user_id", user_id = user_id)
    else:
        new_user_reports = user_report_count + 1
        db.execute("UPDATE users SET reports = :reports WHERE id = :user_id", reports = new_user_reports, user_id = user_id)

