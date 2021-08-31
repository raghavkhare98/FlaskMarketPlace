"""
this file is created and named as such because it will initialise all the variables and packages required to run the website and this will
the first file which will execute
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # we initialised login here because flask  login needs to know which app you want it's functionalities for

app = Flask(__name__) #creatin an instance of the Flask class. This app will work as the central object of everything such as view functions, url etc.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' #this is the location of the database hence URI instead of URL. URI is an identifier of a specific resource
app.config['SECRET_KEY'] = 'b9722e02f979d3f0f602a321'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #this variable is set for login required
login_manager.login_message_category = "info" #this is the category of the flash message
from market import routes