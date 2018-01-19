import csv
import urllib.request

from flask import redirect, render_template, request, session
from functools import wraps

def apology():
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


def login_required(f):
    "zorgt ervoor dat een user eers moet inloggen alvorens een actie uit te voeren"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def add_user():
    hash = pwd_context.hash(request.form.get("password"))
    result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"),hash=hash)

    # ensure that username is not already in use
    if not result:
        return apology("username already in use")

    return result

def post():
    "deze functie zorgt ervoor dat gebruikers foto's kunnen uploaden"

def rate():
    pictures = db.execute("SELECT * FROM photo")
    picture_amount = len(pictures)
    random_int = random.randint(1, picture_amount)

    photo = db.execute("SELECT * FROM photo WHERE photo_id = :photo_id", photo_id = random_int)
    rated_amount = photo["rated"]

    # dit moet nog in html gezet worden
    rating = request.form.get("rate")

    old_rating = photo["rating"]
    new_rating = (old_rating * rated_amount + rating) /(rated_amount + 1)
    photo_id = photo["photo_id"]

    return db.execute("UPDATE photo SET rating = :rating WHERE photo_id = :photo_id"
                        , rating = new_rating, photo_id = photo_id)

def follow():
"deze functie zorgt ervoor dat een user mensen kan volgen"
def unfollow():
"deze functie zorgt ervoor dat een user mensen kan onvolgen"
def comment():
"deze functie zorgt ervoor dat een user comments kan toevoegen"
def report():
"deze fucntie zorgt ervoor dat een user een andere user kan reporten"
def sorteer():
"deze functie zorgt ervoor dat een user zijn feed kan sorteren"