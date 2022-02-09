from flask import Blueprint, render_template
import os
import os.path
import shelve

from itsdangerous import json
from data.db_ep import get_db, create_db
from services.admin.events_ep import events

endpoint = Blueprint("admin", __name__)
basedir = os.getcwd()

@endpoint.route("/frontpage")
def admin_frontpage():
    if os.path.isfile(f'{get_db()}.dat') is False:
        create_db()
    db = shelve.open(get_db(), flag='c')
    events_dict: dict = db['Events']
    users_dict: dict = db['Users']
    db.close()
    print(f'{events_dict}')
    events_list = []
    for key in events_dict:
        events = events_dict.get(key)
        events_list.append(events)
    users_list = []
    for key in users_dict:
        users = users_dict.get(key)
        users_list.append(users)
    return render_template("admin/frontpage.html",
                           events_list=events_list,
                           users_list=users_list,
                           count=len(events_list))

@endpoint.route("/notif")
def notif():
    db = shelve.open(get_db(), flag='c')
    events_dict: dict = db['Events']
    db.close()
    events_list = []
    for key in events_dict:
        events = events_dict.get(key)
        events_list.append(events)
    notif = []
    for i in events_list:
        if i.get_sold() == 0:
            notif.append(f'{i.get_name()} has {i.get_sold()} ticket sold.')
    print(notif)
    return notif[0]
