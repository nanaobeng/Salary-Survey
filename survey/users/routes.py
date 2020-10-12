from flask import Flask, render_template, url_for , flash, redirect, request , Blueprint
from survey import db,bcrypt
from survey.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, SectorForm, IndustryForm , ClientForm, JobForm, SurveyForm
from survey.models import User
from flask_login import login_user, current_user, logout_user , login_required
from survey.users.utils import send_reset_email

users = Blueprint('users',__name__)



@users.route("/register",methods=["POST","GET"])
def register():
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Account Created','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',form=form,title="Register")
   


@users.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

  
        
        if user and (bcrypt.check_password_hash(user.password,form.password.data)):
            
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page)  if next_page else redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful',"danger")
    return render_template('login.html',form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))




@users.route("/account")
@login_required
def account():
    return render_template('account.html')


@users.route("/reset_password",methods=['POST','GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset account','info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html',form=form)


@users.route("/reset_password/<token>",methods=['POST','GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated','success')
        return redirect(url_for('users.login'))
    return render_template("reset_token.html",form=form,title="Reset Password")


@users.route("/create_client")
def create_client():
    form = ClientForm()
    return render_template("create_client.html",form=form,title="Create Client")


@users.route("/create_contact")
def create_contact():
    return render_template("contact_person.html")

@users.route("/create_sector")
def create_sector():
    form = SectorForm()
    
    return render_template("create_sector.html",form=form,title="Create Sector")

@users.route("/create_job")
def create_job():
    form = JobForm()
    return render_template("create_job_title.html",form=form,title="Create Job Title")


@users.route("/create_industry")
def create_industry():
    form = IndustryForm()
    return render_template("create_industry.html",form=form,title="Create Industry")

@users.route("/create_admin")
def create_admin():
    return render_template("register_admin.html")


@users.route("/create_comparator")
def create_comparator():
    return render_template("register_comparator.html")



@users.route("/survey")
def survey():
    form = SurveyForm()
    return render_template("survey_form.html",form=form,title="Survey")


@users.route("/create_questions")
def questions():
    form = SurveyForm()
    return render_template("create_questions.html",title="Set Questions")





