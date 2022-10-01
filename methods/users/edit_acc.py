from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from config import mysql
from argon2 import PasswordHasher

ph = PasswordHasher()
from werkzeug.security import generate_password_hash, check_password_hash

edit_acc = Blueprint("edit_acc", __name__)


@edit_acc.route("/edit_acc", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        email = request.form.get("email")
        i_old_password = request.form.get("old_password")
        new_password1 = request.form.get("new_password1")
        new_password2 = request.form.get("new_password2")
        new_name = request.form.get("name")

        if new_password1 != new_password2:
            flash("passwords don't match", category="error")
        if new_password1 == new_password2:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email = %s ", (email,))
            result = cur.fetchone()
            if result != None:
                id = result["id"]
                email = result["email"]
                old_password = result["password"]
                first_name = result["first_name"]
                try:
                    password = ph.verify(
                        old_password,
                        i_old_password,
                    )
                    password = True
                except:
                    password = False

                if password:
                    password = ph.hash(new_password1) if new_password1 != None else old_password
                    name = new_name if new_name != None else first_name
                    cur.execute(
                        "UPDATE users SET password =%s ,first_name =%s WHERE id = %s",
                        (password, name, id),
                    )
                    mysql.connection.commit()
                    session.pop("first_name", None)
                    session["first_name"] = name
                    flash("edit saved successfully", category="success")
                    return redirect(url_for("view_comments.home"))
                else:
                    flash("your old password is invalid", category="error")
    return render_template("edit_acc.html", title="edit acc", loggedin=True)
