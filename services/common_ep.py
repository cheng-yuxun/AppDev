from flask import Blueprint, render_template, redirect, request, url_for, flash , Flask , Response , session
import shelve
import os.path
from services.admin.events_ep import events
from flask_mail import Mail , Message
from services.forms.form_acc import LoginForm , ForgetPasswordform
from services.forms.form_search import Search, EventFilter
from data.db_ep import get_db, create_db
from uuid import uuid4
from datetime import datetime, timedelta
import json
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
mail = Mail()
mail.init_app(app)
endpoint = Blueprint("base", __name__)

@endpoint.route("/", methods=["GET", "POST"])
def home_page():
    if os.path.isfile(f"{get_db()}.dat") is False:
        create_db()
    session["points"] = 123456
    db = shelve.open(get_db(), flag="c")
    events_dict: dict = db["Events"]
    products_dict: dict = db["Products"]
    sesh = db['current_session']
    try:
        user_id = sesh['user_id']
        user_dict: dict = db['Users']
        user = user_dict.get(user_id)
        eventcart: dict = user.getcart()
    except:
        user = ''
    db.close()
    events_list = []
    products_list = []
    eventfilter = EventFilter(request.form)
    if request.method == "GET":
        searchform = Search(request.form)
        if user == '':
            eventcart = {}
        for key in events_dict:
            events = events_dict.get(key)
            if events.get_status() == "Active" and events.get_uuid() not in eventcart:
                events_list.append(events)
        for key in products_dict:
            products = products_dict.get(key)
            if products.get_status() == 'Available':
                products_list.append(products)
    if request.method == "POST":
        searchform = Search(request.form)
        if searchform.search.data == "":
            return redirect(url_for("base.home_page"))
        else:
            query = searchform.search.data.upper().replace(" ", "")
            db = shelve.open(get_db(), "r")
            events_dict: dict = db["Events"]
            products_dict: dict = db["Products"]
            if user is None:
                eventcart = {}
            for key in events_dict:
                events = events_dict.get(key)
                if (
                    query == events.get_name().upper().replace(" ", "")
                    and events.get_status() == "Active" and events.get_uuid() not in eventcart
                ):
                    events_list.append(events)
            for key in products_dict:
                products = products_dict.get(key)
                if query == products.get_name().upper().replace(" ", "") and products.get_status() == 'Available':
                    products_list.append(products)
    try:
        event_active_keys: list = events_list[0:4]
        event_other_keys: list = events_list[4:]
        product_active_keys: list = products_list[0:4]
        product_other_keys: list = products_list[4:]
    except IndexError:
        event_active_keys = ""
        event_other_keys = ""
        product_active_keys = ""
        product_other_keys = ""
    return render_template(
        "common/home.html",
        event_active_keys=event_active_keys,
        event_other_keys=event_other_keys,
        product_active_keys=product_active_keys,
        product_other_keys=product_other_keys,
        searchform=searchform,
        count=len(events_list) + len(products_list),
        query=searchform.search.data,
        eventfilter=eventfilter,

    )


