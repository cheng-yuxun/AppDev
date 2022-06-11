from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from services.forms.form_rewards import CreateForm
from datetime import date
import shelve
from data import Rewards, Person
# from fastapi import Form, FastAPI
# from starlette.requests import Request
from werkzeug.utils import secure_filename
import os
from data.db_ep import get_db, create_db

basedir = os.getcwd()
DBDIR = f"{basedir}/notes"
app = Flask(__name__)
app.secret_key = 'qasxcvgtredsxc'
app.config['DEBUG'] = True

Upload_Folder = 'static/assets/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['Upload_FOLDER'] = Upload_Folder

today = date.today()

endpoint = Blueprint("userewards", __name__)


# #Cilent
# @app.route('/')
# def home():
#     session["points"] = 123456
#     return render_template('home.html')


@endpoint.route('/detailedRewards/<id>')
def detailedRewards(id):
    rewards_dict = {}
    db = shelve.open(get_db(), 'w')
    rewards_dict = db['Rewards']
    rewards = rewards_dict.get(id)
    points = db['points']
    db['id'] = id
    db.close()

    return render_template('rewards_user/detailedRewards.html', rewards=rewards, points=points, id=id)


@endpoint.route('/redeemedRewards/<rewardPts>/<qty>')
# USE THIS ONCE FORM IS SETUP IN "/detailedRewards"
# @app.route('/redeemedRewards/<id>, methods=['GET', 'POST'])
# def redeemedRewards(id):
def redeemedRewards(rewardPts, qty):
    rewards_dict = {}
    # ADD NAME AND EXPIRY DATE OF VOUCHER TO HISTORY SHELVE
    history_dict = {}
    db = shelve.open(get_db(), 'w')
    rewards_dict = db['Rewards']

    try:
        history_dict = db['History']

    except:
        print('Creating new dict')
        db['History'] = {}
        history_dict = db['History']

    points = db['points']

    # qty = request.form['count']
    # rewardPts = rewards.get_points()
    # print(rewardPts, qty)

    # if(request.method == 'POST'):
    rewards = rewards_dict.get(db['id'])
    # rewards = rewards_dict.get(id)
    redeemedPts = int(rewardPts) * int(qty)
    remainingPts = points - redeemedPts
    db['points'] = remainingPts
    rewards.set_redemption(int(rewards.get_redemption()) + int(qty))
    db['Rewards'] = rewards_dict

    # print(rewards_dict)
    # print(len(rewards_dict))
    current_session = shelve.open(get_db(), 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db(), 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    history_object = {}

    # SHOW NAME AND EXPIRY DATE OF VOUCHER
    # print(f'Name of voucher: {rewards.get_description()}\nExpiry date: {rewards.get_date_expire()}')
    # ADD INTO HISTORY OBJECT


    # ADD TO PERSISTENT STORAGE

    history = user.gethistory()
    rec = Rewards.History(rewards.get_name(), str(rewards.get_date_expire()))

    for x in history:
        if rec.get_description() == x.get_description():
            x.add_quantity(int(qty))
            print(x.get_quantity())
            break
    else:
        rec.add_quantity(int(qty))
        user.addHistory(rec)


    dbuser['Users'] = user_dict
    db.close()
    return render_template('rewards_user/redeemedRewards.html', redeemedPts=redeemedPts, points=remainingPts,
                           rewardPts=rewardPts,
                           qty=qty)


@endpoint.route("/rewards_ava")
# ALL COUPONS
def rewards_details(history=None):
    db = shelve.open(get_db(), 'w')

    db["points"] = 123456
    points = db['points']
    rewards_list = []
    history_list = []
    current_session = shelve.open(get_db(), 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db(), 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)

    history = user.gethistory()

    for x in history:
        for i in range(0, x.get_quantity()):
            records = x
            history_list.append(records)


    try:
        rewards_dict: dict = db['Rewards']
        history_dict: dict = db['History']

        for key in rewards_dict:
            rewards = rewards_dict.get(key)
            rewards_list.append(rewards)


    except:
        print('Creating new dict')


    db.close()

    return render_template("rewards_user/userRewards.html", rewards_list=rewards_list, points=points, today=today,
                           history_list=history_list, history=history)
#yr mom pretty