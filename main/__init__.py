from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
app = Flask(__name__)
app.config['SECRET_KEY']="sadasfw23ekqje2sdadad"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="index"
login_manager.login_message="ابتدا وارد شوید."
login_manager.login_message_category="danger"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='email'
app.config['MAIL_PASSWORD']='password'
mail=Mail(app)
from main import routes