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

# custom filter
app.jinja_env.filters["usd"] = usd
# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
"GEEN IDEE WAT DIT STUK HIERONDER DOET (EINDE)"


@app.route("/login", methods=["GET", "POST"])
def login():
    "HIER LOGT DE USER IN"
    "TODO"



@app.route("/register", methods=["GET", "POST"])
def register():
    "HIER REGRISTREERT DE USER HET ACCOUNT"
    "TODO"


@app.route("/logout")
def logout():
    "HIER LOGT DE USER UIT"

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    "TODO"

@app.route("/search", methods=["GET", "POST"])
def search():
    "HIER KAN DE USER ANDERE ACCOUNTS OPZOEKEN"
    "TODO"