@endpoint.route('/LoginPage' , methods=['Get' , 'Post'])
def LoginPage(error=None , expirytime=None , oldpassword=None , forgetful_user=None , timeout_expiry = None):
    if os.path.isfile(f'{get_db()}.dat') is False:
        create_db()
    db = shelve.open(get_db(), 'c')
    login_form = LoginForm(request.form)
    ForgetPasswordForm = ForgetPasswordform(request.form)

    try:
        forgetful_user_dict = db['forgetful_user']
        for key in forgetful_user_dict:
            forgetful_user = key
            oldpassword = forgetful_user_dict[key]
    except:
        print("Error opening forgetpassword system db")

    expirytime_dict = {}
    forgetful_user_dict = {}
    try:
        if 'expirytime' in db:
            expirytime_dict =  db['expirytime']
            expirytime = expirytime_dict['expiry_time']
        else:
            db['expirytime'] = expirytime_dict

        if 'forgetful_user' in db:
            forgetful_user_dict = db['forgetful_user']

        else:
            db['forgetful_user'] = forgetful_user_dict

    except:
        print("Error opening forgetpassword system db ")


    if request.method == 'POST' and ForgetPasswordForm.validate():
        user_dict = {}

        try:
            if 'Users' in db:
                user_dict = db['Users']

            else:
                db['Users'] = user_dict


        except:
            print("Error with account database")

        else:
            for key in user_dict:
                user_email = user_dict.get(key).get_email()
                user_id = user_dict.get(key).get_uuid()
                if ForgetPasswordForm.Email.data == user_email:
                    oldpassword = user_dict.get(key).get_password()
                    temporary_password = str(uuid4())[:8]
                    user_dict.get(key).set_password(temporary_password)
                    starttime = datetime.now()
                    expirytimer = starttime + timedelta(minutes=1)
                    expirytime = expirytimer.strftime('%H:%M:%S')
                    forgetful_user = key
                    try:
                        msg = Message('Reset your password ', sender ='appdevprojectsss@gmail.com', recipients = [ForgetPasswordForm.Email.data])
                        msg.html = render_template('/emails/email.html' , temporary_password=temporary_password)
                        mail.send(msg)
                        expirytime_dict[user_id] = expirytime
                        forgetful_user_dict[forgetful_user] = oldpassword
                        db['forgetful_user'] = forgetful_user_dict
                        db['expirytime'] = expirytime_dict
                        db['Users'] = user_dict
                        flash('Email sent')
                        db.close()
                        return redirect(url_for('base.home_page'))
                    except:
                        flash("Error in sending mail, please check your connection" , 'error')
                        return redirect(url_for('base.home_page'))


            else:
                error='NoEmail'



    if 'timeout_expiry' in session:
            timeout_expiry = session['timeout_expiry']


    if request.method == 'POST' and login_form.validate():

        if 'Password_attempt' in session:
            pass
        else:
            session['Password_attempt'] = 1


        if session['Password_attempt'] == 5:
            error = 'timeout'

        else:
            user_id_dict = {}
            user_dict = {}
            admin_dict = {}
            try:
                if 'current_session' in db:
                    user_id_dict =  db['current_session']
                else:
                    db['current_session'] = user_id_dict
            except:
                print("Error opening session.db")


            try:
                if 'Users' in db:
                    user_dict = db['Users']

                else:
                    db['Users'] = user_dict

                if 'Admin' in db:
                    admin_dict = db['Admin']

                else:
                    db['Admin'] = admin_dict

            except:
                print("error in opening account database")
            for key in user_dict:
                object_info = user_dict[key]
                get_email = getattr(object_info , 'get_email')
                email = get_email()
                get_password= getattr(object_info , 'get_password')
                password = get_password()
                get_userid = getattr(object_info , 'get_uuid')
                user_id = get_userid()
                if login_form.username_or_email.data == email and login_form.password.data == password:
                    if 'Password_attempt' in session:
                        session.pop('Password_attempt' , None)

                    if 'timeout_expiry' in session:
                        session.pop('timeout_expiry' , None)
                    if not db['expirytime'].get(user_id):
                        if user_dict.get(key).get_status() == 'Active':
                            user_id_dict['user_id'] = user_id
                            db['current_session'] = user_id_dict
                            session['loggedin'] = 'user'
                            session['username'] = user_dict.get(key).get_username()
                            session.permanent = True
                            error = None
                            db.close()
                            return redirect(url_for('base.home_page'))

                        else:
                            error='deactivated'
                            break

                    else:
                        if user_dict.get(key).get_status() == 'Active':
                            user_id_dict['user_id'] = user_id
                            db['current_session'] = user_id_dict
                            session['loggedin'] = 'user'
                            session['username'] = user_dict.get(key).get_username()
                            session.permanent = True
                            error = None
                            db.close()
                            return redirect(url_for('auth.changepassword'))

                        else:
                            error='deactivated'
                            break

                elif login_form.username_or_email.data == email and login_form.password.data != password:
                    session['Password_attempt'] += 1
                    if session['Password_attempt'] == 5:
                         timeout_expiry = (datetime.now() + timedelta(minutes=5)).strftime('%H:%M:%S')
                         session['timeout_expiry'] = timeout_expiry

                    error = 'wrongpassword'
                    break

            else:
                for key in admin_dict:
                    object_info = admin_dict[key]
                    get_email = getattr(object_info , 'get_email')
                    email = get_email()
                    get_password= getattr(object_info , 'get_password')
                    password = get_password()
                    get_userid = getattr(object_info , 'get_uuid')
                    user_id = get_userid()
                    if login_form.username_or_email.data == email and login_form.password.data == password:
                        if 'Password_attempt' in session:
                            session.pop('Password_attempt' , None)

                        if 'timeout_expiry' in session:
                            session.pop('timeout_expiry' , None)
                        user_id_dict['user_id'] = user_id
                        db['current_session'] = user_id_dict
                        session['username'] = admin_dict.get(key).get_username()
                        session['loggedin'] = 'user'
                        session.permanent = True
                        db.close()
                        return redirect(url_for('admin.admin_frontpage'))

                    elif login_form.username_or_email.data == email and login_form.password.data != password:
                        session['Password_attempt'] += 1
                        if session['Password_attempt'] == 5:
                             timeout_expiry = (datetime.now() + timedelta(minutes=5)).strftime('%H:%M:%S')
                             session['timeout_expiry'] = timeout_expiry
                        error = 'wrongpassword'
                        break
                else:

                    for key in user_dict:
                        object_info = user_dict[key]
                        get_username = getattr(object_info , 'get_username')
                        username = get_username()
                        get_password= getattr(object_info , 'get_password')
                        password = get_password()
                        get_userid = getattr(object_info , 'get_uuid')
                        user_id = get_userid()
                        if login_form.username_or_email.data == username and login_form.password.data == password:
                            if 'Password_attempt' in session:
                                session.pop('Password_attempt' , None)

                            if 'timeout_expiry' in session:
                                session.pop('timeout_expiry' , None)
                            if not db['expirytime'].get(user_id):
                                if user_dict.get(key).get_status() == 'Active':
                                    user_id_dict['user_id'] = user_id
                                    db['current_session'] = user_id_dict
                                    session['loggedin'] = 'user'
                                    session['username'] = user_dict.get(key).get_username()
                                    session.permanent = True
                                    error = None
                                    db.close()
                                    return redirect(url_for('base.home_page'))

                                else:
                                    error='deactivated'
                                    break

                            else:
                                if user_dict.get(key).get_status() == 'Active':
                                    user_id_dict['user_id'] = user_id
                                    db['current_session'] = user_id_dict
                                    session['loggedin'] = 'user'
                                    session['username'] = user_dict.get(key).get_username()
                                    session.permanent = True
                                    error = None
                                    db.close()
                                    return redirect(url_for('auth.changepassword'))

                                else:
                                    error='deactivated'
                                    break
                    else:
                        for key in admin_dict:
                            object_info = admin_dict[key]
                            get_username = getattr(object_info , 'get_username')
                            username = get_username()
                            get_password= getattr(object_info , 'get_password')
                            password = get_password()
                            get_userid = getattr(object_info , 'get_uuid')
                            user_id = get_userid()
                            if login_form.username_or_email.data == username and login_form.password.data == password:
                                if 'Password_attempt' in session:
                                    session.pop('Password_attempt' , None)

                                if 'timeout_expiry' in session:
                                    session.pop('timeout_expiry' , None)
                                user_id_dict['user_id'] = user_id
                                db['current_session'] = user_id_dict
                                session['username'] = admin_dict.get(key).get_username()
                                session['loggedin'] = 'user'
                                session.permanent = True
                                db.close()
                                return redirect(url_for('admin.admin_frontpage'))


                        else:
                            registered = shelve.open(get_db() , 'r')
                            existing = registered['registered']
                            registered.close()
                            for key in existing:
                                if login_form.username_or_email.data == existing[key]:
                                    session['Password_attempt'] += 1
                                    if session['Password_attempt'] == 5:
                                         timeout_expiry = (datetime.now() + timedelta(minutes=5)).strftime('%H:%M:%S')
                                         session['timeout_expiry'] = timeout_expiry
                                    error = 'wrongpassword'
                                    break
                            else:
                                error = "NoAccountMade"




    return render_template('/common/LoginPage.html', form=login_form,error= error, form2=ForgetPasswordForm , expirytime=expirytime , oldpassword=oldpassword , forgetful_user=forgetful_user , timeout_expiry=timeout_expiry )



