from flask import Flask, render_template, url_for , flash, redirect, request , Blueprint
from survey import db,bcrypt
from survey.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, SectorForm, IndustryForm , ClientForm, JobForm, SurveyForm,AreaForm
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
    if current_user.is_authenticated and current_user.role == 'admin':
        
        return redirect(url_for('users.admin_home'))
    if current_user.is_authenticated and current_user.role != 'admin':
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
    return redirect(url_for('main.landing'))




@users.route("/account")
@login_required
def account():
    test = current_user.role
    return render_template('account.html',test=test)


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

@users.route("/area_of_operation")
def create_area():
    form = AreaForm()
    return render_template("operation_area.html",form=form,title="Create Area of Operation")


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


@users.route("/survey_actions")
@login_required
def survey_home():
    return render_template("survey_dash.html")


@users.route("/create_survey")
def create_survey():
    return render_template("create_survey.html")

@users.route("/add_comparator")

def add_comparators():
    return render_template("add_comparator.html")


@users.route("/add_benchmark_jobs")

def add_benchmark_job():
    return render_template("create_benchmark_jobs.html")

@users.route("/survey_history")

def survey_history():
    return render_template("survey_history.html")


@users.route("/benchmark_jobs")

def benchmark_jobs():
    return render_template("benchmark_jobs.html")


@users.route("/comparators")
def comparators():
    return render_template("comparators.html")

# this route will have to be modified
@users.route("/survey/view_survey")
def view_survey():
    return render_template("view_survey.html")

@users.route("/my_reports")
def my_reports():
    return render_template("my_reports.html")

@users.route("/my_surveys")
def my_surveys():
    return render_template("my_surveys.html")

@users.route("/my_surveys/view_survey/quantitative")
def quantitative_overview():
    return render_template("quantitative_survey_overview.html")

@users.route("/my_surveys/view_survey/qualitative")
def qualitative_overview():
    return render_template("qualitative_survey_overview.html")

@users.route("/administration")
def admin_home():
    return render_template("admin_home.html")

@users.route("/administration/surveys")
def admin_surveys():
    return render_template("admin_surveys.html")

@users.route("/administration/clients")
def admin_clients():
    return render_template("admin_clients.html")

@users.route("/administration/service_requests")
def admin_service_requests():
    return render_template("admin_service_requests.html")


@users.route("/administration/reports")
def admin_reports():
    return render_template("admin_reports.html")

@users.route("/administration/configuration")
def admin_configuration():
    return render_template("admin_configuration.html")


@users.route("/survey/quantitative")
def quantitative_survey():
    form = SurveyForm()
    return render_template("quantitative_survey.html",form=form)






