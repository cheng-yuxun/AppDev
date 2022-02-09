from flask import Flask
from flask_mail import Mail
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'appdevprojectsss@gmail.com'
app.config['MAIL_PASSWORD'] = 'Urmumlol6969@'
mail = Mail()
mail.init_app(app)
Upload_Folder = 'static/media/profilepic/'
app.config['Upload_FOLDER'] = Upload_Folder

from services.common_ep import endpoint as EP_Common
from services.auth_ep import endpoint as EP_Auth
from services.usereward_ep import endpoint as EP_Rewards
from services.admin.frontpage_ep import endpoint as EP_Admin_FrontPage
from services.admin.events_ep import endpoint as EP_Admin_Events
from services.admin.users_ep import endpoint as EP_Admin_Users
from services.admin.products_ep import endpoint as EP_Admin_Products
from services.admin.rewards_ep import endpoint as EP_Admin_Rewards
app.register_blueprint(EP_Common, url_prefix="/")
app.register_blueprint(EP_Auth, url_prefix="/")
app.register_blueprint(EP_Rewards, url_prefix='/')
app.register_blueprint(EP_Admin_FrontPage, url_prefix="/admin")
app.register_blueprint(EP_Admin_Events, url_prefix="/admin")
app.register_blueprint(EP_Admin_Users, url_prefix="/admin")
app.register_blueprint(EP_Admin_Products, url_prefix="/admin")
app.register_blueprint(EP_Admin_Rewards, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)

