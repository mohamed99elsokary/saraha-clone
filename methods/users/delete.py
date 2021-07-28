from config import app, mysql
from flask import Blueprint, request
from status import *
import json

delete = Blueprint("delete", __name__)


@delete.route("/users/delete", methods=["POST"])
def home():
    # fetching input type
    if request.content_type == "application/json":
        inputt = request.json
    else:
        inputt = request.form
    id = inputt.get("id")
    is_deleted = inputt.get("is_deleted")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_deleted = %s WHERE id = %s", (is_deleted, id))
    mysql.connection.commit()
    return {"status": successful}