@endpoint.route('/generate_time')
def generate_time():
    def generator():
        while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S')})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    return Response(generator(), mimetype='text/event-stream')


@endpoint.route("/events_detail/<id>/", methods=["GET", "POST"])
def events_details(id):
    db = shelve.open(get_db(), "r")
    events_dict: dict = db["Events"]
    db.close()
    events_id = events_dict.get(id)
    print(f"--- Retrieving Event Key {events_id.get_uuid()} Data ---")
    searchform = Search(request.form)
    if request.method == "POST":
        return redirect(url_for("base.home_page"), code=307)
    return render_template(
        "common/events_detail.html",
        events_id=events_id,
        searchform=searchform,
    )


@endpoint.route("/products_detail/<id>/", methods=["GET", "POST"])
def products_details(id):
    db = shelve.open(get_db(), "r")
    products_dict: dict = db["Products"]
    db.close()
    products_id = products_dict.get(id)
    print(f"--- Retrieving Product Key {products_id.get_product_id()} Data ---")
    searchform = Search(request.form)
    if request.method == "POST":
        return redirect(url_for("base.home_page"), code=307)
    return render_template(
        "common/products_detail.html",
        products_id=products_id,
        searchform=searchform,
    )


@endpoint.route("/addcart/<id>", methods=["GET", "POST"])
def addcart(id):
    try:
        db = shelve.open(get_db(), "w")
        events_dict: dict = db["Events"]
        products_dict: dict = db['Products']
        session = db['current_session']
        user_id = session['user_id']
        user_dict: dict = db['Users']
        user = user_dict.get(user_id)
        if user is None:
            flash("Pls Sign Up or Log In", category="error")
            return redirect(url_for('base.home_page'))
        try:
            if id in events_dict:
                events_id = events_dict.get(id)
                user.addcart(events_id.get_uuid(), events_id)
                print(f"user{user.get_username()} ordered {user.getcart()}")
                ticket = events_id.get_sold() + 1
                events_id.set_sold(ticket)
                events_id.add_user(ticket, user.get_username())
                flash(f"{events_id.get_name()} has been successfully added to cart", category='success')
            elif id in products_dict:
                products_id = products_dict.get(id)
                user.addproductcart(str(uuid4())[:4], products_id, int(request.data.decode('UTF-8')))
                print(f"user {user.get_username()} ordered {user.getproductcart()}")
                flash(f"{products_id.get_name()} has been successfully added to cart", category='success')
                stonk = products_id.get_stock() - int(request.data.decode('UTF-8'))
                products_id.set_stock(stonk)
                ticket = products_id.get_sold() + int(request.data.decode('UTF-8'))
                products_id.set_sold(ticket)
                products_id.add_user(ticket, user.get_username())
            db["Products"] = products_dict
            db["Events"] = events_dict
            db["Users"] = user_dict
        except:
            pass
        db.close()
    except:
        pass
    return redirect(url_for('base.home_page'))

