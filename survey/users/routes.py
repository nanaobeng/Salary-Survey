from flask import Flask, render_template, url_for , flash, redirect, request , Blueprint, jsonify, json
from survey import db,bcrypt
from survey.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, SectorForm, IndustryForm , ClientForm, JobForm, SurveyForm, AreaForm,QualForm,IndividualRequestForm,CorporateRequestForm,ContactForm
from survey.models import *
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
    return render_template('new_login.html',form=form)


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
    return render_template("new_create_client.html",form=form,title="Create Client")


@users.route("/create_contact")
def create_contact():
    return render_template("contact_person.html")

@users.route("/create_sector",methods=["POST","GET"])
def create_sector():
    form = SectorForm()
    sectors = Sector.query.all()
    if form.validate_on_submit():
       new_sector = Sector(sector=form.name.data)
       db.session.add(new_sector)
       db.session.commit()
       flash('Sector Created','success')
       return redirect(url_for('users.create_sector'))
    return render_template("create_sector.html",form=form,title="Create Sector", Sectors=sectors)


@app.route("/sector/<int:sector_id>/delete", methods=['POST'])
@login_required
def delete_sector(sector_id):
    sector = Sector.query.get_or_404(sector_id)
    db.session.delete(sector)
    db.session.commit()
    flash('Sector Deleted', 'success')
    return redirect(url_for('users.create_sector'))


@users.route("/sector/view", methods = ['POST','GET'])
@login_required
def view_sector():
    sector_id = request.form['id']
    sector = Sector.query.get(sector_id)

    data = []
    data.append({'id':sector.id, 'sector':sector.sector})
    return jsonify(data)
    return redirect(url_for('users.create_sector'))


@users.route("/sector/update/<int:sector_id>", methods = ['POST','GET'])
@login_required
def update_sector(sector_id):
    sector = Sector.query.get_or_404(sector_id)
    form = SectorForm()
    if form.validate_on_submit():
        sector.sector = form.name.data
        db.session.commit()
        flash('Sector Updated', 'success')
    return redirect(url_for('users.create_sector'))
    


@users.route("/create_job")
def create_job():
    form = JobForm()
    return render_template("create_job_title.html",form=form,title="Create Job Title")

@users.route("/area_of_operation", methods=['POST', 'GET'])
def create_area():
    form = AreaForm()
    Areas = Area.query.all()
    
    if form.validate_on_submit():
        area = Area(area = form.name.data, industry_id = form.industry.data)
        
        db.session.add(area)
        db.session.commit()
        flash('Area of Operation Created','success')
        return redirect(url_for('users.create_area'))
    return render_template("operation_area.html",form=form,title="Create Area of Operation", Areas = Areas)


@users.route("/area/<int:area_id>/delete", methods=['POST'])
@login_required
def delete_area(area_id):
    area = Area.query.get_or_404(area_id)
    db.session.delete(area)
    db.session.commit()
    flash('Area of Operation Deleted', 'success')
    return redirect(url_for('users.create_area'))


@users.route("/industry/filter", methods = ['POST','GET'])
@login_required
def filter_industry():
    sector_id = request.form['id']
    industries = Industry.query.filter_by(sector_id = sector_id)
    data = []
    for industry in industries:
        data.append({'id':industry.id, 'industry':industry.industry})
    return jsonify(data)



@users.route("/area/view", methods = ['POST','GET'])
@login_required
def view_area():
    area_id = request.form['id']
    area = Area.query.get(area_id)
    data = []
    data.append({'id':area.id, 'area':area.area, 'industry':area.industry.id, 'sector':area.industry.business_sector.id})
    return jsonify(data)



@users.route("/area/update/<int:area_id>", methods = ['POST','GET'])
@login_required
def update_area(area_id):
    area = Area.query.get_or_404(area_id)
    form = AreaForm()
    if form.validate_on_submit():
        area.area = form.name.data
        area.industry_id = form.industry.data
        db.session.commit()
        flash('Area Updated', 'success')
    return redirect(url_for('users.create_area'))




@users.route("/create_industry", methods=['POST', 'GET'])
def create_industry():
    Industries = Industry.query.all()
    form = IndustryForm()
    if form.validate_on_submit():
        industry = Industry(industry = form.name.data, sector_id = form.sector.data.id)
        
        db.session.add(industry)
        db.session.commit()
        flash('Industry Created','success')
        return redirect(url_for('users.create_industry'))
    return render_template("create_industry.html",form=form,title="Create Industry", Industries = Industries)


@users.route("/industry/<int:industry_id>/delete", methods=['POST'])
@login_required
def delete_industry(industry_id):
    industry = Industry.query.get_or_404(industry_id)
    db.session.delete(industry)
    db.session.commit()
    flash('Industry Deleted', 'success')
    return redirect(url_for('users.create_industry'))


@users.route("/industry/view", methods = ['POST','GET'])
@login_required
def view_industry():
    industry_id = request.form['id']
    industry = Industry.query.get(industry_id)

    data = []
    data.append({'id':industry.id, 'industry':industry.industry, 'sector':industry.sector_id})
    return jsonify(data)
    return redirect(url_for('users.create_industry'))


