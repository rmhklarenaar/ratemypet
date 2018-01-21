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

def user_id():
    # gebruiker ophalen uit de database
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
    # Id van de gebruiker opslaan
    session["user_id"] = rows[0]["id"]

    return session["user_id"]

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

def select_username():
    return db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

def post():
    "deze functie zorgt ervoor dat gebruikers foto's kunnen uploaden"
    return apology("pagina is nog niet af")

def rate(rating):
    pictures = db.execute("SELECT * FROM photo")
    picture_amount = len(pictures)

    if(picture_amount == 0):
        return apology("er zijn geen foto's beschikbaar.")
    random_int = random.randint(1, picture_amount)

    photo = db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = random_int)
    rated_amount = photo[0]["rated"]

    # dit moet nog in html gezet worden
    rating = rating

    old_rating = photo[0]["rating"]
    new_rating = (old_rating * rated_amount + rating) /(rated_amount + 1)
    photo_id = photo[0]["photo_id"]

    return db.execute("UPDATE photo SET rating = :rating, rated = :rated WHERE photo_id = :photo_id"
                        , rating = new_rating, rated = rated_amount + 1, photo_id = photo_id)

def follow_helper():
    "deze functie zorgt ervoor dat een user mensen kan volgen"

    return apology("pagina is nog niet af")
def unfollow():
    "deze functie zorgt ervoor dat een user mensen kan onvolgen"
    return apology("pagina is nog niet af")
def comment():
    "deze functie zorgt ervoor dat een user comments kan toevoegen"
    return apology("pagina is nog niet af")
def report():
    "deze fucntie zorgt ervoor dat een user een andere user kan reporten"
    return apology("pagina is nog niet af")
def sorteer():
    "deze functie zorgt ervoor dat een user zijn feed kan sorteren"
    return apology("pagina is nog niet af")