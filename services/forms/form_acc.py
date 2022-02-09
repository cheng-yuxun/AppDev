from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators , BooleanField , IntegerField , HiddenField , PasswordField , ValidationError
from wtforms.fields import EmailField, DateField
from flask_wtf.file import FileField , FileAllowed
from datetime import datetime, timedelta



def date_validator(form , field):
    now = datetime.now()

    if now.year - field.data.year < 12 or now.year - field.data.year > 110:
        raise ValidationError('Enter a valid age')

    elif now.year - field.data.year == 12 or now.year - field.data.year == 110:
        if now.month < field.data.month:
            raise  ValidationError('Enter a valid age')

        elif now.month == field.data.month:
            if now.day < field.data.day:
                raise  ValidationError('Enter a valid age')




def card_expiry(form , field):
    year = (field.data[3:])
    month = (field.data[:2])
    now = datetime.now()
    current_year = str(now.year)
    calc_current_year = int(current_year[2:])
    if calc_current_year > int(year):
        raise ValidationError("Your card has expired")

    elif calc_current_year == int(year):
        if now.month > int(month):
            raise ValidationError("Your card has expired")



class SignUpForm(Form):
    username = StringField('Username'  , [validators.Length(min=1, max=150), validators.DataRequired()] , render_kw={"placeholder" : "Username"})
    checkbox = BooleanField('Email/Phone number')
    Switching = EmailField("Email" ,[validators.Email(message="Please enter a correct email") ,validators.DataRequired()] , render_kw={"placeholder" : "Email"})
    Code = StringField("" , [validators.length(min=6 , max=6), validators.DataRequired()] , render_kw={"placeholder" : "Verification code"})
    password = PasswordField("Password" , [validators.length(min=8 , message="Please enter a stronger password") , validators.DataRequired() , validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" , message="Weak Password") ], render_kw={"placeholder": "Password"})
    confirmpassword = PasswordField("Confirm Password", [validators.length(min=8) , validators.EqualTo('password' , message='Password must match') ] , render_kw={"placeholder": "Confirm Password"})
    showpassword = BooleanField("")
    birthdate = DateField("Birthdate" , [validators.DataRequired() , date_validator] , render_kw={"placeholder" : "MM/DD/YYYY"})
    notification = BooleanField("")





class SignUpFormPhone(Form):
    username = StringField('Username'  , [validators.Length(min=1, max=150), validators.DataRequired()] , render_kw={"placeholder" : "Username"})
    checkbox = BooleanField('Email/Phone number' , default=True , render_kw={"checked" : ""})
    Switching = StringField("" ,[validators.Length(min=1, max=8), validators.DataRequired()] , render_kw={"placeholder" : "Phone Number"})
    Code = StringField("" , [validators.length(min=6 , max=6), validators.DataRequired()] , render_kw={"placeholder" : "Verification code"})
    password = PasswordField("Password" , [validators.length(min=8 , message="Please enter a stronger password") , validators.EqualTo('confirmpassword' , message='Password must match') , validators.DataRequired() ], render_kw={"placeholder": "Password"})
    confirmpassword = PasswordField("Confirm Password", [validators.length(min=8) , validators.DataRequired()] , render_kw={"placeholder": "Confirm Password"})
    showpassword = BooleanField("")
    birthdate = DateField("Birthdate" , [validators.DataRequired()] )
    notification = BooleanField("")


class LoginForm(Form):
    username_or_email = StringField('Username/Email' , [validators.DataRequired()] , render_kw={"placeholder" : "Input"})
    password = PasswordField("Password" , [validators.DataRequired()] , render_kw={"placeholder": "Password"})
    showpassword = BooleanField("")

class UpdateProfile(Form):
    usernamefield = StringField('Username' , [validators.DataRequired()]  )
    birthdatefield = DateField('Birthday', [validators.DataRequired() , date_validator] )
    AboutMefield = TextAreaField('About Me')
    cross = BooleanField("")
    file = FileField("Select Image" , validators=[FileAllowed(['jpg' , 'png' ] , 'Images only!')])




class ChangeEmail(Form):
    Email = EmailField("" , render_kw={"placeholder" : "Email"})
    Code = StringField("" , render_kw={"placeholder" : "6-Digit code"})
    NewEmail = EmailField("" ,[validators.Email(message="Please enter a correct email") ,validators.DataRequired()] , render_kw={"placeholder" : "New Email"})




class AddPhoneNumber(Form):
    Phonenumber = StringField("" , [validators.length(min= 8 , max=8) , validators.DataRequired()] , render_kw={"placeholder" : "Phone Number"})


class ChangePhoneNumber(Form):
     Phonenumber = StringField("" , render_kw={"placeholder" : "Phone Number" , "disabled" : ''})
     NewPhonenumber = StringField("" , [validators.length(min= 8 , max=8) , validators.DataRequired()], render_kw={"placeholder" : "New Phone Number"})


class ChangePassword(Form):
    CurrentPassword = PasswordField("", [validators.length(min=8) , validators.DataRequired()] , render_kw={"placeholder": "Current Password"})
    NewPassword = PasswordField("" , [validators.length(min=8) , validators.DataRequired() , validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$" , message="Weak Password") ] , render_kw={"placeholder" : "New Password"})
    ConfirmNewPassword = PasswordField("" ,[validators.length(min=8) , validators.DataRequired() ,validators.EqualTo('NewPassword' , message='Password must match') ] , render_kw={"placeholder" : "Retype Password"} , )
    showpassword = BooleanField("")



class PaymentMethod(Form):
    Cardtype = SelectField("Card Type", [validators.DataRequired()] , choices={'Visa' , 'MasterCard'})
    Cardnumber = StringField("Card Number" , [validators.DataRequired() , validators.length(min=19 , max=19)] , render_kw={"placeholder" : "Card no"})
    Expirationdate = StringField("Expiration Date" , [validators.DataRequired() , validators.length(min=5 , max=5) , card_expiry] , render_kw={"placeholder": "MM/YY"})
    CCV = PasswordField("CCV" , [validators.DataRequired() , validators.length(min=3 , max=3)] , render_kw={"placeholder" : "CCV"})


class LanguageForm(Form):
    LanguageField = SelectField("Display content in this language" , choices={"English" , "简体中文  (simplified chinese)"})


class ForgetPasswordform(Form):
    Email = EmailField("",[validators.Email(message="Please enter a correct email") ,validators.DataRequired()] , render_kw={"placeholder" : "Email"})


