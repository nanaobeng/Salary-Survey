from flask import Flask, render_template, url_for , flash, redirect, request , Blueprint, jsonify, json, session
from survey import db , bcrypt
from survey.users.forms import RegistrationForm, LoginForm, RequestResetForm, RequestSearchForm, ResetPasswordForm, SectorForm, IndustryForm , MessageComment, ClientForm, JobForm, SurveyForm, AreaForm,QualForm,IndividualRequestForm,CorporateRequestForm,ContactForm,ServiceRequestForm
from survey.models import *
from flask_login import login_user, current_user, logout_user , login_required
from survey.users.utils import send_reset_email
from datetime import datetime
from sqlalchemy import or_, desc

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


@users.route("/create_client",methods=['POST','GET'])
def create_client():
    usn = current_user
    form = ClientForm()
    
    if form.validate_on_submit():
        post = Postal_address(street_line1=form.mailing_building.data,street_line2=form.mailing_street.data,city=form.mailing_city.data,country=form.mailing_country.data,region=form.mailing_country.data)
        street = Street_address(street_line1=form.street_building.data,street_line2=form.street_street.data,city=form.street_city.data,country=form.street_country.data,region=form.street_country.data)
        chair = Board_chairman(first_name=form.chairman_firstname.data,last_name=form.chairman_lastname.data,other_names=form.chairman_other_names.data,email=form.chairman_email.data,mobile_number=form.chairman_phone.data,nationality=form.chairman_nationality.data)
        ceo = Ceo(first_name=form.ceo_firstname.data,last_name=form.ceo_lastname.data,other_names=form.ceo_other_names.data,email=form.ceo_email.data,mobile_number=form.ceo_phone.data,nationality=form.ceo_nationality.data)
        key = Key_management(first_name=form.key_firstname.data,last_name=form.key_lastname.data,other_names=form.key_other_names.data,email=form.key_email.data,mobile_number=form.key_phone.data,nationality=form.key_nationality.data)
        cur_aud = Current_auditor(name=form.current_auditor_name.data,address=form.current_auditor_address.data,city=form.current_auditor_city.data,country=form.current_auditor_country.data)
        prev_aud = Previous_auditor(name=form.previous_auditor_name.data,address=form.previous_auditor_address.data,city=form.previous_auditor_city.data,country=form.previous_auditor_country.data)
        con = Contact_person(first_name=form.contact_firstname.data,last_name=form.contact_lastname.data,other_names=form.contact_middlename.data,email=form.c_email.data,mobile_number=form.c_phone.data,nationality=form.contact_nationality.data,date_of_birth=form.contact_dob.data,job=form.job.data)
        sec = Company_secretary(name=form.company_secretary_name.data,address=form.company_secretary_address.data,city=form.company_secretary_city.data,country=form.company_secretary_country.data)
        client = Client(
        company_history = form.company_history.data,
        company_name = form.name.data,
        user = usn,
        sector = form.sector.data,
        industry = form.industry.data,
        area = form.area.data,
        financial_year_end = form.financial_year_end.data,
        company_type = form.company_type.data,
        postal_address = post,
        street_address = street,
        reg_number = form.registration.data,
        vat_number = form.vat.data,
        tel = form.telephone.data,
        fax = form.fax.data,
        company_email = form.email.data,
        website = form.website.data,
        date_inc = form.date_of_incorporation.data,
        country_inc = form.country_of_incorporation.data,
        board_chairman = chair,
        ceo = ceo,
        key_management = key,
        previous_auditor=prev_aud,
        current_auditor=cur_aud,
        company_secretary= sec,
        contact_person = con)
        db.session.add(post)
        db.session.add(street)
        db.session.add(chair)
        db.session.add(ceo)
        db.session.add(key)
        db.session.add(cur_aud)
        db.session.add(prev_aud)
        db.session.add(con)
        db.session.add(sec)
        db.session.add(client)
        db.session.commit()

        flash('Client has successfully been created','success')
        return redirect(url_for('users.create_client'))
    return render_template("new_create_client.html",form=form,title="Create Client")


@users.route("/create_contact")
def create_contact():
    return render_template("contact_person.html")

# load messages from 'Contact' in database
@users.route("/messages")
def messages():
    form = MessageComment()
    messages = Contact.query.filter_by(status="Open").order_by(desc(Contact.timestamp)).all()
    # messages = Contact.query.all()
    return render_template("messages.html", messages=messages, form=form)

# view message modal
@users.route('/view_message', methods=['POST','GET'])
def viewMessage():
    id = request.form['id']

    messages = Contact.query.filter_by(id=id)
    comments = Comment.query.filter_by(contact_id=id)
    comment_array = []
    temp = []
    for message in messages:
        temp.append({'id': message.id, 'title':message.title ,'firstname' :message.firstname,
        'lastname':message.lastname,'email':message.email,'job_title':message.job_title,
        'company_name':message.company_name,'phone':message.phone,'address_1':message.address_1,
        'address_2':message.address_2,'city':message.city,'country':message.country,
        'status':message.status,'timestamp':message.timestamp})
    
    for comment in comments:
        comment_array.append(comment.comment)

    temp.append({'comments': comment_array})

    return jsonify(temp)