@endpoint.route('/cancelevent/<id>', methods=['GET', 'POST'])
def cancelevent(id):
    db = shelve.open(get_db(), "w")
    events_dict: dict = db["Events"]
    session = db['current_session']
    user_id = session['user_id']
    user_dict: dict = db['Users']
    user = user_dict.get(user_id)
    count = 1
    participants = {}
    if id in events_dict:
        events_id = events_dict.get(id)
        print(f"user {user.get_username()} cancelled {user.getcart()}")
        ticket = events_id.get_sold() - 1
        events_id.set_sold(ticket)
        flash(f"You have cancelled your reservation for {events_id.get_name()}", category='success')

        user.getcart().pop(id)
        for key in events_id.get_user():
            if events_id.get_user()[key] != user.get_username():
                participants[count] = events_id.get_user()[key]
                count += 1
        events_id.set_user(participants)
    db["Events"] = events_dict
    db["Users"] = user_dict
    db.close()
    return redirect(url_for('base.cart'))



@endpoint.route("/eventfilter", methods=["GET", "POST"])
def eventfilter():
    eventfilter = EventFilter(request.form)
    searchform = Search(request.form)
    db = shelve.open(get_db(), "r")
    events_dict: dict = db["Events"]
    sesh = db['current_session']
    cart = {}
    try:
        user_id = sesh['user_id']
        user_dict: dict = db['Users']
        user = user_dict.get(user_id)
        cart: dict = user.getcart()
        print(f'this is cart {cart}')
    except:
        user = ''
        cart = {}
    db.close()
    events_list = []
    
    if user is None:
        print(f'user is none')
        cart = {}

    def filter(events):
        if events not in events_list and events.get_uuid() not in cart and events.get_status() == 'Active':
            events_list.append(events)

    for key in events_dict:
        events = events_dict.get(key)

        if request.form.get("onsitecheck") is not None or request.form.get("livestreamcheck") is not None:
            if events.get_category() == request.form.get("onsitecheck") or events.get_category() == request.form.get("livestreamcheck"):
                if eventfilter.start_date.data is not None and eventfilter.end_date.data is not None:
                    if eventfilter.start_date.data <= events.get_date() <= eventfilter.end_date.data:
                        filter(events)
                else:
                    filter(events)
        else:
            if eventfilter.start_date.data is not None and eventfilter.end_date.data is not None:
                if eventfilter.start_date.data <= events.get_date() <= eventfilter.end_date.data:
                    filter(events)
            else:
                return redirect(url_for('base.home_page'))

    try:
        event_active_keys: list = events_list[0:4]
        event_other_keys: list = events_list[4:]
    except IndexError:
        event_active_keys = ""
        event_other_keys = ""
    return render_template(
        "common/result.html",
        eventfilter=eventfilter,
        searchform=searchform,
        events_list=events_list,
        event_active_keys=event_active_keys,
        event_other_keys=event_other_keys,
        p='no',
        e='yes'

    )

