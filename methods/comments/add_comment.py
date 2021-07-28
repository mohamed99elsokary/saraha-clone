from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from config import mysql
import json

add_comment = Blueprint("add_comment", __name__)


@add_comment.route("/add", methods=["GET", "POST"])
def home():

    id = request.args["id"]
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is Soo Short", category="error")
        else:
            flash("Note Added ", category="success")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO notes SET data = %s  , user_id =%s", (note, id))
            mysql.connection.commit()
    if "loggedin" in session:
        return render_template("home.html", loggedin=True, add=1)
    else:
        return render_template("home.html", loggedin=False, add=1)