# 
@users.route('/messages/update/<int:messageId>', methods=['POST'])
def updateMessage(messageId):
    message = Contact.query.get_or_404(messageId)
    form = MessageComment()
    if form.validate_on_submit:
        comment = Comment(comment=form.comment.data, contact_id=messageId)
        status = str(form.status.data)
        if (status == "True"):
            new_status = "Closed"
        elif (status == "False"):
            new_status = "Open" 
        message.status = new_status
        db.session.add(comment)
        db.session.commit()
        flash("Message Updated", "success")
        return redirect(url_for('users.messages'))


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
    query = Main_benchmark_job.query.all()
    base = Base_salary.query.all()
    
    return render_template("new_view_client_benchmark.html",query=query,base=base)



@users.route("/my_benchmark_jobs/options")
def my_benchmark_options():
    usn = current_user
    job = Main_benchmark_job.query.filter_by(user_account=usn).all()

    return render_template("new_client_benchmark_options.html",job=job)

@users.route("/my_benchmark_jobs/new",methods=['POST','GET'])
def my_benchmark_jobs_create():
    form = SurveyForm()
    user = current_user
    if form.validate_on_submit():
        b_job = Main_benchmark_job(job_title=form.job_title.data,grade=form.grade.data,main_department=form.department.data,reporting_relationship=form.reporting_relationship.data,job_description=form.job_desc.data,duties_and_responsibility=form.key_duties.data,financial_responsibilities=form.fin_res.data,technical_qualification=form.tech_qual.data,minimum_years_of_experience=form.exp_years.data,user_account=user)
        base = Base_salary(monthly_base_salary=form.base_salary.data,main_benchmark_base=b_job)
        inc  = Incentive(company_performance=form.company_bonus_performance.data,individual_performance=form.individual_bonus_performance.data,annual_incentive=form.annual_bonus.data,incentive=form.incentive_bonus.data,other_cash=form.other_bonus.data,main_benchmark_incentive=b_job)
        benefits = Benefit(staff_bus=form.staff_bus.data,company_car=form.company_car.data,personal_travel=form.personal_travel.data,petrol=form.petrol.data,vehicle_maintenance=form.vehicle.data,driver=form.driver.data,health_insurance=form.health_insurance.data,medical_assistance=form.medical_assistance.data,funeral_assistance=form.funeral_assistance.data,life_insurance=form.life_insurance.data,group_accident=form.group_accident.data,club_membership=form.club_membership.data,school_fees=form.school_fees.data,vacation=form.vacation.data,housing=form.housing.data,telephone=form.telephone.data,security=form.security.data,other_benefits=form.other_benefits.data,main_benchmark_benefit=b_job)
        allowance = Allowance(vehicle_maintenance=form.vehicle_maintenance.data,vehicle=form.allowance_vehicle.data,transport=form.transport.data,fuel=form.fuel.data,car=form.car.data,driver=form.allowance_driver.data,domestic_safety=form.domestic.data,housing=form.allowance_housing.data,utilities=form.utilities.data,meal=form.meal.data,telephone=form.allowance_telephone.data,entertainment=form.entertainment.data,education_support=form.education.data,vacation=form.vacation_allowance.data,uniform=form.uniform.data,mobile_money=form.mobile_money.data,miscellaenous=form.misc.data,main_benchmark_allowance=b_job)
        db.session.add(b_job)
        db.session.add(base)
        db.session.add(inc)
        db.session.add(benefits)
        db.session.add(allowance)
        db.session.commit()
        flash('Job Position Created','success')
        return redirect(url_for('users.my_benchmark_jobs_create')) 
    return render_template("new_client_create_benchmark.html",form=form)

@users.route("/my_surveys")
def my_surveys():
    usn = current_user.id
    query = []
    surveys = Benchmark_job.query.all()
    for survey in surveys:
        if survey.benchmark.user.id == usn:
            query.append(survey)

    return render_template("quantitative_survey_overview.html",usn=usn,query=query)
    return render_template("quantitative_survey_overview.html")

@users.route("/my_surveys/view_survey/quantitative")
def quantitative_overview():
    
    return render_template("quantitative_survey_overview.html")

@users.route("/my_surveys/view_survey/qualitative")
def qualitative_overview():
    cli = Client.query.all()
    usn = current_user.id
    qual = Qualitative_survey.query.all()
    for i in qual:
        if i.client_qual.user.id == current_user.id:
            qual = i
    for i in cli:
        if i.user.id == current_user.id:
            cli = i
    return render_template("qualitative_survey_overview.html",cli=cli,qual=qual,usn=usn)

@users.route("/administration")
def admin_home():
    return render_template("new_admin_dashboard.html")

@users.route("/administration/surveys")
def admin_surveys():
    return render_template("new_view_survey.html")

@users.route("/administration/benchmark-jobs")
def admin_benchmarl():
    return render_template("admin_benchmark.html")

@users.route("/administration/clients",methods=['POST','GET'])
def admin_clients():
    query = Client.query.all()
    
    if request.method == 'POST':
        client = Client.query.get_or_404(request.form['client_id'])
        client.status = request.form['c_status']
        try:
            db.session.commit()
            flash('Client Updated','success')
            return redirect(url_for('users.admin_clients'))
        except:
            flash('There was an issue updating the client','danger')
            return redirect(url_for('users.admin_clients'))
    else:
        return render_template("new_view_client.html",query=query)


