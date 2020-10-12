from flask import render_template,request,Blueprint
from flask_login import login_user, current_user, logout_user , login_required
from survey.models import User


main = Blueprint('main', __name__)
@main.route("/")
@main.route("/home")
@login_required
def index():
    return render_template("index.html")

