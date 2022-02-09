from PIL import Image
from flask import Blueprint, url_for, render_template, redirect, request
import os
import os.path
import shelve
from data.db_ep import get_db

endpoint = Blueprint("users", __name__)
basedir = os.getcwd()


@endpoint.route("/users")
def users():
    db = shelve.open(get_db(), flag="c")
    users_dict: dict = db["current_session"]
    db.close()
    users_list = []
    for key in users_dict:
        users = users_dict.get(key)
        users_list.append(users)

    return render_template(
        "admin/users/users.html", users_list=users_list, count=len(users_list)
    )