@users.route("/administration/reports")
def admin_reports():
    return render_template("new_admin_reports.html")


@users.route("/administration/client_hub")
def client_hub():
    
    return render_template("client_hub.html")
    
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


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

@users.route("/survey/quantitative/<int:id>",methods=['POST','GET'])
def quantitative_survey(id):
    job = Benchmark_job.query.get_or_404(id)
    form = SurveyForm()
    if form.validate_on_submit():
        

        job.comp_benchmark_base.monthly_base_salary=form.base_salary.data
      
        job.comp_benchmark_incentive.company_performance=form.company_bonus_performance.data
        job.comp_benchmark_incentive.individual_performance=form.individual_bonus_performance.data
        job.comp_benchmark_incentive.annual_incentive=form.annual_bonus.data
        job.comp_benchmark_incentive.incentive=form.incentive_bonus.data
        job.comp_benchmark_incentive.other_cash=form.other_bonus.data
    

        job.comp_benchmark_benefit.staff_bus=form.staff_bus.data
        job.comp_benchmark_benefit.company_car=form.company_car.data
        job.comp_benchmark_benefit.personal_travel=form.personal_travel.data
        job.comp_benchmark_benefit.petrol=form.petrol.data
        job.comp_benchmark_benefit.vehicle_maintenance=form.vehicle.data
        job.comp_benchmark_benefit.driver=form.driver.data
        job.comp_benchmark_benefit.health_insurance=form.health_insurance.data
        job.comp_benchmark_benefit.medical_assistance=form.medical_assistance.data
        job.comp_benchmark_benefit.funeral_assistance=form.funeral_assistance.data
        job.comp_benchmark_benefit.life_insurance=form.life_insurance.data
        job.comp_benchmark_benefit.group_accident=form.group_accident.data
        job.comp_benchmark_benefit.club_membership=form.club_membership.data
        job.comp_benchmark_benefit.school_fees=form.school_fees.data
        job.comp_benchmark_benefit.vacation=form.vacation.data
        job.comp_benchmark_benefit.housing=form.housing.data
        job.comp_benchmark_benefit.telephone=form.telephone.data
        job.comp_benchmark_benefit.security=form.security.data
        job.comp_benchmark_benefit.other_benefits=form.other_benefits.data

        job.comp_benchmark_allowance.vehicle_maintenance=form.vehicle_maintenance.data
        job.comp_benchmark_allowance.vehicle=form.allowance_vehicle.data
        job.comp_benchmark_allowance.transport=form.transport.data
        job.comp_benchmark_allowance.fuel=form.fuel.data
        job.comp_benchmark_allowance.car=form.car.data
        job.comp_benchmark_allowance.driver=form.allowance_driver.data
        job.comp_benchmark_allowance.domestic_safety=form.domestic.data
        job.comp_benchmark_allowance.housing=form.allowance_housing.data
        job.comp_benchmark_allowance.utilities=form.utilities.data
        job.comp_benchmark_allowance.meal=form.meal.data
        job.comp_benchmark_allowance.telephone=form.allowance_telephone.data
        job.comp_benchmark_allowance.entertainment=form.entertainment.data
        job.comp_benchmark_allowance.education_support=form.education.data
        job.comp_benchmark_allowance.vacation=form.vacation_allowance.data
        job.comp_benchmark_allowance.uniform=form.uniform.data
        job.comp_benchmark_allowance.mobile_money=form.mobile_money.data
        job.comp_benchmark_allowance.miscellaenous=form.misc.data
        job.status = "Completed"
        try:
            db.session.commit()
            flash('Survey Completed','success')
            return redirect(url_for('users.my_surveys'))
        except:
            flash('There was an issue completing the survey','danger')
            return redirect(url_for('users.my_surveys'))
        
    return render_template("quantitative_survey.html",form=form, job=job)

@users.route("/survey/quantitative/view/<int:id>",methods=['POST','GET'])
def quantitative_survey_view(id):
    job = Benchmark_job.query.get_or_404(id)
    form = SurveyForm()
    return render_template("view_quant.html",form=form, job=job)

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


@users.route("/user/view-benchmark/<int:id>")
def client_view_benchmark(id):
    job = Main_benchmark_job.query.get_or_404(id)
    base = Base_salary.query.filter_by(id=id).first()
    incentive = Incentive.query.filter_by(id=id).first()
    allowance = Allowance.query.filter_by(id=id).first()
    benefit = Benefit.query.filter_by(id=id).first()
    
    form = SurveyForm()
    return render_template("new_view_benchmark.html", job=job,form=form,base=base,benefit=benefit,allowance=allowance,incentive=incentive)


@users.route("/administration/review_benchmark")
def review_benchmark():
    

    return render_template("review_benchmark.html")

@users.route("/administration/view_client/<int:id>")
def view_client(id):
    client = Client.query.get_or_404(id)
    

    return render_template("new_view_client_info.html",client=client)

