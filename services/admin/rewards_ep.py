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

endpoint = Blueprint("rewards", __name__)

#Admin
@endpoint.route('/create_rewards', methods=['GET', 'POST'])
def create():
    create_form = CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        rewards_dict = {}
        db = shelve.open(get_db(), 'c')
        try:
            rewards_dict = db['Rewards']
            print(len(rewards_dict))
        except:
            print("Error in retrieving Rewards from Rewards.db.")

        # COMPARE DATES
        # START DATE MUST BE MORE THAN CURRENT DATE
        # EXPIRY DATE MUST BE MORE THAN START DATE
        if (create_form.date_start.data > today and create_form.date_start.data < create_form.date_expire.data):
            reward = Rewards.Rewards(create_form.name.data, create_form.points.data, create_form.category.data,
                                     create_form.redemption.data, create_form.code.data,
                                     create_form.date_start.data, create_form.date_expire.data,
                                     create_form.description.data,
                                     create_form.picture.data)

            uploaded_file = CreateForm(request.files)
            f = uploaded_file.picture.data
            if f != None:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['Upload_FOLDER'], filename))
                reward.set_picture(filename)
            rewards_dict[reward.get_uuid()] = reward
            db['Rewards'] = rewards_dict
            db.close()
            return redirect(url_for("rewards.view", code=302))
        else:
            if (create_form.date_start.data <= today):
                flash(f'Start date must be after {today}!')

            elif (create_form.date_start.data >= create_form.date_expire.data):
                flash(f'Expiry date must be after {create_form.date_start.data}!')

    return render_template('admin/rewards/createRewards.html', form=create_form)


@endpoint.route('/view_rewards', methods=['GET', 'POST'])
def view():
    rewards_dict = {}
    db = shelve.open(get_db(), 'r')
    rewards_dict = db['Rewards']
    db.close()

    rewards_list = []
    for key in rewards_dict:
        rewards = rewards_dict.get(key)
        rewards_list.append(rewards)
        # print(rewards.get_status() + '\n')

    # print(len(rewards_dict))
    return render_template('admin/rewards/viewRewards.html', count=len(rewards_list), rewards_list=rewards_list)


@endpoint.route('/deleteRewards/<id>', methods=['POST'])
def delete_rewards(id):
    while True:
        rewards_dict = {}
        db = shelve.open(get_db(), 'w')
        rewards_dict = db['Rewards']
        rewards_dict.pop(id)
        db['Rewards'] = rewards_dict
        db.close()

        return redirect(url_for("rewards.view"))


@endpoint.route('/updateRewards/<id>/', methods=['GET', 'POST'])
def update_rewards(id):
    update_rewards = CreateForm(request.form)
    if request.method == 'POST' and update_rewards.validate():
        rewards_dict = {}
        db = shelve.open(get_db(), 'w')
        rewards_dict = db['Rewards']

        # COMPARE DATES
        # START DATE MUST BE MORE THAN CURRENT DATE
        # EXPIRY DATE MUST BE MORE THAN START DATE

        if (
                update_rewards.date_start.data > today and update_rewards.date_start.data < update_rewards.date_expire.data):
            reward = rewards_dict.get(id)
            reward.set_name(update_rewards.name.data)
            reward.set_points(update_rewards.points.data)
            reward.set_category(update_rewards.category.data)
            reward.set_redemption(update_rewards.redemption.data)
            reward.set_code(update_rewards.code.data)
            reward.set_description(update_rewards.description.data)
            reward.set_date_start(update_rewards.date_start.data)
            reward.set_date_expire(update_rewards.date_expire.data)
            reward.set_picture(update_rewards.picture.data)

            db['Rewards'] = rewards_dict
            db.close()
            return redirect(url_for("rewards.view", code=302))
        else:
            if (update_rewards.date_start.data <= today):
                flash(f'Start date must be after {today}!')

            elif (update_rewards.date_start.data >= update_rewards.date_expire.data):
                flash(f'Expiry date must be after {update_rewards.date_start.data}!')

        return render_template('admin/rewards/updateRewards.html', form=update_rewards)
    else:
        rewards_dict = {}
        db = shelve.open(get_db(), 'r')
        rewards_dict = db['Rewards']
        db.close()

        reward = rewards_dict.get(id)
        update_rewards.name.data = reward.get_name()
        update_rewards.points.data = reward.get_points()
        update_rewards.category.data = reward.get_category()
        update_rewards.redemption.data = reward.get_redemption()
        update_rewards.code.data = reward.get_code()
        update_rewards.description.data = reward.get_description()
        update_rewards.date_start.data = reward.get_date_start()
        update_rewards.date_expire.data = reward.get_date_expire()
        update_rewards.picture.data = reward.get_picture()

        return render_template('admin/rewards/updateRewards.html', form=update_rewards)


@endpoint.route("/rewards_status/<id>", methods=['POST'])
def availability(id):
    db = shelve.open(get_db(), 'w')
    rewards_dict: dict = db['Rewards']
    rewards = rewards_dict.get(id)
    if rewards.get_status() == 'Available':
        print(f"Event Key {rewards.get_uuid()} is inactivated!")
        rewards.set_status('Unavailable')
    else:
        print(f"Event Key {rewards.get_uuid()} is activated!")
        rewards.set_status('Available')
    db['Rewards'] = rewards_dict
    db.close()
    return redirect(url_for("rewards.view"))


# @app.route("/createA", methods=['GET', 'POST'])  # Process form data
# def create_achievement():
#     create_achievements = CreateAchievements(request.form)
#     if request.method == 'POST' and create_achievements.validate():
#         db = shelve.open(DBDIR)
#         uuid = str(uuid4())[:8]
#         db[uuid] = {
#             "id": uuid,
#             "subject": create_achievements.subject.data,
#             "content": create_achievements.content.data,
#             "date_created": create_achievements.date_created,
#             "date_updated": create_achievements.date_updated,
#         }
#         db.close()  # to prevent data corruption/loss of data
#         return redirect(url_for("view_achievement", code=302))
#     return render_template("createAchievements.html")
#
#
# @app.route("/viewA", methods=['GET', 'POST'])
# def view_achievement():
#     db = shelve.open(DBDIR)
#     notes = dict(db)
#     db.close()
#     return render_template("viewAchievements.html", notes=notes)
#