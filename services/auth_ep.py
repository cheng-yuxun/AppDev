from flask import Blueprint, render_template, redirect, url_for, request , Flask , flash , session , Response
from flask_mail import Mail
import shelve
from data.db_ep import get_db
from data.Person import Admin, User
from services.forms.form_acc import SignUpForm, SignUpFormPhone, UpdateProfile , ChangeEmail ,  AddPhoneNumber , ChangePhoneNumber ,  ChangePassword , PaymentMethod , LanguageForm , ForgetPasswordform
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os , json , time
app = Flask(__name__)
Upload_Folder = 'static/media/profilepic/'
app.config['Upload_FOLDER'] = Upload_Folder
app.config['SECRET_KEY'] = 'abcd'


endpoint = Blueprint("auth", __name__)
basedir = os.getcwd()


# account management ep from here
@endpoint.route('/SignUp' , methods=['Get' , 'Post'])
@endpoint.route('/SignUp/<error>' , methods=['Get' , 'Post'])

def sign_up(error = None , submit=None):
    sign_up_form = SignUpForm(request.form)
    existing = {}
    Accounts_created_dict = {}
    user_dict ={}
    admin_dict = {}
    db = shelve.open(get_db() , 'c')
    try:
        if 'registered' in db:
            existing =  db['registered']
        else:
            db['registered'] = existing

    except:
        print("Error in opening registered.db")

    try:
        if 'Accounts_created' in db:
            Accounts_created_dict = db['Accounts_created']

        else:
            db['Accounts_created'] = Accounts_created_dict

    except:
        print("Error in opening accounts created.db")

    try:
        if 'Users' in db:
            user_dict = db['Users']

        else:
            db['Users'] = user_dict

        if 'Admin' in db:
            admin_dict = db['Admin']
        else:
            db['Admin'] = {}

    except:
        print("Error with account database")

    if request.method == "POST" and sign_up_form.validate():
        if sign_up_form.Switching.data not in existing:
            submit = None
            if "admin.com" in str(sign_up_form.Switching.data):
                admin_dict = {}
                if "Admin" in db:
                    admin_dict = db['Admin']
                admin = Admin(sign_up_form.username.data , sign_up_form.password.data , sign_up_form.birthdate.data)
                admin.set_email(sign_up_form.Switching.data)
                admin_dict[admin.get_uuid()] = admin
                existing[admin.get_email()] = admin.get_username()
                db['registered'] = existing
                db['Admin'] = admin_dict
                db.close()
                return redirect('/')
            else:
                user_dict = {}
                db = shelve.open(get_db() , 'c')
                user_dict = db['Users']
                userdetails = User(sign_up_form.username.data , sign_up_form.password.data , sign_up_form.birthdate.data)
                user_dict[userdetails.get_uuid()] = userdetails
                userdetails.set_email(sign_up_form.Switching.data)
                existing[userdetails.get_email()] = userdetails.get_username()
                db['registered'] = existing
                db['Users'] = user_dict
                if datetime.now().strftime('%m/%d/%y') in Accounts_created_dict:
                    Accounts_created_dict[datetime.now().strftime('%m/%d/%y')] += 1

                else:
                    Accounts_created_dict[datetime.now().strftime('%m/%d/%y')] = 1

                db['Accounts_created'] = Accounts_created_dict
                db.close()
                return redirect('/')


        else:
            error = True

    elif request.method == 'POST':
        submit = 'submit'

    return render_template('/auth/SignUp.html' , form=sign_up_form , error= error , submit=submit)




@endpoint.route('/signout')
def signout():
    session.pop('username' , None)
    session.pop('loggedin' , None)
    return redirect(url_for("base.home_page"))


@endpoint.route('/Profile')
def show_profile(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db())
    user_dict = dbuser['Users']
    dbuser.close()
    user_object = user_dict[user_id]
    get_username = getattr(user_object , 'get_username')
    userprofile_name = get_username()
    get_ABoutMe = getattr(user_object , 'get_AboutMe')
    userprofile_AboutMe = get_ABoutMe()
    get_birthdate = getattr(user_object , 'get_birthdate')
    userprofile_birthdate = get_birthdate()
    get_image = getattr(user_object , 'get_image')
    userprofile_image = get_image()

    return render_template('/auth/MyProfile.html', loggedin=loggedin , userprofile_name = userprofile_name , userprofile_birthdate=userprofile_birthdate , userprofile_AboutMe=userprofile_AboutMe , userprofile_image=userprofile_image)