@users.route("/administration/edit_client/<int:id>",methods=['POST','GET'])
def edit_client(id):
    sector = Sector.query.all()
    industry = Industry.query.all()
    area = Area.query.all()

    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.company_name = request.form['company_name']
        client.sector_id = request.form['sector']
        client.industry_id = request.form['industry']
        client.area_id = request.form['area']
        client.financial_year_end = request.form['financial_year_end']
        client.vat_number = request.form['vat']
        client.company_type = request.form['company_type']
        client.tel = request.form['tel']
        client.fax = request.form['fax']
        client.company_email = request.form['email']
        client.website = request.form['website']
        client.date_inc = datetime.strptime(request.form['date_inc'], '%Y-%m-%d')
        client.country_inc = request.form['country_inc']
        client.board_chairman.first_name = request.form['chairman_firstname']
        client.board_chairman.last_name = request.form['chairman_lastname']
        client.board_chairman.other_names = request.form['chairman_other_names']
        client.board_chairman.email = request.form['chairman_email']
        client.board_chairman.nationality = request.form['chairman_nationality']
        client.board_chairman.mobile_number = request.form['chairman_phone']
        client.ceo.first_name = request.form['ceo_firstname']
        client.ceo.last_name = request.form['ceo_lastname']
        client.ceo.other_names = request.form['ceo_other_names']
        client.ceo.email = request.form['ceo_email']
        client.ceo.nationality = request.form['ceo_nationality']
        client.ceo.mobile_number = request.form['ceo_phone']
        client.key_management.first_name = request.form['key_firstname']
        client.key_management.last_name = request.form['key_lastname']
        client.key_management.other_names = request.form['key_other_names']
        client.key_management.email = request.form['key_email']
        client.key_management.nationality = request.form['key_nationality']
        client.key_management.mobile_number = request.form['key_phone']
        client.previous_auditor.name = request.form['previous_auditor_name']
        client.previous_auditor.address = request.form['previous_auditor_address']
        client.previous_auditor.city = request.form['previous_auditor_city']
        client.previous_auditor.country = request.form['previous_auditor_country']
        client.current_auditor.name = request.form['current_auditor_name']
        client.current_auditor.address = request.form['current_auditor_address']
        client.current_auditor.city = request.form['current_auditor_city']
        client.current_auditor.country = request.form['current_auditor_country']
        client.company_secretary.name = request.form['company_secretary_name']
        client.company_secretary.address = request.form['company_secretary_address']
        client.company_secretary.city = request.form['company_secretary_city']
        client.company_secretary.country = request.form['company_secretary_country']
        client.postal_address.street_line1 = request.form['mailing_building']
        client.postal_address.street_line2 = request.form['mailing_street']
        client.postal_address.city = request.form['mailing_city']
        client.postal_address.region = request.form['mailing_region']
        client.postal_address.country = request.form['mailing_country']
        client.street_address.street_line1 = request.form['street_building']
        client.street_address.street_line2 = request.form['street_street']
        client.street_address.city= request.form['street_city']
        client.street_address.region = request.form['street_region']
        client.street_address.country = request.form['street_country']
        client.reg_number = request.form['reg_number']
        client.tax_id = request.form['tax_id']
        
        client.contact_person.first_name = request.form['contact_firstname']
        client.contact_person.lastname = request.form['contact_lastname']
        client.contact_person.other_names = request.form['contact_other_names']
        client.contact_person.email = request.form['contact_email']
        client.contact_person.nationality = request.form['contact_nationality']
        client.contact_person.mobile_number = request.form['contact_phone']
        client.contact_person.job = request.form['contact_job']
        client.contact_person.date_of_birth = datetime.strptime(request.form['contact_dob'], '%Y-%m-%d')
        try:
            db.session.commit()
            flash('Client Updated','success')
            return redirect(url_for('users.admin_clients'))
        except:
            flash('There was an issue updating the client','danger')
            return redirect(url_for('users.admin_clients'))
    else:

        return render_template("new_edit_client.html",client=client,sector=sector,industry=industry,area=area)

