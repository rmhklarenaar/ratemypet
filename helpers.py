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

def post():

def rate():
"deze functie zorgt ervoor dat een user foto's kan raten"
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