from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from functools import wraps

import sys
sys.path.append("/Users/georgesnomicos/fnet")
from test_fruit_model import fruit_test

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
    feed_image = "test.jpeg"
    product_id = 2
    qty = 1
    date_added = "29/04"
    db = get_db()

    result = db.execute("INSERT INTO log_{} (product_id, qty, date_added) VALUES ({}, {} , '{}')".format(g.username, product_id, qty, date_added))
    db.commit()
    result = db.execute("DELETE FROM log_gn WHERE id>4")
    db.commit()

    results = db.execute('SELECT * FROM log_{}'.format(g.username)).fetchall()
    items_name = []
    img_link = []
    qty = []
    date = []
    for item in results:
        product_result = db.execute('SELECT product_name, product_image_loc FROM products WHERE id={}'.format(item[1])).fetchone()
        items_name.append(product_result[0])
        img_link.append(product_result[1])
        qty.append(item[2])
        date.append(item[3])
    
    if request.method == "POST":
        if request.form.get("capture"):            
            db = get_db()
            image = db.execute('SELECT image FROM store where id=1').fetchone()[0]
            prob, item_name = model_infer(image, model="")
            
            prob, item_name = 0.9, "Other"

            stream = io.BytesIO(image)
            img = Image.open(stream)

            d = ImageDraw.Draw(img)
            font = ImageFont.truetype('/Users/georgesnomicos/Library/Fonts/arial_narrow_7.ttf',50)

            d.text((250,500), item_name[0], fill=(255,0,0),font=font)
            # d.text((250,400), "%s "%(round(prob.item(),2)), fill=(255,0,0),font=font)

            img.save('img.jpeg')
            with open('img.jpeg','rb') as f:
                image = f.read()

            db.execute('UPDATE store SET image=? WHERE id=2', [image])
            db.commit()

            feed_image = "static.jpeg"

    return render_template("main_menu/dashboard.html", feed_image=feed_image,items_name=items_name, img_link=img_link, qty=qty, date=date)

@bp.route("/history", methods=["POST","GET"])
@restrict
def history():
    return 'Not implemented'