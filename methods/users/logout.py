from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from config import mysql
from argon2 import PasswordHasher

ph = PasswordHasher()
from werkzeug.security import generate_password_hash, check_password_hash

logout = Blueprint("logout", __name__)


@logout.route("/logout")
def home():

    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("first_name", None)
    return redirect(url_for("login.home"))