@users.route("/my_benchmark_jobs/edit/<int:id>",methods=['POST','GET'])
def edit_benchmark(id):
    dept = Department.query.all()
    job = Main_benchmark_job.query.get_or_404(id)
    base = Base_salary.query.filter_by(id=id).first()
    incentive = Incentive.query.filter_by(id=id).first()
    allowance = Allowance.query.filter_by(id=id).first()
    benefit = Benefit.query.filter_by(id=id).first()
    
    form = SurveyForm()
    if request.method == 'POST':
        job.job_title = request.form['job_title']
        job.department_id = request.form['department']
        job.grade = request.form['grade']
        job.job_description = request.form['job_description']
        job.reporting_relationship = request.form['reporting_relationship']
        job.duties_and_responsibility = request.form['key_duties']
        job.financial_responsibilities = request.form['financial_responsibilities']
        job.technical_qualification = request.form['tech_qual']
        job.minimum_years_of_experience = request.form['exp_years']


        base.monthly_base_salary= request.form['base_salary']

        incentive.company_performance = request.form['cmp_bonus']
        incentive.individual_performance = request.form['indv_bonus']
        incentive.annual_incentive = request.form['annual_bonus']
        incentive.incentive = request.form['inv_bonus']
        incentive.other_cash = request.form['other_bonus']


        benefit.staff_bus = request.form['staff_bus']
        benefit.company_car = request.form['cmp_car']
        benefit.personal_travel = request.form['personal_travel']
        benefit.petrol = request.form['petrol']
        benefit.vehicle_maintenance = request.form['vehicle']
        benefit.driver = request.form['driver']
        benefit.health_insurance= request.form['htl_ins']
        benefit.medical_assistance = request.form['medi_assis']
        benefit.funeral_assistance = request.form['funeral_assistance']
        benefit.life_insurance = request.form['life_insurance']
        benefit.group_accident = request.form['group_accident']
        benefit.club_membership  = request.form['club_membership']
        benefit.school_fees = request.form['school_fees']
        benefit.vacation= request.form['vacation']
        benefit.housing = request.form['housing']
        benefit.telephone = request.form['telephone']
        benefit.security = request.form['security']
        benefit.other_benefits = request.form['other_benefits']


        allowance.vehicle_maintenance = request.form['vehicle_maintenance']
        allowance.vehicle = request.form['allowance_vehicle']
        allowance.transport = request.form['transport']
        allowance.fuel = request.form['fuel']
        allowance.car = request.form['car']
        allowance.driver = request.form['allowance_driver']
        allowance.domestic_safety = request.form['domestic']
        allowance.housing = request.form['allowance_housing']
        allowance.utilities = request.form['utilities']
        allowance.meal = request.form['meal']
        allowance.telephone = request.form['allowance_telephone']
        allowance.entertainment = request.form['entertainment']
        allowance.education_support = request.form['education']
        allowance.vacation = request.form['allowance_vacation']
        allowance.uniform = request.form['uniform']
        allowance.mobile_money = request.form['momo']
        allowance.miscellaenous = request.form['misc']
        try:
            db.session.commit()
            flash('Job Updated','success')
            return redirect(url_for('users.my_benchmark_jobs'))
        except:
            flash('There was an issue updating the job position','danger')
            return redirect(url_for('users.my_benchmark_jobs'))
        
        


    else:
        
        return render_template("new_edit_client_benchmark_jobs.html", job=job,form=form,base=base,benefit=benefit,allowance=allowance,incentive=incentive,dept=dept)



@users.route("/client/benchmark")
def benchmark_home():
    usn = current_user
    job = Main_benchmark_job.query.filter_by(user_account=usn).all()
    return render_template("benchmark_dashboard.html",job=job)




@users.route('/form')
def sdg():
	form = MyForm()
	return render_template('sdg.html', form=form)



@users.route('/i')
def indexx():
 form = MyForm()
 return render_template('sdg.html', form=form)

@users.route('/countries', methods=['POST'])
def countrydic():
    tag = request.form["id"]
    search = "%{}%".format(tag)

    vajx2 = request.form['id']
    posts = Main_benchmark_job.query.filter(Main_benchmark_job.job_title.like(search)).all()
    temp = []
    for post in posts:
        temp.append({'id': post.id, 'job_title':post.job_title ,'main_department' :post.main_department.department})

    return jsonify(temp)

    list_countries = [r.as_dict() for r in posts]
    return 'list_countries'
    res = Main_benchmark_job.query.all()

    return jsonify(list_countries)
 
@users.route('/process', methods=['POST'])
def process():
    country = request.form['country']
    if country:
        return jsonify({'country':country})
    return jsonify({'error': 'missing data..'})



@users.route('/jobs', methods=['POST','GET'])
def jobdic():
    tag = request.form['id']
    search = "%{}%".format(tag)

  
    posts = Main_benchmark_job.query.filter_by(id=tag)
    temp = []
    for post in posts:

        temp.append({'id': post.id, 'job_title':post.job_title ,'main_department' :post.main_department.department, 'job_description' : post.job_description, 'grade':post.grade})

    return jsonify(temp)








@users.route('/compare', methods=['POST'])
def comparedic():
    tag = request.form["id"]
    search = "%{}%".format(tag)

    vajx2 = request.form['id']
    posts = Client.query.filter(Client.company_name.like(search)).all()
    temp = []
    for post in posts:
        temp.append({'id': post.id, 'company_name':post.company_name ,'company_history' :post.company_history,'sector':post.sector.sector,'industry':post.industry.industry})

    return jsonify(temp)


@users.route('/comps', methods=['POST','GET'])
def compdic():
    tag = request.form['id']
    search = "%{}%".format(tag)

  
    posts = Client.query.filter_by(id=tag)
    temp = []
    for post in posts:

        temp.append({'id': post.id, 'company_name':post.company_name ,'company_history' :post.company_history,'sector':post.sector.sector,'industry':post.industry.industry,'area':post.area.area})

    return jsonify(temp)


@users.route('/compss', methods=['POST','GET'])
def compdict():
    tag = request.form['id']
    search = "%{}%".format(tag)

  
    posts = Client.query.filter_by(company_name=tag)
    temp = []
    for post in posts:

        temp.append({'id': post.id, 'company_name':post.company_name ,'company_history' :post.company_history,'sector':post.sector.sector,'industry':post.industry.industry,'area':post.area.area})

    return jsonify(temp)


