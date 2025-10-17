from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba2e18ce248bab7ce9425333f0420b57a5f07dfef342e1876d3013a524acf416f813af3071a65e3860475fe8e81c3a42c3c8fa65051de39aa2037fa695b305a7bc7044a415eb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:Felipe1323@localhost:5432/mi_basededatos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#login_manager = LoginManager(app)
#login_manager.login_view = 'login'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
