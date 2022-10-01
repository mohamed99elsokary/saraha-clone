from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from config import mysql
from argon2 import PasswordHasher

ph = PasswordHasher()
from werkzeug.security import generate_password_hash, check_password_hash

sign_up = Blueprint("sign_up", __name__)


@sign_up.route("/sign-up", methods=["GET", "POST"])
def home():
    try:
        if "loggedin" in session:
            return redirect(url_for("view_comments.home"))
        cur = mysql.connection.cursor()
        if request.method == "POST":
            email = request.form.get("email")
            first_name = request.form.get("firstName")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            password = ph.hash(password1)
            cur.execute("SELECT * FROM users WHERE email = %s ", (email,))
            result = cur.fetchone()
            if result is None:
                if len(email) < 4:
                    flash(
                        "email must be greater than 3 characters", category="error"
                    )
                elif len(first_name) < 2:
                    flash(
                        "first name must be greater than 1 characters",
                        category="error",
                    )
                elif password1 != password2:
                    flash("passwords dont' match", category="error")
                elif len(password1) < 7:
                    flash(
                        "password must be greater than 6 characters",
                        category="error",
                    )
                else:
                    cur.execute(
                        "INSERT INTO users SET first_name = %s, email = %s , password = %s ",
                        (first_name, email, password),
                    )
                    mysql.connection.commit()
                    cur.execute("SELECT * FROM users WHERE email = %s ", (email,))
                    result = cur.fetchone()
                    flash("acc created", category="success")
                    session["loggedin"] = True
                    session["id"] = result["id"]
                    session["first_name"] = result["first_name"]
                    return redirect(url_for("view_comments.home"))
            else:
                flash("Email is already Exists ", category="error")

        return render_template("sign_up.html")
    except:
        flash("Something Went wrong", category="error")
