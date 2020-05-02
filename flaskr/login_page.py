from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('login_page', __name__, url_prefix="/login")

@bp.route("/", methods=["POST", "GET"])
def signing_in():
    info = ""
    if request.method == "POST":
        username = request.form.get("id_field")
        if username:
            db = get_db()
            results = db.execute('SELECT username FROM users').fetchall()
            print(results)
            if results:
                for user in results:
                    if user[0] == username:
                        g.username = username
                        return redirect(url_for('main_menu.dashboard'))
            else:
                info = "User does not exist"
    
    return render_template('login_page/login.html', text_info=info)

@bp.route("/register", methods=["POST", "GET"])
def register():
    username_exist = False
    info = ""
    if request.method == "POST":
        username = request.form.get("id_field")
        db = get_db()
        results = db.execute('SELECT username FROM users').fetchall()
        if results:
            for user in results:
                if user[0] == username:
                    username_exist = True
                    break
        if not username_exist:
            result = db.execute("INSERT INTO users (username) VALUES ('{}')".format(username))
            db.commit()
            create_table_log_user(username, db)
            info = "Succesfully registered"
            # return redirect(url_for("login_page.signing_in"))

    return render_template('login_page/register.html', exist=username_exist, text_info=info)

def create_table_log_user(username, db):
    create_table_sql = """ CREATE TABLE IF NOT EXISTS log_{} (
                                id integer PRIMARY KEY,
                                product_id integer,
                                qty integer NOT NULL,
                                date_added text
                        );""".format(username)
    
    db.execute(create_table_sql)
    db.commit()