@endpoint.route('/UpdateProfile' , methods=['GET', 'POST'])
def update_profile(error=None ):
    current_session = shelve.open(get_db() , 'r')
    session_dict = current_session['current_session']
    user_id = session_dict['user_id']
    current_session.close()
    UpdateProfileForm = UpdateProfile(request.form)
    UpdateProfileFormFile = UpdateProfile(request.files)
    if request.method == "POST" and UpdateProfileForm.validate() and UpdateProfileFormFile.file.validate(request.files):
        dbuser = shelve.open(get_db() , 'w')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        user.set_username(UpdateProfileForm.usernamefield.data)
        user.set_birthdate(UpdateProfileForm.birthdatefield.data)
        user.set_AboutMe(UpdateProfileForm.AboutMefield.data)
        f = UpdateProfileFormFile.file.data
        if f != None:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['Upload_FOLDER'] , filename))
            user.set_image(filename)
        session['username'] = user_dict.get(user_id).get_username()
        dbuser['Users'] = user_dict
        dbuser.close()
        return redirect(url_for('auth.show_profile'))

    elif request.method == "POST" and not UpdateProfileFormFile.file.validate(request.files):
        error = True
        dbuser = shelve.open(get_db() , 'r')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        userprofile_name = user.get_username()
        userprofile_birthdate = user.get_birthdate()
        userprofile_AboutMe = user.get_AboutMe()
        userprofile_image = user.get_image()
        UpdateProfileForm.usernamefield.data = userprofile_name
        UpdateProfileForm.birthdatefield.data = userprofile_birthdate
        UpdateProfileForm.AboutMefield.data = userprofile_AboutMe
        UpdateProfileFormFile.file.data = userprofile_image
        dbuser.close()


    else:
        dbuser = shelve.open(get_db() , 'r')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        userprofile_name = user.get_username()
        userprofile_birthdate = user.get_birthdate()
        userprofile_AboutMe = user.get_AboutMe()
        userprofile_image = user.get_image()
        UpdateProfileForm.usernamefield.data = userprofile_name
        UpdateProfileForm.birthdatefield.data = userprofile_birthdate
        UpdateProfileForm.AboutMefield.data = userprofile_AboutMe
        UpdateProfileFormFile.file.data = userprofile_image
        dbuser.close()

    return render_template('/auth/UpdateProfile.html' , form=UpdateProfileForm , userprofile_name = userprofile_name , userprofile_birthdate=userprofile_birthdate , userprofile_image = userprofile_image , error=error )