@endpoint.route("/productfilter", methods=["GET", "POST"])
def productfilter():
    eventfilter = EventFilter(request.form)
    searchform = Search(request.form)
    db = shelve.open(get_db(), "r")
    products_dict: dict = db['Products']
    sesh = db['current_session']
    cart = {}
    try:
        user_id = sesh['user_id']
        user_dict: dict = db['Users']
        user = user_dict.get(user_id)
        cart: dict = user.getcart()
    except:
        pass
    db.close()
    events_list = []
    products_list = []

    def filter(products):
        if products not in products_list and products.get_status() == 'Available':
            products_list.append(products)

    for key in products_dict:
        products = products_dict.get(key)
        if request.form.get("shirtcheck") is not None or request.form.get("footwearcheck") is not None or request.form.get("pantscheck") is not None:
            if products.get_ptype() == request.form.get("shirtcheck") or products.get_ptype() == request.form.get("footwearcheck") or products.get_ptype() == request.form.get("pantscheck"):
                filter(products)
        else:
            return redirect(url_for('base.home_page'))
    try:
        product_active_keys: list = products_list[0:4]
        product_other_keys: list = products_list[4:]
    except IndexError:
        product_active_keys = ""
        product_other_keys = ""
    print(events_list)
    return render_template(
        "common/result.html",
        eventfilter=eventfilter,
        searchform=searchform,
        product_active_keys=product_active_keys,
        product_other_keys=product_other_keys,
        p='yes',
        e='no'

    )


# cart route in common ep

@endpoint.route('/cart', methods=['GET', 'POST'])
def cart():
    searchform = Search(request.form)
    db = shelve.open(get_db(), 'r')
    session = db['current_session']
    user_id = session['user_id']
    user_dict: dict = db['Users']
    user = user_dict.get(user_id)
    print(f'this is user {user}')
    if user is None:
        flash('Pls login or sign up', category='error')
        try:
            return redirect(url_for(request.referrer))
        except:
            return redirect(url_for('base.home_page'))
    db.close()
    event_list = []
    eventcart = []
    eventhistory = []
    productcart = []
    print(f'this is event cart {user.getcart()}')
    p_cart = user.getproductcart()
    total = 0
    eventotal = 0
    try:
        for i in user.getcart():
            event = user.getcart().get(i)
            event_list.append(events)
            if event.get_category() == 'Onsite':
                eventotal += event.get_price()
            if datetime.strptime(f'{event.get_date()} {event.get_end_time()}', "%Y-%m-%d %H:%M:%S") < datetime.now():
                eventhistory.append(event)
            elif datetime.strptime(f'{event.get_date()} {event.get_end_time()}', "%Y-%m-%d %H:%M:%S") > datetime.now():
                eventcart.append(event)
        # for i in user.getproductcart():
        #     p_cart[i] = user.getproductcart().get(i)
        for i in p_cart:
            total += (int(p_cart[i][1]) * int(p_cart[i][0].get_price()))
        
        
    except:
        pass
    return render_template('common/cart.html',
    user=user,
    searchform=searchform,
    eventcart=eventcart,
    productcart=productcart,
    total=total,
    eventotal=eventotal,
    eventhistory=eventhistory,
    p_cart=p_cart,
    event_list=event_list)

