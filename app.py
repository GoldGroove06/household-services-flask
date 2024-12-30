from flask import Flask, render_template, redirect, url_for 
from routes.customer_route import customer_route
from routes.prof_route import prof_route
from routes.admin_route import admin_route
from routes.auth_route import auth_route
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from model import *



load_dotenv()


app = Flask("__name__")
app.app_context().push()


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = os.getenv('SESSION_ID')
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def homepage():
    return render_template('home_page.html')

auth_route(app)
prof_route(app)
customer_route(app)
admin_route(app)


if __name__ == "__main__" :
    db.create_all()
   
    app.debug=True
    app.run()