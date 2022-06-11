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
    products_dict: dict = db['Products']
    db.close()
    eventcount: list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for key in events_dict:
        events = events_dict.get(key)
        d_list = str(events.get_date()).rsplit('-')
        if int(d_list[1]) != 10:
            m = int(d_list[1].replace('0', ''))-1
        else:
            m = int(d_list[1])-1
        eventcount[m] += 1

    sold = 0
    for key in products_dict:
        products = products_dict.get(key)
        sold += int(products.get_sold())
    
    users_list = []
    for key in users_dict:
        users = users_dict.get(key)
        users_list.append(users)
    return render_template("admin/frontpage.html",
                           users_list=users_list,
                           eventcount=eventcount,
                           sold=sold)

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
