from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from config import mysql
import json

view_comments = Blueprint("view_comments", __name__)


@view_comments.route("/", methods=["GET", "POST"])
def home():
    try:
        if "loggedin" in session:
            id = session["id"]
            first_name = session["first_name"]

            if request.method == "POST":
                note = request.form.get("note")
                if len(note) < 1:
                    flash("Note is Soo Short", category="error")
                else:
                    flash("Note Added ", category="success")
                    cur = mysql.connection.cursor()
                    cur.execute(
                        "INSERT INTO notes SET data = %s  , user_id =%s", (note, id)
                    )
                    mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM notes WHERE user_id = %s ", (id,))
            notes = cur.fetchall()
            print(notes)
            if len(notes) == 0:
                no_comments = True
            else:
                no_comments = False
            your_link = "http://127.0.0.1:5000/add?id=" + str(id)
            return render_template(
                "home.html",
                loggedin=True,
                notes=notes,
                link=your_link,
                no_comments=no_comments,
                first_name=first_name,
            )
        else:
            return redirect(url_for("login.home"))
    except:
        flash("Something Went Wrong", category="error")