@users.route('/survey_create', methods=['POST','GET'])
def created_survey_ajax():
    bench = request.form['bench']
    comp = request.form['comp']
    survey = request.form['survey']
    start_date = request.form['start_date']
    client = request.form['client']
    #search = "%{}%".format(tag)

    bench_split = bench.split(',')
    comp_split = comp.split(',')
    posts = Client.query.filter_by(company_name=client).first()
    b_id = "f"

    #client_id = temp[0].id
    sur = Survey(name=survey,status="unprocessed",survey_client=posts)
    db.session.add(sur)
   
    
    
    for i in bench_split:
        b_id = (int(i.replace("b", "")))
        main = Main_benchmark_job.query.filter_by(id=b_id).first()
        base = Base_salary.query.filter_by(id=main.id).first()
        incentive = Incentive.query.filter_by(id=main.id).first()
        allowance = Allowance.query.filter_by(id=main.id).first()
        benefit = Benefit.query.filter_by(id=main.id).first()
        for c in comp_split :
            c_id = (int(c.replace("c", "")))
            cli = Client.query.filter_by(id=c_id).first()
            db.session.add(Survey_comparator(comparator=sur,client=cli,status="unprocessed"))
            db.session.add(Benchmark_job(job_title=main.job_title,department=main.main_department,grade=main.grade,reporting_relationship=main.reporting_relationship,job_description=main.job_description,duties_and_responsibility=main.duties_and_responsibility,financial_responsibilities= main.financial_responsibilities,technical_qualification=main.technical_qualification,minimum_years_of_experience=main.minimum_years_of_experience,benchmark=cli,comp_benchmark=sur,comp_benchmark_allowance=allowance,comp_benchmark_benefit=benefit,comp_benchmark_incentive=incentive,comp_benchmark_base=base))
    
    db.session.commit()
    return jsonify('success')



 

@users.route('/survey_modal', methods=['POST','GET'])
def smodaldict():
    tag = request.form['id']
    search = "%{}%".format(tag)

  
    posts = Survey.query.filter_by(id=tag).all()
    post = posts[0]
    b_marks = Benchmark_job.query.all()
    comps = Survey_comparator.query.all()
    temp_b = []
    temp_c = []
    for b in b_marks:
        if(b.comp_benchmark.id == post.id):
            temp_b.append(b.job_title)
    for c in comps:
        if(c.comparator.id == post.id):
            temp_c.append(c.comparator.survey_client.company_name)

    temp_b = list(dict.fromkeys(temp_b))
    temp_c = list(dict.fromkeys(temp_c))
    temp = []
   

    temp.append({'id': post.id, 'name':post.name ,'client':post.survey_client.company_name,'industry' :post.survey_client.industry.industry,'area':post.survey_client.area.area,'start_date':post.start_date,'benchmarks':temp_b,'comps':temp_c})

    return jsonify(temp)



@users.route('/survey_filters', methods=['POST','GET'])
def survey_filter():
    tag = request.form['stat']
    tag = tag.split(",")



@users.route("/administration/service_requests", methods=["POST","GET"])
def admin_service_requests():
    form = ServiceRequestForm() 
    searchform = RequestSearchForm()
    ind = Individual_request.query.filter_by(status="pending").all()
    corp= Corporate_request.query.filter_by(status="pending").all()
#filter_by(status="pending").
    return render_template("new_requests.html",form=form ,ind=ind, corp=corp, searchform=searchform)

@users.route("/administration/service_requests/search", methods=["POST"])
def search_requests():
    searchform = RequestSearchForm()
    form = ServiceRequestForm()
    status = request.form['selectstatus']
    requesttype = request.form['selecttype']
    if request.method == 'POST':
        if ((requesttype != "all") and (status !="all")):
            ind = Individual_request.query.filter_by(status=status,type_of_request=requesttype).all()
            corp = Corporate_request.query.filter_by(status=status,type_of_request=requesttype).all()
        elif ((requesttype == "all") and (status !="all")):
            ind = Individual_request.query.filter_by(status=status,type_of_request="individual").all()
            corp= Corporate_request.query.filter_by(status=status,type_of_request="corporate").all()
        elif ((requesttype != "all") and (status =="all")):
            ind = Individual_request.query.filter_by(type_of_request=requesttype).all()
            corp = Corporate_request.query.filter_by(type_of_request=requesttype).all()
        else:
            ind = Individual_request.query.all()
            corp= Corporate_request.query.all()
        return render_template("new_requests.html",searchform=searchform,form=form,ind=ind, corp=corp)
    return render_template("new_requests.html",searchform=searchform,form=form,ind=ind, corp=corp)
    
#,(or_(Individual_request.firstname.like(('%' + search + '%')),Individual_request.lastname.like(('%' + search + '%')),Individual_request.status.like(('%' + search + '%'))) )


  

  
    posts =  Survey.query.filter(Survey.status.in_(tag)).all()
   
    temp = []
    for post in posts:

        temp.append({'id': post.id})

    return jsonify(temp)

# @users.route("/administration/service_requests", methods=["POST","GET"])
# def admin_service_requests():
#     form = ServiceRequestForm() 
#     ind = Individual_request.query.all()
#     corp= Corporate_request.query.filter_by(status="pending").all()

#     return render_template("new_requests.html",form=form ,ind=ind, corp=corp )

@users.route('/view_request', methods=['POST','GET'])
def viewRequest():
    id = request.form['id']

    requests = Individual_request.query.filter_by(id=id)
    comments = RequestComment.query.filter_by(contact_id=id)
@users.route('/view_request/<int:id>', methods=['POST','GET'])
def viewIndRequest(id):
       
    request = Individual_request.query.get_or_404(id)
    comments = RequestComment.query.filter_by(service_id=id)
    comment_array = []
    temp = []
  
    temp.append({'id': request.id, 'date_of_request': request.date_of_request, 'type_of_request': request.type_of_request,
    'status': request.status,'firstname' : request.firstname,'lastname': request.lastname,'email': request.email,'dob': request.dob,'phone': request.phone,
    'address': request.address,'city': request.city,'country': request.country,'service': request.service})
    
    for comment in comments:
        comment_array.append(comment.comment)

    temp.append({'comments': comment_array})

    return jsonify(temp)


