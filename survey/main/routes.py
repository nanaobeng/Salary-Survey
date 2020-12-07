from flask import render_template,request,Blueprint, redirect, url_for
from flask_login import login_user, current_user, logout_user , login_required
from survey.models import User


main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('users.admin_home'))
    
    return render_template('index.html')
 






@main.route("/")
def landing():
    if current_user.is_authenticated and current_user.role == 'admin':
        
        return redirect(url_for('users.admin_home'))
    if current_user.is_authenticated and current_user.role != 'admin':
        return redirect(url_for('main.index'))

    return render_template("new_landing.html")



@main.route("/contact")
def contact():
    
    return render_template("contact.html")


@main.route("/terms")
def terms():
    
    return render_template("terms.html")


@main.route("/privacy")
def privacy():
    
    return render_template("privacy.html")




