from flask import Blueprint, render_template, flash, session, redirect, url_for, request
from config import mysql
import json

delete_comment = Blueprint("delete_comment", __name__)


@delete_comment.route("/delete-note", methods=["POST"])
def home():

    note = json.loads(request.data)
    note_id = note["noteId"]
    user_id = session["id"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM notes WHERE  id= %s ", (note_id,))
    notes = cur.fetchone()
    if notes != None:
        owner_id = notes["user_id"]
        if owner_id == user_id:
            cur.execute("DELETE FROM notes WHERE id =%s", (note_id,))
            mysql.connection.commit()
            flash("Note deleted ", category="success")
        else:
            flash("wierd error ", category="error")

    return render_template("home.html", loggedin=True, notes=notes)