@users.route('/administration/service_requests/update/<int:requestId>', methods=['POST'])
def updateRequest(requestId):
    request = Individual_request.query.get_or_404(requestId)
    form = ServiceRequestForm()
    if form.validate_on_submit:
        comment = RequestComment(comment=form.comment.data, service_id=requestId)
        request.status = form.newstatus.data
        db.session.add(comment)
        db.session.commit()
        flash("Request Updated", "success")
        return redirect(url_for('users.admin_service_requests'))

@users.route('/view_corprequest/<int:id>', methods=['POST','GET'])
def viewCorpRequest(id):
    
    post = Corporate_request.query.get_or_404(id)
    comments = RequestComment.query.filter_by(service_id=id)
    comment_array = []
    temp = []
  
    temp.append({'id': post.id, 'date_of_request':post.date_of_request, 'type_of_request':post.type_of_request,
    'status':post.status,'company_name' :post.company_name,'sector':post.sector,'industry':post.industry,'area':post.area,'financial_year_end':post.financial_year_end,'company_type':post.company_type,
   'postal_address' : post.postal_address,'company_email':post.company_email,'postal_address':post.postal_address,'street_address':post.street_address,'reg_number':post.reg_number,'vat_number':post.vat_number,'tel':post.tel,
    'website':post.website,'date_inc':post.date_inc,'country_inc':post.country_inc,'chair_firstname':post.chair_firstname,'chair_lastname':post.chair_lastname,
   'chair_other':post.chair_other,'chair_nation':post.chair_nation,'chair_email':post.chair_email,'chair_phone':post.chair_phone,'ceo_firstname': post.ceo_firstname,
   'ceo_lastname':post.ceo_lastname,'ceo_other':post.ceo_other,'ceo_nation':post.ceo_nation, 'ceo_email':post.ceo_email,'ceo_phone':post.ceo_phone,
   'other_board_firstname':post.other_board_firstname,'other_board_lastname':post.other_board_lastname,'other_board_other':post.other_board_other,
   'other_board_nation':post.other_board_nation,'other_board_email':post.other_board_email,'other_board_phone':post.other_board_phone,'key_firstname':post.key_firstname,
   'key_lastname':post.key_lastname,'key_other':post.key_other,'key_nation':post.key_nation,'key_email':post.key_email,'key_phone':post.key_phone,
    'prev_name':post.prev_name,'prev_address':post.prev_address,'prev_city':post.prev_city,'prev_country':post.prev_country,'current_name':post.current_name 
    ,'current_address':post. current_address,'current_city':post.current_city  ,'current_country':post.current_country,'sec_name':post.sec_name,'sec_address':post.sec_address
    ,'sec_city':post. sec_city,'sec_country':post.sec_country,'contact_firstname ':post.contact_firstname,'contact_lastname':post. contact_lastname 
    ,'contact_other':post. contact_other,'contact_nation':post. contact_nation,'contact_email ':post.contact_email,'contact_dob ':post.contact_dob,'contact_phone':post.contact_phone,
    'brief_history ':post.brief_history,'service':post.service,  })
     
    for comment in comments:
        comment_array.append(comment.comment)

    temp.append({'comments': comment_array})

    return jsonify(temp)

@users.route('/administration/service_requests/corpupdate/<int:corprequestId>', methods=['POST'])
def updateCorpRequest(corprequestId):
    request = Corporate_request.query.get_or_404(corprequestId)
    form = ServiceRequestForm()
    if form.validate_on_submit:
        comment = RequestComment(comment=form.comment.data, service_id=corprequestId)
        request.status = form.newstatus.data
        db.session.add(comment)
        db.session.commit()
        flash("Request Updated", "success")
        return redirect(url_for('users.admin_service_requests'))

# search messages on messages.html 
@users.route('/messages/search', methods = ['POST'])
def searchMessages():
    search = request.form['search_term']
    if (len(search) == 0):
        messages = Contact.query.filter_by(status="False")
        new_messages = []
        for message in messages:
            new_messages.append({'id': message.id, 'firstname': message.firstname, 'lastname': message.lastname, 
            'company': message.company_name, 'timestamp': message.timestamp, 'status': message.status})

        return jsonify(new_messages)
    
    messages = Contact.query.filter(or_(Contact.firstname.like(('%' + search + '%')),
    Contact.lastname.like(('%' + search + '%')),
    Contact.company_name.like(('%' + search + '%'))))
    new_messages = []
    for message in messages:
        new_messages.append({'id': message.id, 'firstname': message.firstname, 'lastname': message.lastname, 
        'company': message.company_name, 'timestamp': message.timestamp, 'status': message.status})


@users.route('/benchmark_details', methods=['POST','GET'])
def b_details():


    tag = request.form['id']
    

  
    post = Benchmark_job.query.get_or_404(tag)

    temp = []
   

    temp.append({'id': post.id,'status':post.status, 'job_title':post.job_title , 'grade':post.grade ,'reporting_relationship':post.reporting_relationship,'job_description' :post.job_description,'duties_and_responsibility':post.duties_and_responsibility,'financial_responsibilities':post.financial_responsibilities,'technical_qualification':post.technical_qualification,'minimum_years_of_experience':post.minimum_years_of_experience})

    return jsonify(temp)


