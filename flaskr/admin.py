from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix="/admin",template_folder="templates/admin")

@bp.route("/products", methods=["POST","GET"])
def products():
    if request.method == "GET":
        db = get_db()
        results = db.execute("SELECT product_name, product_image_loc FROM products").fetchall()
        img_link = []
        products = []
        for product in results:
            products.append(product[0])
            img_link.append(product[1])

    return render_template("admin/products.html", products=products, img_link=img_link)


@bp.route("/users", methods=["POST","GET"])
def users_products():
    db = get_db()
    items_name = []
    date = []
    qty = []
    img_link = []

    results = db.execute("SELECT username FROM users").fetchall()
    users = []
    for user in results:
        users.append(user[0])

    if request.method == "POST":
        username = request.form.get("users")
        if username:
            results = db.execute('SELECT * FROM log_{}'.format(username)).fetchall()
            for item in results:
                product_result = db.execute('SELECT product_name, product_image_loc FROM products WHERE id={}'.format(item[1])).fetchone()
                items_name.append(product_result[0])
                img_link.append(product_result[1])
                qty.append(item[2])
                date.append(item[3])
        print(username, items_name)

    return render_template("admin/users_products.html", users=users, items_name=items_name, date=date, qty=qty, img_link=img_link)