@users.route("/industry/update/<int:industry_id>", methods = ['POST','GET'])
@login_required
def update_industry(industry_id):
    industry = Industry.query.get_or_404(industry_id)
    form = IndustryForm()
    if form.validate_on_submit():
        industry.industry = form.name.data
        industry.sector_id = form.sector.data.id
        db.session.commit()
        flash('Industry Updated', 'success')
    return redirect(url_for('users.create_industry'))



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

    return render_template("create_questions.html",title="Set Questions")


@users.route("/survey_actions")
@login_required
def survey_home():
    return render_template("survey_dash.html")


@users.route("/create_survey")
def create_survey():
    form = SurveyForm()
    if form.validate_on_submit():
        sur = Survey(name="test2",start_date=datetime(2012, 3, 3, 10, 10, 10),end_date=datetime(2012, 3, 3, 10, 10, 10),status="active",client_id=1)
        db.session.add(sur)
        db.session.commit()
        flash('Account Created','success')
        return redirect(url_for('users.login'))
    return render_template("new_create_survey.html",form=form)

@users.route("/edit_survey")
def edit_survey():
    return render_template("admin_edit_survey.html")

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
    return render_template("new_client_reports.html")

@users.route("/my_benchmark_jobs")
def my_benchmark_jobs():
    
    form = SurveyForm()
    return render_template("new_view_client_benchmark.html",form=form)



@users.route("/my_benchmark_jobs/options")
def my_benchmark_options():

    return render_template("new_client_benchmark_options.html")

@users.route("/my_benchmark_jobs/new")
def my_benchmark_jobs_create():
    form = SurveyForm()
    return render_template("new_client_create_benchmark.html",form=form)

@users.route("/my_surveys")
def my_surveys():
    return render_template("quantitative_survey_overview.html")

@users.route("/my_surveys/view_survey/quantitative")
def quantitative_overview():
    return render_template("quantitative_survey_overview.html")

@users.route("/my_surveys/view_survey/qualitative")
def qualitative_overview():
    return render_template("qualitative_survey_overview.html")

@users.route("/administration")
def admin_home():
    return render_template("new_admin_dashboard.html")

@users.route("/administration/surveys")
def admin_surveys():
    return render_template("new_view_survey.html")

@users.route("/administration/benchmark-jobs")
def admin_benchmarl():
    return render_template("admin_benchmark.html")

@users.route("/administration/clients")
def admin_clients():
    return render_template("new_view_client.html")

@users.route("/administration/service_requests")
def admin_service_requests():
    return render_template("new_requests.html")


@users.route("/administration/reports")
def admin_reports():
    return render_template("new_admin_reports.html")

@users.route("/administration/client_hub")
def client_hub():
    return render_template("client_hub.html")

@users.route("/administration/configuration")
def admin_configuration():
    return render_template("admin_configuration.html")

@users.route("/administration/config/users")
def admin_users():
    rows_per_page = 5
    search = request.args.get('search', 1, type=str)
    page = request.args.get('page', 1, type=int)
    if search !='':
        
        Users = User.query.paginate(page=page, per_page=rows_per_page)
        # Users = User.query.filter(User.email.like(('%'+search+'%'))).paginate(page=page, per_page=rows_per_page)
    else:
        Users = User.query.paginate(page=page, per_page=rows_per_page)
    
    return render_template("admin_users.html", Users=Users)

@users.route("/administration/config/benchmark_jobs")
def admin_benchmark_jobs():
    return render_template("admin_benchmark_jobs.html")

@users.route("/administration/config/create_benchmark_job")
def create_benchmark_job():
    return render_template("create_benchmark_job.html")

@users.route("/survey/quantitative")
def quantitative_survey():
    form = SurveyForm()
    return render_template("quantitative_survey.html",form=form)






@users.route("/user/profile")
def update_profile():
    
    return render_template("update_profile.html")


@users.route("/administration/corporate-request-review")
def review_corporate():
    
    return render_template("new_service_requests_view.html")




@users.route("/administration/individual-request-review")
def review_individual():
    
    
    return render_template("new_service_individual_requests_view.html")

@users.route("/user/update-client")
def update_client():
    
    
    return render_template("update_client.html")


@users.route("/user/client-benchmark")
def client_benchmark():
    
    form = SurveyForm()
    return render_template("client_create_benchmark_job.html", form=form)


@users.route("/user/view-benchmark")
def client_view_benchmark():
    
    form = SurveyForm()
    return render_template("new_view_benchmark.html", form=form)


@users.route("/administration/review_benchmark")
def review_benchmark():
    

    return render_template("review_benchmark.html")

@users.route("/administration/view_client")
def view_client():
    

    return render_template("new_view_client_info.html")

@users.route("/administration/edit_client")
def edit_client():
    

    return render_template("new_edit_client.html")

@users.route("/my_benchmark_jobs/edit")
def edit_benchmark():
    
    form = SurveyForm()
    return render_template("new_edit_client_benchmark_jobs.html",form=form)