@users.route('/save_qualitative', methods=['POST','GET'])
def save_qualitative():

    main = Client.query.all()
    for i in main:
        if (i.user.id == current_user.id):
            main = i
    client = request.form['client']
    num_emp = request.form['num_emp']
    num_work_hours = request.form['num_work_hours']
    pol_structure = request.form['policy_structure']
    ovr_policy = request.form['ovr_policy']


    formal_salary_structure_ovr = request.form['formal_salary_structure_ovr']
    ss_adjusted = request.form['ss_adjusted']
    last_adj_date = request.form['last_adj_date']
    avg_inc = request.form['avg_inc']
    adj_basis = request.form['adj_basis']
    inflation = request.form['inflation']
    business_conditions = request.form['business_conditions']
    salary_levels = request.form['salary_levels']
    other_indicators = request.form['other_indicators']
    grade_ajs = request.form['grade_ajs']
    how_adjs_made = request.form['how_adjs_made']
    job_eval_sys = request.form['job_eval_sys']
    auto_inflation_adjs = request.form['auto_inflation_adjs']
    auto_inflation_adjs_exp = request.form['auto_inflation_adjs_exp']
    num_grade_levels = request.form['num_grade_levels']
    notch_diff = request.form['notch_diff']
    sal_increments = request.form['sal_increments']
    staff_progress = request.form['staff_progress']
    staff_progress_exp = request.form['staff_progress_exp']
    experience = request.form['experience']
    previous_salary = request.form['previous_salary']
    hiring_rate = request.form['hiring_rate']
    max_salary = request.form['max_salary']
    sal_exceeded = request.form['sal_exceeded']
    sal_exceeded_exp = request.form['sal_exceeded_exp']
    annual_cash_bonus = request.form['annual_cash_bonus']
    annual_cash_bonus_exp = request.form['annual_cash_bonus_exp']
    plans_eligibility = request.form['plans_eligibility']
    plans_eligibility_exp = request.form['plans_eligibility_exp']
    bonus_payout = request.form['bonus_payout']
    bonus_payout_exp = request.form['bonus_payout_exp']
    month_13 = request.form['month_13']
    month_13_payout = request.form['month_13_payout']
    month_13_payout_exp = request.form['month_13_payout_exp']
    month_13_payout_restriction = request.form['month_13_payout_restriction']
    direct_compensations = request.form['direct_compensations']
    num_leave_days = request.form['num_leave_days']
    sick_leave = request.form['sick_leave']
    maternity_leave = request.form['maternity_leave']
    paternity_leave = request.form['paternity_leave']
    compassionate_leave = request.form['compassionate_leave']
    other_leave = request.form['other_leave']
    redundancy = request.form['redundancy']
    



    test = bool(Qualitative_survey.query.filter_by(client_name=client,status="In Progress").first())
    if(test):

        query = Qualitative_survey.query.filter_by(client_name=client,status="In Progress").first()
        query.emp_number = num_emp
        query.working_hours=num_work_hours
        query.overtime_policy=ovr_policy
    
        db.session.commit()
        return('code submitted')
    
    else:
        qls = Qualitative_survey(client_name=client,status="In Progress",emp_number=num_emp,working_hours=num_work_hours,overtime_policy=ovr_policy,salary_structure=formal_salary_structure_ovr,salary_structure_adjustments=ss_adjusted,avg_perc_review=avg_inc,adjusment_basis=adj_basis,inflation_indicator=inflation,business_conditions_indicator=business_conditions,salary_level_indicator=salary_levels,other_indicator=other_indicators,isGradesAdjustedBySamePerc=grade_ajs,detailed_adjustments=how_adjs_made,job_evaluation=job_eval_sys,cost_of_living_adjustments_periodically=auto_inflation_adjs,cost_of_living_adjustments_periodically_basis=auto_inflation_adjs_exp,grade_levels=num_grade_levels,perc_grade_difference=notch_diff,grade_bases=sal_increments,staff_progress=staff_progress,experience_scale=experience,previous_scale=previous_salary,hiring_rate=hiring_rate,max_salary_grade=max_salary,max_salary_exceeded=sal_exceeded,max_salary_exceeded_reason=sal_exceeded_exp,haveIncentivePlans=annual_cash_bonus,incentive_plans=annual_cash_bonus_exp,annual_cash_eligibility=plans_eligibility,client_qual=main)
        db.session.add(qls)
        db.session.commit()
    
    

    return jsonify(pol_structure)

    return jsonify(new_messages)


@users.route("/administration/client_reports")
def client_reports():
    
    return render_template("client_hub_reports.html")


# @users.route('/messages/update/<int:messageId>', methods=['POST'])
# def updateMessage(messageId):
#     message = Contact.query.get_or_404(messageId)
#     form = MessageComment()
#     if form.validate_on_submit:
#         comment = Comment(comment=form.comment.data, contact_id=messageId)
#         message.status = form.my_status.data
#         db.session.add(comment)
#         db.session.commit()
#         flash("Message Updated", "success")
#         return redirect(url_for('users.messages'))
