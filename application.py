from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from helpers import *
from flask_uploads import UploadSet, configure_uploads, IMAGES
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
        return redirect(url_for("index"))

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

@app.route("/your_userpage", methods = ["GET", "POST"])
@login_required
def your_userpage():
    user_id = session["user_id"]
    username = get_username(user_id)

    if request.method == "POST":
        if request.form.get("change") == "yes":
            return render_template("upload_profile_picture.html")
        return render_template("your_userpage.html", user_id = user_id, username = username)

    else:
         # Volgen van andere gebruiker
        followers_following = following_follower(user_id)
        following = followers_following[0]
        followers = followers_following[1]

        picture_info = get_pictures(user_id)
        return render_template("your_userpage.html", user_id = user_id, username = username,
                                following_amount = len(followers), follower_amount = len(following),
                                picture_info = picture_info, post_amount = len(picture_info))
        return render_template("your_userpage.html", users_id = user_id, username = username)


@app.route("/userpage", methods = ["GET", "POST"])
@login_required
def userpage():
    user_id = request.form.get("user_id")
    username = get_username(user_id)

    if request.method == "POST":
        # Volgen van andere gebruiker
        if request.form.get("follow") == "yes":
            if(follow(user_id) == "Already following"):
                return apology("You are already following this account")

        # Ontvolgen van andere gebruiker
        elif request.form.get("unfollow") == "yes":
            if(unfollow(user_id) == "Not following"):
                return apology("You are not following this account")
        followers_following = following_follower(user_id)
        following = followers_following[0]
        followers = followers_following[1]

        picture_info = get_pictures(user_id)
        return render_template("userpage.html", user_id = user_id, username = username,
                                following_amount = len(followers), follower_amount = len(following),
                                picture_info = picture_info, post_amount = len(picture_info))
    else:
        return render_template("userpage.html", users_id = user_id, username = username)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        photo_path = "/static/uploads/" + filename
        db.execute("INSERT INTO photo(photo_path, id) VALUES(:photo_path, :id)", id = session["user_id"], photo_path = photo_path)


    return render_template('upload.html')

@app.route("/upload_profile_picture", methods = ["GET", "POST"])
def upload_profile_picture():
    if request.method == "POST":
        file = request.files['image']
        f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        file.save(f)

    else:
        return render_template("upload_profile_picture.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    picture_info = picture()
    user_id = picture_info[0]["id"]
    photo_path = picture_info[0]["photo_path"]
    old_rating = picture_info[0]["rating"]
    photo_id = picture_info[0]["photo_id"]
    username = get_username(user_id)
    comments = show_comments(photo_id)

    if request.method == "POST":
        if(request.form.get("go_to_user")) != None:
            return render_template("userpage.html", user_id = user_id, username = user_username)

        if request.form.get("rate") != None:
            rating = int(request.form.get("rate"))
            rate(rating, picture_info)
            return render_template("index.html", photo_path = photo_path, rating = round(old_rating, 1), username = username, user_id = user_id, comments = comments)

        if request.form.get("comment") != None:
            if not request.form.get("comment").strip(" "):
                return apology("ingevulde comment is leeg")
            add_comment(request.form.get("comment"), picture_info)
            return render_template("index.html", photo_path = photo_path, rating = round(old_rating, 1), username = username, user_id = user_id, comments = comments)

    else:
        return render_template("index.html", photo_path = photo_path, rating = round(old_rating, 1), username = username, user_id = user_id, comments = comments)

# @app.route("/profile_picture", methods = ["GET", "POST"])
# @login_required
# def profile_picture():


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
