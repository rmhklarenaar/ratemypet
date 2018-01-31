from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
from flask_uploads import UploadSet, configure_uploads, IMAGES
from giphypop import translate, upload
import os

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

@app.route("/login", methods=["GET", "POST"])
def login():

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username!")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password!")

        # query database for username
        rows = select_username(request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("Invalid username and/or password!")

        user_id(request.form.get("username"))
        # redirect user to home page
        return redirect(url_for("feed"))

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
            return apology("Must provide username!")
        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password!")
        # ensure password check was submitted
        elif not request.form.get("password_check"):
            return apology("Must provide password check!")
        # ensure passwords match
        elif request.form.get("password_check") != request.form.get("password"):
            return apology("Passwords must match!")

        # querry database for username
        rows = select_username(request.form.get("username"))
        # ensure username exists and password is correct
        if len(rows) > 0:
            return apology("Username already exists")

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

@app.route("/your_userpage", methods = ["GET", "POST"])
@login_required
def your_userpage():
    # storing varables
    user_id = session["user_id"]
    username = get_username(user_id)
    followers_following = following_follower(user_id)
    following = followers_following[0]
    followers = followers_following[1]
    picture_info = get_pictures(user_id)
    profile_pic = select_profile_pic(user_id)

    # when the delete button is clicked, the photo will be deleted from the database
    if request.form.get("delete_photo") != None:
        delete_picture(request.form.get("delete_photo"))
        return redirect(url_for("your_userpage"))

    # when the reset button is clicked, the history will be cleared and the user can rate all pictures again
    if request.form.get("reset") != None:
        reset_history(user_id)

    # when the change button is clicked, the user will be able to change his profile picture
    if request.form.get("change") == "yes":
        return render_template("upload_profile_picture.html")

    # redirect to your userpage
    return render_template("your_userpage.html", user_id = user_id, username = username,
                            following_amount = len(followers), follower_amount = len(following),
                            picture_info = picture_info,profile_pic = profile_pic, post_amount = len(picture_info))

@app.route("/userpage", methods = ["GET", "POST"])
@login_required
def userpage():
    print("00000000000000000000000000000000000000000000000000000")
    # storing variables
    user_id = request.form.get("user_id")
    username = get_username(user_id)

    # redirect to your own userpage when searching yourself so you cant follow yourself
    if int(user_id) == session["user_id"]:
        return redirect(url_for("your_userpage"))


    if request.method == "POST":
        # following other users
        if request.form.get("follow") == "yes":
            if(follow(user_id) == "Already following"):
                return apology("You are already following this account!")

        # unfollow other users
        elif request.form.get("unfollow") == "yes":
            if(unfollow(user_id) == "Not following"):
                return apology("You are not following this account!")

        #seperate followers and following from lists in list
        followers_following = following_follower(user_id)
        following = followers_following[0]
        followers = followers_following[1]

        picture_info = get_pictures(user_id)
        # redirect to userpage
        return render_template("userpage.html", user_id = user_id, username = username,
                                following_amount = len(followers), follower_amount = len(following),
                                picture_info = picture_info, profile_pic = select_profile_pic(user_id),post_amount = len(picture_info))

    else:
        # redirect to userpage when GET
        return render_template("userpage.html", users_id = user_id, username = username)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    photos = UploadSet('photos', IMAGES)

    app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
    configure_uploads(app, photos)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        photo_path = "/static/uploads/" + filename
        caption = request.form.get("caption")
        upload_photo(photo_path, caption)

    return render_template('upload.html')

@app.route("/upload_profile_picture", methods = ["GET", "POST"])
@login_required
def upload_profile_picture():
    photos = UploadSet('photos', IMAGES)

    app.config['UPLOADED_PHOTOS_DEST'] = 'static/profile_pic'
    configure_uploads(app, photos)
    if request.method == "POST" and "photo" in request.files:
        try:
            filename = photos.save(request.files['photo'])
            photo_path = "/static/profile_pic/" + filename
            upload_profile_pic(photo_path)
        except:
            return apology("Must submit a file!")

        return redirect(url_for("your_userpage"))
    else:
        return render_template("upload_profile_picture.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def feed():
    # get a picture that's unique and not from yourself
    picture_info = get_right_picture(request.form.get("photo_id"), request.form.get("rate"), request.form.get("check_comment"))
    if picture_info == "comment":
        picture_info = get_picture_info(request.form.get("photo_id"))

    # give apology when no pictures left to rate
    if picture_info == "apology":
        return apology ("all out of photo's")

    # store frequently used variables
    user_id = picture_info[0]["id"]
    photo_id = int(picture_info[0]["photo_id"])


    # store frequently used render template for feed
    redirect_to_feed = render_template("feed.html", photo_path = picture_info[0]["photo_path"], rating = round(picture_info[0]["rating"], 1),gifs = show_gifs(photo_id),
                                username = get_username(user_id), user_id = user_id, comments = show_comments(photo_id), photo_id = photo_id,
                                caption = picture_info[0]["caption"])

    if request.method == "POST":
        # report a persons post
        if request.form.get("report") != None:
            report(photo_id, user_id)
            return redirect_to_feed

        # add to history after rating
        if request.form.get("rate") != None:
            add_to_history(user_id, photo_id)
            rating = int(request.form.get("rate"))
            rate(rating, request.form.get("photo_id"))
            return redirect_to_feed

        # add comments
        if request.form.get("comment") != None:
            # add gif as a comment
            if request.form.get("comment").startswith("/gif"):
                query = request.form.get("comment")[len("/gif"):]
                giphy = translate(query,api_key="OqJEhuVDXwcAVJbRre1ubPPRj2nkjMWh")
                gif = giphy.fixed_height.downsampled.url
                add_gif(gif, request.form.get("photo_id"),username)
                return redirect_to_feed
            # add a normal comment
            else:
                add_comment(request.form.get("comment"), request.form.get("photo_id"), session["user_id"])
                return redirect_to_feed
    else:
        # redirect to feed when GET
        return redirect_to_feed

@app.route("/search", methods = ["GET", "POST"])
@login_required
def search():
    username = request.form.get("search_username")

    if request.method == "POST":
        user = search_user(username)
        user_id = user[0]["id"]

        # give apology when user doesnt exist
        if len(user) == 0:
            return apology("User does not exist!")

        # split followers and following from lists in list
        followers_following = following_follower(user_id)
        following = followers_following[0]
        followers = followers_following[1]

        # go to your_userpage when you type own name
        if user_id == session["user_id"]:
            return redirect(url_for("your_userpage"))

        # go to the chosen userpage
        return render_template("userpage.html", user_id = user_id, username = username,
                                following_amount = len(followers), follower_amount = len(following),
                                picture_info = get_pictures(user_id), profile_pic = select_profile_pic(user_id),post_amount = len(picture_info))

    else:
        # redirect to search when GET
        return render_template("search.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def password_change():
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        change_password(request.form.get("current_password"), request.form.get("new_password"),  request.form.get("new_password_again"))
        return redirect(url_for("your_userpage"))
    else:
        return render_template("password_change.html")


@app.route("/hot")
@login_required
def hot():
    leaderboard = featured_photos()
    return render_template("hot.html", leaderboard = leaderboard)


