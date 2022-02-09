from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from services.forms.form_rewards import CreateForm
from datetime import date
import shelve
from data import Rewards
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
    db.close()
    rewards = rewards_dict.get(id)
    points = session['points']
    session['id'] = id
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

    points = session['points']

    # qty = request.form['count']
    # rewardPts = rewards.get_points()
    # print(rewardPts, qty)

    # if(request.method == 'POST'):
    rewards = rewards_dict.get(session['id'])
    # rewards = rewards_dict.get(id)
    redeemedPts = int(rewardPts) * int(qty)
    remainingPts = points - redeemedPts
    session['points'] = remainingPts
    rewards.set_redemption(int(rewards.get_redemption()) + int(qty))
    db['Rewards'] = rewards_dict

    # print(rewards_dict)
    # print(len(rewards_dict))

    for i in range(int(qty)):
        # SHOW NAME AND EXPIRY DATE OF VOUCHER
        # print(f'Name of voucher: {rewards.get_description()}\nExpiry date: {rewards.get_date_expire()}')
        # ADD INTO HISTORY OBJECT
        rec = Rewards.History(rewards.get_description(), str(rewards.get_date_expire()))
        # ADD TO PERSISTENT STORAGE
        countKey = len(history_dict)
        history_dict[countKey] = rec
    db['History'] = history_dict
    print(history_dict)
    db.close()
    return render_template('rewards_user/redeemedRewards.html', redeemedPts=redeemedPts, points=remainingPts, rewardPts=rewardPts,
                           qty=qty)

@endpoint.route("/rewards_ava")
# ALL COUPONS
def rewards_details():
    db = shelve.open(get_db(), 'w')
    points = session['points']
    session["points"] = 123456
    rewards_list = []
    history_list = []

    
    try:
        rewards_dict: dict = db['Rewards']
        history_dict: dict = db['History']
        for key in rewards_dict:
            rewards = rewards_dict.get(key)
            rewards_list.append(rewards)

        for key in history_dict:
            records = history_dict.get(key)
            history_list.append(records)
    except:
        print('Creating new dict')
        db['History'] = {}
        history_dict = db['History']
        

    return render_template("rewards_user/userRewards.html", rewards_list=rewards_list, points=points, today=today,
                           history_list=history_list)