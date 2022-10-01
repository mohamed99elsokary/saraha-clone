from config import app, mysql
from flask import Blueprint, request
from status import *
import json
import string
import random


from mail_sender import mail_sender

reset_password = Blueprint("reset_password", __name__)


@reset_password.route("/users/reset_password", methods=["POST"])
def home():
    # fetching input type
    if request.content_type == "application/json":
        inputt = request.json
    else:
        inputt = request.form
    email = inputt.get("email")
    code = inputt.get("code")
    password = inputt.get("password")

    cur = mysql.connection.cursor()
    cur.execute("SELECT reset_password FROM users WHERE email = %s ", (email,))
    results = cur.fetchall()
    for row in results:
        reset_password = row["reset_password"]
    if code is None:
        random_code = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
        )
        cur.execute(
            "UPDATE users SET reset_password = %s  WHERE email = %s",
            (random_code, email),
        )
        mysql.connection.commit()

        mail = (
            """Acasa wants to tell you that :
        this is your reset password code is """
            + random_code
        )

        mail_sender(email, mail)
        return {"status": successful, "code": random_code}
    else:
        if reset_password == code:
            cur.execute(
                "UPDATE users SET password = %s , reset_password = null  WHERE email = %s",
                (password, email),
            )
            mysql.connection.commit()
            return {"status": successful}
        else:
            return {"status": reset_password_faild}
