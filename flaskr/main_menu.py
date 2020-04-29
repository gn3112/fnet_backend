from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from functools import wraps

bp = Blueprint('main_menu', __name__, url_prefix="/<identifier>", template_folder="templates/main_menu")

def restrict(func):
    @wraps(func)
    def wrapper():
        if not g.username:
            return 'Not Allowed'
        else:
            return func()
    return wrapper

@bp.url_defaults
def add_user(endpoint, values):
    values.setdefault("identifier", g.username)

@bp.url_value_preprocessor
def pull_user(endpoint, values):
    g.username = values.pop('identifier')

@bp.route("/dashboard", methods=["POST","GET"])
@restrict
def dashboard():
    items = []
    img_link = []
    qty = []
    date = []
    return render_template("main_menu/dashboard.html", items=items, img_link=img_link, qty=qty, date=date)

@bp.route("/history", methods=["POST","GET"])
@restrict
def history():
    return 'Hello World'