@endpoint.route('/AccountDetails')
def AccountDetails(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    userprofile_email = user.get_email()
    userprofile_phonenumber = user.get_phonenumber()

    dbuser.close()
    return render_template('/auth/AccountDetails.html' , loggedin=loggedin , userprofile_name=userprofile_name , userprofile_email=userprofile_email , userprofile_phonenumber = userprofile_phonenumber)



@endpoint.route('/ChangeEmail' , methods= ['GET' , 'POST'])
def changeEmail(loggedin = 'user' , existing = None):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    ChangeEmailForm = ChangeEmail(request.form)
    if request.method == 'POST' and ChangeEmailForm.validate():
        dbuser = shelve.open(get_db() , 'r')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        userprofile_email = user.get_email()
        userprofile_name = user.get_username()
        ChangeEmailForm.Email.data = userprofile_email
        dbuser.close()
        dbuser = shelve.open(get_db() , 'w')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        userprofile_name = user.get_username()
        for key in user_dict:
            user_object = user_dict[key]
            user_getemail = getattr(user_object, 'get_email')
            user_email = user_getemail()
            if ChangeEmailForm.NewEmail.data == user_email:
                existing = 'existing'
                break

        else:
            if str(ChangeEmailForm.NewEmail.data).endswith('admin.com'):
                existing = 'admin'

            else:
                existing = None
                user.set_email(ChangeEmailForm.NewEmail.data)
                dbuser['Users'] = user_dict
                dbuser.close()
                return redirect(url_for('auth.AccountDetails'))
    else:
        dbuser = shelve.open(get_db() , 'r')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        userprofile_email = user.get_email()
        userprofile_name = user.get_username()
        ChangeEmailForm.Email.data = userprofile_email
        dbuser.close()

    return render_template('/auth/ChangeEmail.html', form=ChangeEmailForm , loggedin=loggedin , userprofile_name=userprofile_name , existing=existing)


@endpoint.route('/ChangePhoneNumber' , methods=['GET' , 'POST'])
def changephonenumber(existing = None):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_phonenumber = user.get_phonenumber()
    dbuser.close()
    if userprofile_phonenumber == None:
        PhoneNumberForm = AddPhoneNumber(request.form)
        if request.method == "POST" and PhoneNumberForm.validate():
            dbuser = shelve.open(get_db() , 'w')
            user_dict = dbuser['Users']
            user = user_dict.get(user_id)
            user.set_phonenumber(PhoneNumberForm.Phonenumber.data)
            dbuser['Users'] = user_dict
            dbuser.close()
            return redirect(url_for('auth.AccountDetails'))

    else:
        PhoneNumberForm = ChangePhoneNumber(request.form)
        if request.method == "POST" and PhoneNumberForm.validate():
            dbuser = shelve.open(get_db() , 'r')
            user_dict = dbuser['Users']
            user = user_dict.get(user_id)
            PhoneNumberForm.Phonenumber.data = user.get_phonenumber()
            dbuser.close()
            dbuser = shelve.open(get_db() , 'w')
            user_dict = dbuser['Users']
            user = user_dict.get(user_id)
            if PhoneNumberForm.NewPhonenumber.data == user.get_phonenumber():
                existing = 'SamePhoneNumber'

            else:
                existing = None
                user.set_phonenumber(PhoneNumberForm.NewPhonenumber.data)
                dbuser['Users'] = user_dict
                dbuser.close()
                return redirect(url_for('auth.AccountDetails'))
        else:
            dbuser = shelve.open(get_db() , 'r')
            user_dict = dbuser['Users']
            user = user_dict.get(user_id)
            PhoneNumberForm.Phonenumber.data = user.get_phonenumber()
            dbuser.close()

    return render_template('/auth/ChangePhoneNumber.html' , form=PhoneNumberForm , existing=existing , userprofile_phonenumber = userprofile_phonenumber)



@endpoint.route('/changepassword' , methods=['GET' , 'POST'])
def changepassword(loggedin = 'user' , error= None):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    userprofile_password = user.get_password()
    dbuser.close()
    PasswordForm = ChangePassword(request.form)
    if request.method == "POST" and PasswordForm.validate():
        if PasswordForm.CurrentPassword.data != userprofile_password:
            error = 'Wrongpassword'

        else:
            if PasswordForm.NewPassword.data == PasswordForm.CurrentPassword.data:
                error = 'Samepassword'

            else:
                error = None
                db = shelve.open(get_db() , 'w')
                user_dict = db['Users']
                user = user_dict.get(user_id)
                user.set_password(PasswordForm.NewPassword.data)
                db['expirytime'] = {}
                db['forgetful_user'] = {}
                db['Users'] = user_dict
                db.close()
                flash('Successfully changed your password')
                return redirect(url_for('auth.AccountDetails'))

    return render_template('/auth/ChangePassword.html' , loggedin=loggedin , error=error , form=PasswordForm , userprofile_name=userprofile_name)


@endpoint.route('/PaymentDetails')
def PaymentDetails(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    userprofile_creditcard = user.get_creditcard().get_card()
    userprofile_creditcardno = user.get_creditcard().get_cardno()
    dbuser.close()

    return render_template('/auth/PaymentDetails.html' , loggedin=loggedin , userprofile_name=userprofile_name , userprofile_creditcard= userprofile_creditcard , userprofile_creditcardno=userprofile_creditcardno)


@endpoint.route('/EditPaymentMethod' , methods=['GET' , 'POST'])
def editpaymentmethod(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    dbuser.close()
    PaymentMethodForm = PaymentMethod(request.form)
    if request.method == 'POST' and PaymentMethodForm.validate():
        print(PaymentMethodForm.Expirationdate.data)
        dbuser = shelve.open(get_db() , 'w')
        user_dict = dbuser['Users']
        user = user_dict.get(user_id)
        user.get_creditcard().set_card(PaymentMethodForm.Cardtype.data)
        user.get_creditcard().set_cardno(PaymentMethodForm.Cardnumber.data)
        user.get_creditcard().set_expirationdate(PaymentMethodForm.Expirationdate.data)
        user.get_creditcard().set_ccv(PaymentMethodForm.CCV.data)
        dbuser['Users'] = user_dict
        dbuser.close()
        return redirect(url_for('auth.PaymentDetails'))

    return render_template('/auth/PaymentMethodForm.html' , form=PaymentMethodForm , loggedin=loggedin , userprofile_name=userprofile_name )

@endpoint.route('/DeletePaymentMethod')
def DeletePaymentMethod():
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    user.get_creditcard().reset()
    dbuser['Users'] = user_dict
    dbuser.close()
    return redirect(url_for('auth.PaymentDetails'))



@endpoint.route('/Language' , methods=['GET' , 'POST'])
def Language(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    dbuser.close()
    Languageform = LanguageForm(request.form)
    if request.method == 'POST':
        pass



    return render_template('/auth/Language.html' , loggedin=loggedin , userprofile_name=userprofile_name , form=Languageform)


@endpoint.route('/Friends')
def Friends(loggedin='user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    userprofile_friends = user.get_friends()
    userprofile_friendcount = len(user.get_friends())
    userprofile_friendrequest = user.get_friendrequest()
    dbuser.close()


    return render_template("/auth/Friends/Friends.html" , userprofile_name=userprofile_name , userprofile_friends=userprofile_friends , userprofile_friendcount=userprofile_friendcount , userprofile_friendrequest=userprofile_friendrequest , user_dict=user_dict , loggedin=loggedin)


@endpoint.route('/AddFriend')
def AddFriend(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_friendrequest = user.get_friendrequest()
    userprofile_name = user.get_username()
    dbuser.close()

    return render_template('/auth/Friends/AddFriends.html' , loggedin=loggedin , userprofile_name=userprofile_name , user_dict = user_dict , current_user = user_id , userprofile_friendrequest=userprofile_friendrequest)


@endpoint.route('/FriendProfile/<id>')
def FriendProfile(id, loggedin= 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    Friend = user_dict.get(id)
    dbuser.close()
    return render_template('/auth/Friends/FriendProfile.html' , loggedin=loggedin , userprofile_name=userprofile_name , Friend=Friend , user=user , current_user = user_id)


@endpoint.route('/AddingFriends/<id>')
def AddingFriends(id):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    Friend = user_dict.get(id)
    if user_id not in Friend.get_friendrequest():
        Friend.set_friendrequest(user_id)

    else:
        Friend.remove_friendrequest(user_id)

    dbuser['Users'] = user_dict
    dbuser.close()

    return redirect(url_for('auth.AddFriend'))


@endpoint.route('/PendingRequest')
def PendingRequest(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_name = user.get_username()
    userprofile_friendrequest = user.get_friendrequest()
    dbuser.close()

    return render_template('/auth/Friends/PendingRequest.html' , loggedin=loggedin , userprofile_name=userprofile_name , userprofile_friendrequest=userprofile_friendrequest , user_dict=user_dict)


@endpoint.route('/AcceptFriendRequest/<id>')
def AcceptFriendRequest(id):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    user.set_friends(id)
    user.remove_friendrequest(id)
    Friend = user_dict.get(id)
    Friend.set_friends(user_id)
    dbuser['Users'] = user_dict
    dbuser.close()

    return redirect(url_for('auth.PendingRequest'))

@endpoint.route('/RejectFriendRequest/<id>')
def RejectFriendRequest(id):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    user.remove_friendrequest(id)
    dbuser['Users'] = user_dict
    dbuser.close()
    return redirect(url_for('auth.PendingRequest'))

@endpoint.route('/RemoveFriend')
def RemoveFriend(loggedin = 'user'):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    userprofile_friendrequest = user.get_friendrequest()
    userprofile_name = user.get_username()
    userprofile_friends = user.get_friends()
    userprofile_friendcount = len(user.get_friends())
    dbuser.close()

    return render_template('/auth/Friends/RemoveFriend.html' , loggedin=loggedin , userprofile_name=userprofile_name , userprofile_friendrequest=userprofile_friendrequest , user_dict=user_dict , userprofile_friends=userprofile_friends , userprofile_friendcount=userprofile_friendcount)

@endpoint.route('/RemovingFriend/<id>')
def RemovingFriend(id):
    current_session = shelve.open(get_db() , 'r')
    session = current_session['current_session']
    user_id = session['user_id']
    current_session.close()
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(user_id)
    user.remove_friends(id)
    Friend =user_dict.get(id)
    Friend.remove_friends(user_id)
    dbuser['Users'] = user_dict
    dbuser.close()

    return redirect(url_for('auth.RemoveFriend'))




@endpoint.route('/UserDetails')
def UserDetails():
    dbuser = shelve.open(get_db() , 'r')
    user_dict = dbuser['Users']
    return render_template("/admin/users/UserDetails.html" , user_dict=user_dict  )



@endpoint.route('/DeactivateAccount/<id>')
def DeactivateAccount(id):
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(id)
    user.set_status('Deactivated')
    dbuser['Users'] = user_dict
    dbuser.close()
    return redirect(url_for('auth.UserDetails'))


@endpoint.route('/ReactivateAccount/<id>')
def ReactivateAccount(id):
    dbuser = shelve.open(get_db() , 'w')
    user_dict = dbuser['Users']
    user = user_dict.get(id)
    user.set_status('Active')
    dbuser['Users'] = user_dict
    dbuser.close()
    return redirect(url_for('auth.UserDetails'))



@endpoint.route('/passwordexpire')
def passwordexpire():
    db =  shelve.open(get_db() , 'w')
    user_dict = db['Users']
    forgetful_user_dict = db['forgetful_user']
    for key in forgetful_user_dict:
        user = key
        oldpassword = forgetful_user_dict[key]
        forgetful_user = user_dict.get(user)
        forgetful_user.set_password(oldpassword)
        forgetful_user_dict.pop(key)
        break

    db['Users'] = user_dict
    db['forgetful_user'] = forgetful_user_dict
    db['expirytime'] = {}
    db.close()


    return redirect(url_for('base.LoginPage'))




@endpoint.route('/timeoutexpire')
def timeoutexpire():
    session.pop('Password_attempt' , None)
    session.pop('timeout_expiry' , None)
    return redirect(url_for('base.home_page'))


@endpoint.route('/PopularityGraph')
def PopularityGraph():
    time = datetime.now().strftime('%m/%d/%y')
    db = shelve.open(get_db() , 'r')
    Accounts_created_dict = {}
    try:
        if 'Accounts_created' in db:
            Accounts_created_dict = db['Accounts_created']

        else:
            db['Accounts_created'] = Accounts_created_dict

    except:
        print("Error in opening accounts created.db")


    return render_template('/admin/users/PopularityGraph.html' , Accounts_created_dict = Accounts_created_dict , time=time)



@endpoint.route('/generate_graph')
def generate_graph():
    def generator():
        while True:
            db = shelve.open(get_db() , 'w')
            Accounts_created_dict = db['Accounts_created']
            if datetime.now().strftime('%m/%d/%y') in Accounts_created_dict:
                pass
            else:
                Accounts_created_dict[datetime.now().strftime('%m/%d/%y')] = 0
            json_graphdata = json.dumps(
                {'time': datetime.now().strftime('%m/%d/%y') , 'Accounts_created' : Accounts_created_dict.get(datetime.now().strftime('%m/%d/%y'))})
            yield f"data:{json_graphdata}\n\n"
            db['Accounts_created'] = Accounts_created_dict

            db.close()

    return Response(generator() , mimetype='text/event-stream')
