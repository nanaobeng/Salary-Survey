from flask import Flask, render_template, url_for , flash, redirect, request , Blueprint, jsonify, session, json
from survey import db , bcrypt
from survey.users.forms import *
from survey.models import *
from flask_login import login_user, current_user, logout_user , login_required
from survey.users.utils import send_reset_email
from datetime import datetime
from dateutil import parser
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
        user = form.user_account.data,
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
        area = Area(area = form.name.data, industry_id = form.industry.data.id)
        
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
    searchform = MyForm()
    compform = ComparatorForm()
    if form.validate_on_submit():
        sur = Survey(name="test2",start_date=datetime(2012, 3, 3, 10, 10, 10),end_date=datetime(2012, 3, 3, 10, 10, 10),status="active",client_id=1)
        db.session.add(sur)
        db.session.commit()
        flash('Account Created','success')
        return redirect(url_for('users.login'))
    return render_template("new_create_survey.html",form=form,searchform=searchform,compform=compform)

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
    benchmark_jobs = Main_benchmark_job.query.filter_by(user_account=current_user, status='Pending').all()
    
    return render_template("new_view_client_benchmark.html",benchmark_jobs=benchmark_jobs)



@users.route("/my_benchmark_jobs/search_pool")
def client_search_job_pool():
    # usn = current_user
    # job = Main_benchmark_job.query.filter_by(user_account=usn).all()

    return render_template("client_search_job_pool.html")

@users.route("/job_pool/search", methods=['POST'])
def search_job_pool():
    
    search = request.form['search']
    search_result = []
    if search !='':
        jobs = Benchmark_job_pool.query.filter(Benchmark_job_pool.job_title.like(('%'+search+'%')))
        for job in jobs:
            search_result.append({'id':job.id,
            'job_title':job.job_title,
            'grade':job.grade,
            'department':job.department.department,
            'area':job.area.area,
             }) 
    
    return jsonify(search_result)

# get details of selected pool job to be displayed in modal
@users.route("/job_pool/search/view", methods = ['POST'])
def search_job_pool_view():
    id=request.form['id']
    search_result =[]
    job = Benchmark_job_pool.query.get_or_404(id)
    search_result = ({
        'job_title':job.job_title,
        'grade':job.grade,
        'department':job.department.department,

        'reporting_relationship':job.reporting_relationship or '',
        'job_description':job.job_description or '',
        'key_duties':job.duties_and_responsibility or '',
        'financial_responsibilies':job.financial_responsibilities or '',
        'technical_qualifications':job.technical_qualification or '',
        'years_of_experience':job.minimum_years_of_experience or '',
        })
    return jsonify(search_result)

# Route to new benchmark job when adding from pool
@users.route("/my_benchmark_jobs/new",methods=['POST','GET'])
def my_benchmark_jobs_create():
    job = {}
    try:
        if request.args.get('pool'):
            id = request.args.get('pool')
            job = Benchmark_job_pool.query.get_or_404(id)
            # job = {
            #     'job_title':job_.job_title
            # }
    except:
        pass
    form = SurveyForm()
    user = current_user
    if form.validate_on_submit():
        b_job = Main_benchmark_job(job_title=form.job_title.data,grade=form.grade.data,main_department=form.department.data,reporting_relationship=form.reporting_relationship.data,job_description=form.job_desc.data,duties_and_responsibility=form.key_duties.data,financial_responsibilities=form.fin_res.data,technical_qualification=form.tech_qual.data,minimum_years_of_experience=form.exp_years.data,user_account=user, status='Pending')
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
        return redirect(url_for('users.my_benchmark_jobs')) 
    return render_template("new_client_create_benchmark.html",form=form, job=job)

@users.route("/my_surveys")
def my_surveys():
    usn = current_user.id
    query = []
    final_list = []
    surveys = Survey_comparator.query.all()
    bench = Benchmark_job.query.all()
    for survey in surveys:
        if survey.client.user.id == usn:
            query.append(survey)

    for i in query:
        for j in bench:
            if i.comparator.id == j.comp_benchmark.id and j not in final_list:
                final_list.append(j)
            
               

    return render_template("quantitative_survey_overview.html",usn=usn,query=final_list)
    

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
    compform = ComparatorForm()
    query = Survey.query.all()
    return render_template("new_view_survey.html",query=query,compform=compform)

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
    total_num_requests = json.dumps(Individual_request.query.count() + Corporate_request.query.count())
    total_indv_requests = json.dumps(Individual_request.query.count())
    total_corp_requests = json.dumps(Corporate_request.query.count())

    total_pending_requests = json.dumps(Individual_request.query.filter_by(status='pending').count() + Corporate_request.query.filter_by(status='pending').count())
    total_awaiting_requests = json.dumps(Individual_request.query.filter_by(status='requesting_client_information').count() + Corporate_request.query.filter_by(status='requesting_client_information').count())
    total_fpass_requests = json.dumps(Individual_request.query.filter_by(status='first_pass').count() + Corporate_request.query.filter_by(status='first_pass').count())
    total_ccheck_requests = json.dumps(Individual_request.query.filter_by(status='conflict_check').count() + Corporate_request.query.filter_by(status='conflict_check').count())
    total_fcomp_requests = json.dumps(Individual_request.query.filter_by(status='finish_completion').count() + Corporate_request.query.filter_by(status='finish_completion').count())
    total_submitted_requests = json.dumps(Individual_request.query.filter_by(status='submitted').count() + Corporate_request.query.filter_by(status='submitted').count())
    
    num_indv_pending_requests = Individual_request.query.filter_by(status='pending').count()
    num_indv_awaiting_requests = Individual_request.query.filter_by(status='requesting_client_information').count()
    num_indv_first_pass_requests = Individual_request.query.filter_by(status='first_pass').count()
    num_indv_conflict_check_requests = Individual_request.query.filter_by(status='conflict_check').count()
    num_indv_finish_completion_requests = Individual_request.query.filter_by(status='finish_completion').count()
    num_indv_submitted_requests = Individual_request.query.filter_by(status='submitted').count()

    num_corp_pending_requests = Corporate_request.query.filter_by(status='pending').count()
    num_corp_awaiting_requests = Corporate_request.query.filter_by(status='requesting_client_information').count()
    num_corp_first_pass_requests = Corporate_request.query.filter_by(status='first_pass').count()
    num_corp_conflict_check_requests = Corporate_request.query.filter_by(status='conflict_check').count()
    num_corp_finish_completion_requests = Corporate_request.query.filter_by(status='finish_completion').count()
    num_corp_submitted_requests = Corporate_request.query.filter_by(status='submitted').count()

    total_clients = json.dumps(Client.query.count())
    total_active_clients = json.dumps(Client.query.filter_by(status='active').count())
    total_inactive_clients = json.dumps(Client.query.filter_by(status='Inactive').count())

    total_messages = json.dumps(Contact.query.count())
    total_open_messages = json.dumps(Contact.query.filter_by(status='Open').count())
    total_closed_messages = json.dumps(Contact.query.filter_by(status='Closed').count())
    
    new_indv_requests = Individual_request.query.filter_by(status='pending')
    new_corp_requests = Corporate_request.query.filter_by(status='pending')
    new_messages = Contact.query.filter_by(status='Open')

    return render_template("client_hub.html", total_num_requests=total_num_requests, 
    total_indv_requests=total_indv_requests, total_corp_requests=total_corp_requests,
    total_pending_requests=total_pending_requests, total_awaiting_requests=total_awaiting_requests,
    total_fpass_requests=total_fpass_requests, total_ccheck_requests=total_ccheck_requests,
    total_fcomp_requests=total_fcomp_requests, total_submitted_requests=total_submitted_requests,
    num_indv_pend=num_indv_pending_requests, num_indv_await=num_indv_awaiting_requests,
    num_indv_fp=num_indv_first_pass_requests, num_indv_cc=num_indv_conflict_check_requests,
    num_indv_fc=num_indv_finish_completion_requests, num_indv_sub=num_indv_submitted_requests, 
    num_corp_pend=num_corp_pending_requests, num_corp_await=num_corp_awaiting_requests,
    num_corp_fp=num_corp_first_pass_requests, num_corp_cc=num_corp_conflict_check_requests,
    num_corp_fc=num_corp_finish_completion_requests, num_corp_sub=num_corp_submitted_requests,
    total_clients=total_clients, total_active_clients=total_active_clients, total_inactive_clients=total_inactive_clients,
    total_messages=total_messages, total_open_messages=total_open_messages, total_closed_messages=total_closed_messages,
    new_indv_requests=new_indv_requests, new_corp_requests=new_corp_requests, new_messages=new_messages)

    
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


@users.route("/administration/config/grades")
def admin_grades():
    return render_template("admin_grades.html")


@users.route("/administration/config/permissions")
def admin_permissions():
    return render_template("admin_permissions.html")


### Begining of block working on admin viewing comparator jobs and approving

# Route for admin to view all jobs from comparators
@users.route("/view_comparator_jobs", methods=['POST', 'GET'])
def admin_view_comparator_jobs():
    benchmark_jobs = Benchmark_job.query.filter_by(status='Pending')
    form = BenchmarkJobComment()
    if form.validate_on_submit():
        benchmark_job = Benchmark_job.query.get_or_404(id)
        comment = form.comment.data
        new_comment = Comparator_job_comment(comment=comment, main_benchmark_job_id=1)
        db.session.add(new_comment)
        benchmark_job.status = 'Rejected'
        db.session.commit()
        flash('Job Updated', 'Success')
        return redirect(url_for('users.admin_view_client_benchmark_jobs'))

    return render_template("admin_view_client_benchmark_jobs.html", benchmark_jobs = benchmark_jobs, form=form)


# Filter benchmark jobs
# @users.route("/client_benchmark_job/filter", methods = ['POST'])
# def filter_client_jobs():
#     status = request.form.getlist('status[]')
#     client = request.form.getlist('client[]')
#     filtered_jobs = []
#     # filter if status and client are both selected
#     if len(status) >0 and len(client)>0:
#         for status_ in status:
#             for client_ in client:
#                 user_id = Client.query.get_or_404(client_).user_id
                
#                 # return jsonify(client_object)
#                 benchmark_jobs = Main_benchmark_job.query.filter_by(status=status_, user = user_id)
#                 for benchmark_job in benchmark_jobs:
#                     filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
#         return jsonify(filtered_jobs)

#     # filter if status is selected and no client selected
#     if len(status) >0 and len(client)==0:
#         for status_ in status:
            
#             benchmark_jobs = Main_benchmark_job.query.filter_by(status=status_)
#             for benchmark_job in benchmark_jobs:
#                 filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
#         return jsonify(filtered_jobs)

#     # filter if client is selected and no status selected
#     if len(status) ==0 and len(client)>0:
#         for client_ in client:
#             user_id = Client.query.get_or_404(client_).user_id
#             benchmark_jobs = Main_benchmark_job.query.filter_by(user=user_id)
#             for benchmark_job in benchmark_jobs:
#                 filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
#         return jsonify(filtered_jobs)


#     # query if no filter is selected
#     if len(status) ==0 and len(client)==0:
#         benchmark_jobs = Main_benchmark_job.query.filter_by(status='Pending')
#         for benchmark_job in benchmark_jobs:
#             filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
#         return jsonify(filtered_jobs)


#Reject benchmark_job
@users.route("/comparator_job/reject/<int:id>", methods=['POST'])
def reject_comparator_job(id):
    form = BenchmarkJobComment()
    if form.validate_on_submit():
        benchmark_job = Benchmark_job.query.get_or_404(id)
        comment = form.comment.data
        new_comment = Comparator_job_comment(comment=comment, comparator_job_id=id)
        db.session.add(new_comment)
        benchmark_job.status = 'Rejected'
        db.session.commit()
        flash('Job Updated', 'Success')
        return redirect(url_for('users.admin_view_client_benchmark_jobs'))

# Approve client benchmark Job
@users.route("/comparator_job/approve", methods = ['POST'])
def approve_comparator_job():
    
    id = request.form['id']
   
    benchmark_job = Benchmark_job.query.get_or_404(id)
    benchmark_job.status = 'Approved'

    # Check if comment is not blank and add to comment table
    comment = request.form['comment']
    if comment != '':
        new_comment = Comparator_job_comment(comment=comment, comparator_job_id=id)
        db.session.add(new_comment)
    db.session.commit()
    flash('Job Updated', 'Success')
    return 'true'

# Route to search for comparator based of search input and return to input fielf
# @users.route("/client/search", methods =['POST'])
# def search_client():
#     search = request.form['search']
#     clients = Client.query.filter(Client.company_name.like(('%'+search+'%')))
#     new_clients =[]
#     for client in clients:
#         new_clients.append({'id':client.id,'name':client.company_name})
#     return jsonify(new_clients)

# Route to get job details and send back to ajax function to be displayed in modal
@users.route("/comparator_job/view", methods=['POST'])
def view_comparator_job():
    id = request.form['id']
    benchmark_job = Comparator_job.query.get_or_404(id)

    comments = []
    for comment in benchmark_job.comment:
        comments.append(comment.comment)
    new_benchmark_job = {
        'id':benchmark_job.id, 
        'job_title':benchmark_job.job_title,
        'grade':benchmark_job.grade,
        'department':benchmark_job.main_department.department,
        'reporting_relationship':benchmark_job.reporting_relationship,
        'job_description':benchmark_job.job_description,
        'key_duties':benchmark_job.duties_and_responsibility,
        'financial_responsibilies':benchmark_job.financial_responsibilities,
        'technical_qualifications':benchmark_job.technical_qualification,
        'years_of_experience':benchmark_job.minimum_years_of_experience,
        'status_':benchmark_job.status,
        'base_salary': "{:,.2f}".format(benchmark_job.base[0].monthly_base_salary or 0),
        'company_performance_bonus': "{:,.2f}".format(benchmark_job.incentive[0].company_performance or 0) ,
        'individual_performance_bonus': "{:,.2f}".format(benchmark_job.incentive[0].individual_performance or 0),
        'annual_bonus': "{:,.2f}".format(benchmark_job.incentive[0].annual_incentive or 0),
        'incentive_bonus': "{:,.2f}".format(benchmark_job.incentive[0].incentive or 0),
        'other_bonus': "{:,.2f}".format(benchmark_job.incentive[0].other_cash or 0),
        'b_staff_bus': "{:,.2f}".format(benchmark_job.benefit[0].staff_bus or 0),
        'b_company_car': "{:,.2f}".format(benchmark_job.benefit[0].company_car or 0),
        'b_personal_travel': "{:,.2f}".format(benchmark_job.benefit[0].personal_travel or 0),
        'b_petrol': "{:,.2f}".format(benchmark_job.benefit[0].petrol or 0),
        'b_vehicle': "{:,.2f}".format(benchmark_job.benefit[0].vehicle_maintenance or 0),
        'b_driver': "{:,.2f}".format(benchmark_job.benefit[0].driver or 0),
        'b_health_insurance': "{:,.2f}".format(benchmark_job.benefit[0].health_insurance or 0),
        'b_medical_assistance': "{:,.2f}".format(benchmark_job.benefit[0].medical_assistance or 0),
        'b_funeral_assistance': "{:,.2f}".format(benchmark_job.benefit[0].funeral_assistance or 0),
        'b_life_insurance': "{:,.2f}".format(benchmark_job.benefit[0].life_insurance or 0),
        'b_accident': "{:,.2f}".format(benchmark_job.benefit[0].group_accident or 0),
        'b_club_membership': "{:,.2f}".format(benchmark_job.benefit[0].club_membership or 0),
        'b_school_fees': "{:,.2f}".format(benchmark_job.benefit[0].school_fees or 0),
        'b_vacation': "{:,.2f}".format(benchmark_job.benefit[0].vacation or 0),
        'b_housing': "{:,.2f}".format(benchmark_job.benefit[0].housing or 0),
        'b_telephone': "{:,.2f}".format(benchmark_job.benefit[0].telephone or 0),
        'b_security': "{:,.2f}".format(benchmark_job.benefit[0].security or 0),
        'b_other': "{:,.2f}".format(benchmark_job.benefit[0].other_benefits or 0),
        
        'a_vehicle_maintenance': "{:,.2f}".format(benchmark_job.allowance[0].vehicle_maintenance or 0),
        'a_vehicle': "{:,.2f}".format(benchmark_job.allowance[0].vehicle or 0),
        'a_transport': "{:,.2f}".format(benchmark_job.allowance[0].transport or 0),
        'a_fuel': "{:,.2f}".format(benchmark_job.allowance[0].fuel or 0),
        'a_car': "{:,.2f}".format(benchmark_job.allowance[0].car or 0),
        'a_driver': "{:,.2f}".format(benchmark_job.allowance[0].driver or 0),
        'a_domestic_safety': "{:,.2f}".format(benchmark_job.allowance[0].domestic_safety or 0),
        'a_housing': "{:,.2f}".format(benchmark_job.allowance[0].housing or 0),
        'a_utilities': "{:,.2f}".format(benchmark_job.allowance[0].utilities or 0),
        'a_meal': "{:,.2f}".format(benchmark_job.allowance[0].meal or 0),
        'a_telephone': "{:,.2f}".format(benchmark_job.allowance[0].telephone or 0),
        'a_entertainment': "{:,.2f}".format(benchmark_job.allowance[0].entertainment or 0),
        'a_education': "{:,.2f}".format(benchmark_job.allowance[0].education_support or 0),
        'a_vacation': "{:,.2f}".format(benchmark_job.allowance[0].vacation or 0),
        'a_uniform': "{:,.2f}".format(benchmark_job.allowance[0].uniform or 0),
        'a_mobile_money': "{:,.2f}".format(benchmark_job.allowance[0].mobile_money or 0),
        'a_miscellaneous': "{:,.2f}".format(benchmark_job.allowance[0].miscellaenous or 0),
       

        'comments_': comments
        }
    return jsonify(new_benchmark_job)



### End of block working on admin viewing client benchmark jobs and approving





### Begining of block working on admin viewing client benchmark jobs and approving

# Route for admin to view all benchmark jobs from clients
@users.route("/view_client_benchmark_jobs", methods=['POST', 'GET'])
def admin_view_client_benchmark_jobs():
    benchmark_jobs = Main_benchmark_job.query.filter_by(status='Pending')
    form = BenchmarkJobComment()
    if form.validate_on_submit():
        benchmark_job = Main_benchmark_job.query.get_or_404(id)
        comment = form.comment.data
        new_comment = Main_benchmark_job_comment(comment=comment, main_benchmark_job_id=id)
        db.session.add(new_comment)
        benchmark_job.status = 'Rejected'
        db.session.commit()
        flash('Job Updated', 'Success')
        return redirect(url_for('users.admin_view_client_benchmark_jobs'))

    return render_template("admin_view_client_benchmark_jobs.html", benchmark_jobs = benchmark_jobs, form=form)


# Filter benchmark jobs
@users.route("/client_benchmark_job/filter", methods = ['POST'])
def filter_jobs():
    status = request.form.getlist('status[]')
    
    filtered_jobs = []
    # A separate condition to differentiate filters for client from filter for admin
    is_client = request.form['is_client']
    if is_client == 'client':
        
        for status_ in status:
            benchmark_jobs = Main_benchmark_job.query.filter_by(status=status_, user_account = current_user)
           
            for benchmark_job in benchmark_jobs:
                filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
        return jsonify(filtered_jobs)

    client = request.form.getlist('client[]')
    # filter if status and client are both selected
    if len(status) >0 and len(client)>0:
        for status_ in status:
            for client_ in client:
                user_id = Client.query.get_or_404(client_).user_id
                
                # return jsonify(client_object)
                benchmark_jobs = Main_benchmark_job.query.filter_by(status=status_, user = user_id)
                for benchmark_job in benchmark_jobs:
                    filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
        return jsonify(filtered_jobs)

    # filter if status is selected and no client selected
    if len(status) >0 and len(client)==0:
        for status_ in status:
            
            benchmark_jobs = Main_benchmark_job.query.filter_by(status=status_)
            for benchmark_job in benchmark_jobs:
                filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
        return jsonify(filtered_jobs)

    # filter if client is selected and no status selected
    if len(status) ==0 and len(client)>0:
        for client_ in client:
            user_id = Client.query.get_or_404(client_).user_id
            benchmark_jobs = Main_benchmark_job.query.filter_by(user=user_id)
            for benchmark_job in benchmark_jobs:
                filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
        return jsonify(filtered_jobs)


    # query if no filter is selected
    if len(status) ==0 and len(client)==0:
        benchmark_jobs = Main_benchmark_job.query.filter_by(status='Pending')
        for benchmark_job in benchmark_jobs:
            filtered_jobs.append({'id':benchmark_job.id, 'job_title':benchmark_job.job_title, 'client':benchmark_job.user_account.client[0].company_name, 'department':benchmark_job.main_department.department, 'grade':benchmark_job.grade, 'timestamp':benchmark_job.timestamp, 'status':benchmark_job.status})
        return jsonify(filtered_jobs)


#Reject benchmark_job
@users.route("/client_benchmark_job/reject/<int:id>", methods=['POST'])
def reject_client_benchmark_job(id):
    form = BenchmarkJobComment()
    if form.validate_on_submit():
        benchmark_job = Main_benchmark_job.query.get_or_404(id)
        comment = form.comment.data
        new_comment = Main_benchmark_job_comment(comment=comment, main_benchmark_job_id=id)
        db.session.add(new_comment)
        benchmark_job.status = 'Rejected'
        db.session.commit()
        flash('Job Updated', 'Success')
        return redirect(url_for('users.admin_view_client_benchmark_jobs'))

# Approve client benchmark Job
@users.route("/client_benchmark_job/approve", methods = ['POST'])
def approve_client_benchmark_job():
    
    id = request.form['id']
   
    benchmark_job = Main_benchmark_job.query.get_or_404(id)
    benchmark_job.status = 'Approved'

    # Check if comment is not blank and add to comment table
    comment = request.form['comment']
    if comment != '':
        new_comment = Main_benchmark_job_comment(comment=comment, main_benchmark_job_id=id)
        db.session.add(new_comment)
    db.session.commit()
    flash('Job Updated', 'Success')
    return 'true'

# Route to search for client based of search input and return to input fielf
@users.route("/client/search", methods =['POST'])
def search_client():
    search = request.form['search']
    clients = Client.query.filter(Client.company_name.like(('%'+search+'%')))
    new_clients =[]
    for client in clients:
        new_clients.append({'id':client.id,'name':client.company_name})
    return jsonify(new_clients)

# Route to get job details and send back to ajax function to be displayed in modal
@users.route("/client_benchmark_job/view", methods=['POST'])
def view_client_benchmark_job():
    id = request.form['id']
    benchmark_job = Main_benchmark_job.query.get_or_404(id)

    comments = []
    for comment in benchmark_job.comment:
        comments.append(comment.comment)
    new_benchmark_job = {
        'id':benchmark_job.id, 
        'job_title':benchmark_job.job_title,
        'grade':benchmark_job.grade,
        'department':benchmark_job.main_department.department,
        'reporting_relationship':benchmark_job.reporting_relationship,
        'job_description':benchmark_job.job_description,
        'key_duties':benchmark_job.duties_and_responsibility,
        'financial_responsibilies':benchmark_job.financial_responsibilities,
        'technical_qualifications':benchmark_job.technical_qualification,
        'years_of_experience':benchmark_job.minimum_years_of_experience,
        'status_':benchmark_job.status,
        'base_salary': "{:,.2f}".format(benchmark_job.base[0].monthly_base_salary or 0),
        'company_performance_bonus': "{:,.2f}".format(benchmark_job.incentive[0].company_performance or 0) ,
        'individual_performance_bonus': "{:,.2f}".format(benchmark_job.incentive[0].individual_performance or 0),
        'annual_bonus': "{:,.2f}".format(benchmark_job.incentive[0].annual_incentive or 0),
        'incentive_bonus': "{:,.2f}".format(benchmark_job.incentive[0].incentive or 0),
        'other_bonus': "{:,.2f}".format(benchmark_job.incentive[0].other_cash or 0),
        'b_staff_bus': "{:,.2f}".format(benchmark_job.benefit[0].staff_bus or 0),
        'b_company_car': "{:,.2f}".format(benchmark_job.benefit[0].company_car or 0),
        'b_personal_travel': "{:,.2f}".format(benchmark_job.benefit[0].personal_travel or 0),
        'b_petrol': "{:,.2f}".format(benchmark_job.benefit[0].petrol or 0),
        'b_vehicle': "{:,.2f}".format(benchmark_job.benefit[0].vehicle_maintenance or 0),
        'b_driver': "{:,.2f}".format(benchmark_job.benefit[0].driver or 0),
        'b_health_insurance': "{:,.2f}".format(benchmark_job.benefit[0].health_insurance or 0),
        'b_medical_assistance': "{:,.2f}".format(benchmark_job.benefit[0].medical_assistance or 0),
        'b_funeral_assistance': "{:,.2f}".format(benchmark_job.benefit[0].funeral_assistance or 0),
        'b_life_insurance': "{:,.2f}".format(benchmark_job.benefit[0].life_insurance or 0),
        'b_accident': "{:,.2f}".format(benchmark_job.benefit[0].group_accident or 0),
        'b_club_membership': "{:,.2f}".format(benchmark_job.benefit[0].club_membership or 0),
        'b_school_fees': "{:,.2f}".format(benchmark_job.benefit[0].school_fees or 0),
        'b_vacation': "{:,.2f}".format(benchmark_job.benefit[0].vacation or 0),
        'b_housing': "{:,.2f}".format(benchmark_job.benefit[0].housing or 0),
        'b_telephone': "{:,.2f}".format(benchmark_job.benefit[0].telephone or 0),
        'b_security': "{:,.2f}".format(benchmark_job.benefit[0].security or 0),
        'b_other': "{:,.2f}".format(benchmark_job.benefit[0].other_benefits or 0),
        
        'a_vehicle_maintenance': "{:,.2f}".format(benchmark_job.allowance[0].vehicle_maintenance or 0),
        'a_vehicle': "{:,.2f}".format(benchmark_job.allowance[0].vehicle or 0),
        'a_transport': "{:,.2f}".format(benchmark_job.allowance[0].transport or 0),
        'a_fuel': "{:,.2f}".format(benchmark_job.allowance[0].fuel or 0),
        'a_car': "{:,.2f}".format(benchmark_job.allowance[0].car or 0),
        'a_driver': "{:,.2f}".format(benchmark_job.allowance[0].driver or 0),
        'a_domestic_safety': "{:,.2f}".format(benchmark_job.allowance[0].domestic_safety or 0),
        'a_housing': "{:,.2f}".format(benchmark_job.allowance[0].housing or 0),
        'a_utilities': "{:,.2f}".format(benchmark_job.allowance[0].utilities or 0),
        'a_meal': "{:,.2f}".format(benchmark_job.allowance[0].meal or 0),
        'a_telephone': "{:,.2f}".format(benchmark_job.allowance[0].telephone or 0),
        'a_entertainment': "{:,.2f}".format(benchmark_job.allowance[0].entertainment or 0),
        'a_education': "{:,.2f}".format(benchmark_job.allowance[0].education_support or 0),
        'a_vacation': "{:,.2f}".format(benchmark_job.allowance[0].vacation or 0),
        'a_uniform': "{:,.2f}".format(benchmark_job.allowance[0].uniform or 0),
        'a_mobile_money': "{:,.2f}".format(benchmark_job.allowance[0].mobile_money or 0),
        'a_miscellaneous': "{:,.2f}".format(benchmark_job.allowance[0].miscellaenous or 0),
       

        'comments_': comments
        }
    return jsonify(new_benchmark_job)


    
### End of block working on admin viewing comparator jobs and approving





@users.route("/administration/config/benchmark_jobs")
def admin_benchmark_jobs():
    return render_template("admin_benchmark_jobs.html")

@users.route("/administration/config/create_benchmark_job", methods=['POST', 'GET'])
def create_benchmark_job():
    if request.method == 'POST':
        
        return 'success'
    return render_template("create_benchmark_job.html")


@users.route("/survey/quantitative/<int:id>/<int:usn>/<int:sid>",methods=['POST','GET'])
def quantitative_survey(id,usn,sid):
    job = Benchmark_job.query.get_or_404(id)
    form = SurveyForm()

    dept = Department.query.all()

    s_comp = Survey_comparator.query.all()
    
    s_compp = Survey_comparator.query.all()          
        
    
    status = False
    comp = Comparator_job.query.all()


    for sur in s_comp:
                if(sur.client.user.id == usn and sur.comparator.id == sid and job.comp_benchmark.id == sid ):
                    s_comp = sur

    for sur in comp:
                if(id == sur.benchmark.id and usn == sur.comparator.client.user.id):
                    s_compp = sur
    for c in comp:
        if(c.benchmark.id == id ):
            status = True
    if form.validate_on_submit():
        if(status == False):
            
                        
            benifit = Benefit(staff_bus = 2)
            allowance = Allowance(housing = 33)
            incentive = Incentive(other_cash = 4)
            base = Base_salary(monthly_base_salary=4)
            new_comparator = Comparator_job(job_title=request.form['j_t'],department=form.department.data,grade="test grade",reporting_relationship="sample",job_match=20,comparator=s_comp,benchmark=job,comp_benchmark_base=base,comp_benchmark_incentive=incentive,comp_benchmark_allowance=allowance,comp_benchmark_benefit=benifit) 
            db.session.add(benifit)
            db.session.add(allowance)
            db.session.add(incentive)
            db.session.add(base)
            db.session.add(new_comparator)
            try:
                db.session.commit()
                flash('Survey Completed','success')
                return redirect(url_for('users.my_surveys'))
            except:
                flash('There was an issue completing the survey','danger')
                return redirect(url_for('users.my_surveys'))

        else:
            s_comp.job_title = form.job_title.data
            s_comp.grade = form.grade.data
            s_comp.job_title = form.department.data
            s_comp.jreporting_relationship = form.reporting_relationship.data
            #s_comp.job_title = form.job_match.data
          

            s_comp.comp_benchmark_base.monthly_base_salary=form.base_salary.data
        
            s_comp.comp_benchmark_incentive.company_performance=form.company_bonus_performance.data
            s_comp.comp_benchmark_incentive.individual_performance=form.individual_bonus_performance.data
            s_comp.comp_benchmark_incentive.annual_incentive=form.annual_bonus.data
            s_comp.comp_benchmark_incentive.incentive=form.incentive_bonus.data
            s_comp.comp_benchmark_incentive.other_cash=form.other_bonus.data
        

            s_comp.comp_benchmark_benefit.staff_bus=form.staff_bus.data
            s_comp.comp_benchmark_benefit.company_car=form.company_car.data
            s_comp.comp_benchmark_benefit.personal_travel=form.personal_travel.data
            s_comp.comp_benchmark_benefit.petrol=form.petrol.data
            s_comp.comp_benchmark_benefit.vehicle_maintenance=form.vehicle.data
            s_comp.comp_benchmark_benefit.driver=form.driver.data
            s_comp.comp_benchmark_benefit.health_insurance=form.health_insurance.data
            s_comp.comp_benchmark_benefit.medical_assistance=form.medical_assistance.data
            s_comp.comp_benchmark_benefit.funeral_assistance=form.funeral_assistance.data
            s_comp.comp_benchmark_benefit.life_insurance=form.life_insurance.data
            s_comp.comp_benchmark_benefit.group_accident=form.group_accident.data
            s_comp.comp_benchmark_benefit.club_membership=form.club_membership.data
            s_comp.comp_benchmark_benefit.school_fees=form.school_fees.data
            s_comp.comp_benchmark_benefit.vacation=form.vacation.data
            s_comp.comp_benchmark_benefit.housing=form.housing.data
            s_comp.comp_benchmark_benefit.telephone=form.telephone.data
            s_comp.comp_benchmark_benefit.security=form.security.data
            s_comp.comp_benchmark_benefit.other_benefits=form.other_benefits.data

            s_comp.comp_benchmark_allowance.vehicle_maintenance=form.vehicle_maintenance.data
            s_comp.comp_benchmark_allowance.vehicle=form.allowance_vehicle.data
            s_comp.comp_benchmark_allowance.transport=form.transport.data
            s_comp.comp_benchmark_allowance.fuel=form.fuel.data
            s_comp.comp_benchmark_allowance.car=form.car.data
            s_comp.comp_benchmark_allowance.driver=form.allowance_driver.data
            s_comp.comp_benchmark_allowance.domestic_safety=form.domestic.data
            s_comp.comp_benchmark_allowance.housing=form.allowance_housing.data
            s_comp.comp_benchmark_allowance.utilities=form.utilities.data
            s_comp.comp_benchmark_allowance.meal=form.meal.data
            s_comp.comp_benchmark_allowance.telephone=form.allowance_telephone.data
            s_comp.comp_benchmark_allowance.entertainment=form.entertainment.data
            s_comp.comp_benchmark_allowance.education_support=form.education.data
            s_comp.comp_benchmark_allowance.vacation=form.vacation_allowance.data
            s_comp.comp_benchmark_allowance.uniform=form.uniform.data
            s_comp.comp_benchmark_allowance.mobile_money=form.mobile_money.data
            s_comp.comp_benchmark_allowance.miscellaenous=form.misc.data
            s_comp.status = "Completed"
            try:
                db.session.commit()
                flash('Survey Completed','success')
                return redirect(url_for('users.my_surveys'))
            except:
                flash('There was an issue completing the survey','danger')
                return redirect(url_for('users.my_surveys'))

       

        



    if(status == True):
        return render_template("quantitative_survey.html",form=form, job=s_compp,state="saved",dept=dept)
    else:
        return render_template("quantitative_survey.html",form=form, job=Benchmark_job.query.get_or_404(id),state="unsaved",dept=dept)

    
    

@users.route("/survey/quantitative/view/<int:id>/<int:usn>/<int:sid>",methods=['POST','GET'])
def quantitative_survey_view(id,usn,sid):
    job = Benchmark_job.query.get_or_404(id)
    form = SurveyForm()
    s_comp = Survey_comparator.query.all()
    
    s_compp = Survey_comparator.query.all()          
        
    
    status = False
    comp = Comparator_job.query.all()


    for sur in comp:
                if(id == sur.benchmark.id and usn == sur.comparator.client.user.id):
                    s_comp = sur

    return render_template("view_quant.html",form=form, job=s_comp)

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
        job.status = 'Pending'

        base.monthly_base_salary= request.form['base_salary'] or None

        incentive.company_performance = request.form['cmp_bonus'] or None
        incentive.individual_performance = request.form['indv_bonus'] or None
        incentive.annual_incentive = request.form['annual_bonus'] or None
        incentive.incentive = request.form['inv_bonus'] or None
        incentive.other_cash = request.form['other_bonus'] or None


        benefit.staff_bus = request.form['staff_bus'] or None
        benefit.company_car = request.form['cmp_car'] or None
        benefit.personal_travel = request.form['personal_travel'] or None
        benefit.petrol = request.form['petrol'] or None
        benefit.vehicle_maintenance = request.form['vehicle'] or None
        benefit.driver = request.form['driver'] or None
        benefit.health_insurance= request.form['htl_ins'] or None
        benefit.medical_assistance = request.form['medi_assis'] or None
        benefit.funeral_assistance = request.form['funeral_assistance'] or None
        benefit.life_insurance = request.form['life_insurance'] or None
        benefit.group_accident = request.form['group_accident'] or None
        benefit.club_membership  = request.form['club_membership'] or None
        benefit.school_fees = request.form['school_fees'] or None
        benefit.vacation= request.form['vacation'] or None
        benefit.housing = request.form['housing'] or None
        benefit.telephone = request.form['telephone'] or None
        benefit.security = request.form['security'] or None
        benefit.other_benefits = request.form['other_benefits'] or None


        allowance.vehicle_maintenance = request.form['vehicle_maintenance'] or None
        allowance.vehicle = request.form['allowance_vehicle'] or None
        allowance.transport = request.form['transport'] or None
        allowance.fuel = request.form['fuel'] or None
        allowance.car = request.form['car'] or None
        allowance.driver = request.form['allowance_driver'] or None
        allowance.domestic_safety = request.form['domestic'] or None
        allowance.housing = request.form['allowance_housing'] or None
        allowance.utilities = request.form['utilities'] or None
        allowance.meal = request.form['meal'] or None
        allowance.telephone = request.form['allowance_telephone'] or None
        allowance.entertainment = request.form['entertainment'] or None
        allowance.education_support = request.form['education'] or None
        allowance.vacation = request.form['allowance_vacation'] or None
        allowance.uniform = request.form['uniform'] or None
        allowance.mobile_money = request.form['momo'] or None
        allowance.miscellaenous = request.form['misc'] or None
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
    empty_arr = []
    tag = request.form["id"]
    search = "%{}%".format(tag)
    if(len(tag) == 0):
        return jsonify(empty_arr)

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
    empty_arr = []
    tag = request.form['id']
    search = "%{}%".format(tag)
    if(len(tag) == 0):
        return jsonify(empty_arr)

  
    posts = Main_benchmark_job.query.filter_by(id=tag)
    temp = []
    for post in posts:

        temp.append({'id': post.id, 'job_title':post.job_title ,'main_department' :post.main_department.department, 'job_description' : post.job_description, 'grade':post.grade})

    return jsonify(temp)








@users.route('/compare', methods=['POST'])
def comparedic():
    empty_arr = []
    tag = request.form["id"]
    search = "%{}%".format(tag)
    
    if(len(tag) == 0):
        return jsonify(empty_arr)

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
    start_date = parser.parse(start_date)
    #search = "%{}%".format(tag)

    bench_split = bench.split(',')
    comp_split = comp.split(',')
    posts = Client.query.filter_by(company_name=client).first()
    b_id = "f"

    #client_id = temp[0].id
    sur = Survey(name=survey,status="Inactive",survey_client=posts,start_date=start_date)
    db.session.add(sur)
   
    
    
    for i in bench_split:
        b_id = (int(i.replace("b", "")))
        main = Main_benchmark_job.query.filter_by(id=b_id).first()
        base = Base_salary.query.filter_by(id=main.id).first()
        incentive = Incentive.query.filter_by(id=main.id).first()
        allowance = Allowance.query.filter_by(id=main.id).first()
        benefit = Benefit.query.filter_by(id=main.id).first()
        db.session.add(Benchmark_job(job_title=main.job_title,department=main.main_department,grade=main.grade,reporting_relationship=main.reporting_relationship,job_description=main.job_description,duties_and_responsibility=main.duties_and_responsibility,financial_responsibilities= main.financial_responsibilities,technical_qualification=main.technical_qualification,minimum_years_of_experience=main.minimum_years_of_experience,benchmark=posts,comp_benchmark=sur,comp_benchmark_allowance=allowance,comp_benchmark_benefit=benefit,comp_benchmark_incentive=incentive,comp_benchmark_base=base))
        for c in comp_split :
            c_id = (int(c.replace("c", "")))
            cli = Client.query.filter_by(id=c_id).first()
            db.session.add(Survey_comparator(comparator=sur,client=cli,status="Inactive"))
            
    
    db.session.commit()
    return jsonify(start_date)



 

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
            temp_c.append(c.client.company_name)

    temp_b = list(dict.fromkeys(temp_b))
    temp_c = list(dict.fromkeys(temp_c))
    temp = []
   

    temp.append({'id': post.id, 'name':post.name ,'client':post.survey_client.company_name,'industry' :post.survey_client.industry.industry,'area':post.survey_client.area.area,'start_date':post.start_date,'benchmarks':temp_b,'comps':temp_c})

    return jsonify(temp)



@users.route('/survey_filters', methods=['POST','GET'])
def survey_filter():
    tag = request.form['stat']
    tag = tag.split(",")



@users.route("/service_requests", methods=["POST","GET"])
def admin_service_requests():
    form = ServiceRequestForm() 
    searchform = RequestSearchForm()
    ind = Individual_request.query.filter_by(status="pending").all()
    corp= Corporate_request.query.filter_by(status="pending").all()

    return render_template("new_requests.html",form=form ,ind=ind, corp=corp, searchform=searchform)

@users.route("/service_requests/search", methods=["POST"])
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
    
    posts =  Survey.query.filter(Survey.status.in_(tag)).all()
    
    temp = []
    for post in posts:

        temp.append({'id': post.id})

    return jsonify(temp)

@users.route("/service_requests/searchrequest", methods=["POST"])
def search():
    # namesearch = SearchRequestForm()
    form = ServiceRequestForm()
    searchform = RequestSearchForm()
    search_term = request.form.get("keyword"," ")
    if request.method == 'POST':
        if (search_term != " "):
            ind =  Individual_request.query.filter(Individual_request.firstname.like('%' + search_term + '%')).all()
            corp =  Corporate_request.query.filter(Corporate_request.company_name.like('%' + search_term + '%')).all()
    return render_template("new_requests.html",form=form,ind=ind,searchform=searchform, corp=corp)

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


@users.route('/service_requests/update/<int:requestId>', methods=['POST'])
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

@users.route('/service_requests/corpupdate/<int:corprequestId>', methods=['POST'])
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
        messages = Contact.query.filter_by(status="Open")
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
    return jsonify(new_messages)


@users.route('/benchmark_details', methods=['POST','GET'])
def b_details():
    tag = request.form['id']
    post = Benchmark_job.query.get_or_404(tag)
    temp = []
    temp.append({'id': post.id,'status':post.status, 'job_title':post.job_title , 'grade':post.grade ,'reporting_relationship':post.reporting_relationship,'job_description' :post.job_description,'duties_and_responsibility':post.duties_and_responsibility,'financial_responsibilities':post.financial_responsibilities,'technical_qualification':post.technical_qualification,'minimum_years_of_experience':post.minimum_years_of_experience,'survey':post.comp_benchmark.id})
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
        query.salary_structure=formal_salary_structure_ovr
        query.salary_structure_adjustments=ss_adjusted
        query.avg_perc_review=avg_inc
        query.adjusment_basis=adj_basis
        query.inflation_indicator=inflation
        query.business_conditions_indicator=business_conditions
        query.salary_level_indicator=salary_levels
        query.other_indicator=other_indicators
        query.isGradesAdjustedBySamePerc=grade_ajs
        query.detailed_adjustments=how_adjs_made
        query.job_evaluation=job_eval_sys
        query.cost_of_living_adjustments_periodically=auto_inflation_adjs
        query.cost_of_living_adjustments_periodically_basis=auto_inflation_adjs_exp
        query.grade_levels=num_grade_levels
        query.perc_grade_difference=notch_diff
        query.grade_bases=sal_increments
        query.staff_progress=staff_progress
        query.experience_scale=experience
        query.previous_scale=previous_salary
        query.hiring_rate=hiring_rate
        query.max_salary_grade=max_salary
        query.max_salary_exceeded=sal_exceeded
        query.max_salary_exceeded_reason=sal_exceeded_exp
        query.haveIncentivePlans=annual_cash_bonus
        query.incentive_plans=annual_cash_bonus_exp
        query.annual_cash_eligibility=plans_eligibility
    
        db.session.commit()
        return('code submitted')
    
    else:
        qls = Qualitative_survey(client_name=client,status="In Progress",emp_number=num_emp,working_hours=num_work_hours,overtime_policy=ovr_policy,salary_structure=formal_salary_structure_ovr,salary_structure_adjustments=ss_adjusted,avg_perc_review=avg_inc,adjusment_basis=adj_basis,inflation_indicator=inflation,business_conditions_indicator=business_conditions,salary_level_indicator=salary_levels,other_indicator=other_indicators,isGradesAdjustedBySamePerc=grade_ajs,detailed_adjustments=how_adjs_made,job_evaluation=job_eval_sys,cost_of_living_adjustments_periodically=auto_inflation_adjs,cost_of_living_adjustments_periodically_basis=auto_inflation_adjs_exp,grade_levels=num_grade_levels,perc_grade_difference=notch_diff,grade_bases=sal_increments,staff_progress=staff_progress,experience_scale=experience,previous_scale=previous_salary,hiring_rate=hiring_rate,max_salary_grade=max_salary,max_salary_exceeded=sal_exceeded,max_salary_exceeded_reason=sal_exceeded_exp,haveIncentivePlans=annual_cash_bonus,incentive_plans=annual_cash_bonus_exp,annual_cash_eligibility=plans_eligibility,client_qual=main)
        db.session.add(qls)
        db.session.commit()
    
    

    return jsonify(salary_structure_adjustments)

    


@users.route("/administration/client_reports")
def client_reports():
    
    return render_template("client_hub_reports.html")


@users.route("/view_reports")
def view_reports():
    form = FilterReportForm()
    return render_template("reports.html", form=form)
 

@users.route('/view_reports/generate_report', methods=['POST'])
def generate_report():
    report_type = request.form['type']
    report_status = request.form['status']
    report_start_date = request.form['start_date']
    report_end_date = request.form['end_date']

    data = []

    if (report_type == 'clients'):
        data = []
        client_data = []

        num_clients = Client.query.count()
        num_active_clients = Client.query.filter_by(status='active').count()
        num_inactive_clients = Client.query.filter_by(status='Inactive').count()

        if (report_status == 'all'):
            clients = Client.query.all()
        else:
            clients = Client.query.filter_by(status=report_status)
        for client in clients:
            temp = {'name': client.company_name, 'company_type': client.company_type, 'area': client.area.area, 'industry': client.industry.industry, 'status': client.status}
            client_data.append(temp)
        
        data.append({'client_data': client_data, 'num_clients': num_clients, 'num_active_clients': num_active_clients, 'num_inactive_clients': num_inactive_clients})
    

    elif (report_type == 'service_requests'):
        num_indv_requests = Individual_request.query.count()
        num_indv_pending_requests = Individual_request.query.filter_by(status='pending').count()
        num_indv_awaiting_requests = Individual_request.query.filter_by(status='requesting_client_information').count()
        num_indv_first_pass_requests = Individual_request.query.filter_by(status='first_pass').count()
        num_indv_conflict_check_requests = Individual_request.query.filter_by(status='conflict_check').count()
        num_indv_finish_completion_requests = Individual_request.query.filter_by(status='finish_completion').count()
        num_indv_submitted_requests = Individual_request.query.filter_by(status='submitted').count()

        num_corp_requests = Corporate_request.query.count()
        num_corp_pending_requests = Corporate_request.query.filter_by(status='pending').count()
        num_corp_awaiting_requests = Corporate_request.query.filter_by(status='requesting_client_information').count()
        num_corp_first_pass_requests = Corporate_request.query.filter_by(status='first_pass').count()
        num_corp_conflict_check_requests = Corporate_request.query.filter_by(status='conflict_check').count()
        num_corp_finish_completion_requests = Corporate_request.query.filter_by(status='finish_completion').count()
        num_corp_submitted_requests = Corporate_request.query.filter_by(status='submitted').count()

        data = []
        indv_request_data = []
        corp_request_data = []

        if (report_status == 'all'):
            indv_requests = Individual_request.query.all()
            corp_requests = Corporate_request.query.all()
        else:
            indv_requests = Individual_request.query.filter_by(status=report_status)
            corp_requests = Corporate_request.query.filter_by(status=report_status)
        for i_request in indv_requests:
            temp = {'firstname': i_request.firstname, 'lastname': i_request.lastname, 'email': i_request.email, 'service': i_request.service, 'status': i_request.status}
            indv_request_data.append(temp)
        for c_request in corp_requests:
            temp = {'company_name': c_request.company_name, 'company_email': c_request.company_email, 'service': c_request.service, 'status': c_request.status}
            corp_request_data.append(temp)
        data.append({'indv_request_data': indv_request_data, 'corp_request_data': corp_request_data, 'num_indv_requests': num_indv_requests, 'num_corp_requests': num_corp_requests, 'num_indv_pend': num_indv_pending_requests,'num_indv_await': num_indv_awaiting_requests,'num_indv_fp': num_indv_first_pass_requests,'num_indv_cc': num_indv_conflict_check_requests,'num_indv_fc': num_indv_finish_completion_requests,'num_indv_sub': num_indv_submitted_requests,'num_corp_pend': num_corp_pending_requests,'num_corp_await': num_corp_awaiting_requests,'num_corp_fp': num_corp_first_pass_requests, 'num_corp_cc': num_corp_conflict_check_requests,'num_corp_fc': num_corp_finish_completion_requests, 'num_corp_sub': num_corp_submitted_requests})

    elif (report_type == 'messages'):
        data = []
        message_data = []

        num_messages = Contact.query.count()
        num_open_messages = Contact.query.filter_by(status='Open').count()
        num_closed_messages = Contact.query.filter_by(status='Closed').count()

        if (report_status == 'all'):
            messages = Contact.query.all()
        else:
            messages = Contact.query.filter_by(status=report_status)
        for message in messages:
            temp = {'firstname': message.firstname, 'lastname': message.lastname, 'company_name': message.company_name, 'email': message.email, 'job_title': message.job_title, 'status': message.status}
            message_data.append(temp)
        
        data.append({'message_data': message_data, 'num_messages': num_messages, 'num_open_messages': num_open_messages, 'num_closed_messages': num_closed_messages})
    
    return jsonify(data)
 
    


@users.route('/edit_survey', methods=['POST','GET'])
def edit_survey_list():
    tag = request.form['id']
    post = Survey.query.get_or_404(tag)
    comps = Survey_comparator.query.all()
    comp_list = []
    for i in comps:
        if(i.comparator.id == post.id):
                if (i.client.company_name +'_'+tag) not in comp_list :
                    x = i.client.company_name + '_' +tag
                 
                    comp_list.append(x)

    # temp = []
    # temp.append({'id': post.id,'status':post.status, 'job_title':post.job_title , 'grade':post.grade ,'reporting_relationship':post.reporting_relationship,'job_description' :post.job_description,'duties_and_responsibility':post.duties_and_responsibility,'financial_responsibilities':post.financial_responsibilities,'technical_qualification':post.technical_qualification,'minimum_years_of_experience':post.minimum_years_of_experience,'survey':post.comp_benchmark.id})
    return jsonify(comp_list)


@users.route('/delete_comp', methods=['POST','GET'])
def delete_comp():
    tag = request.form['id']
    sur_id = request.form['sur_id']
    comp = Survey_comparator.query.all()
    query_change = []
    for i in comp:
        if i.client.company_name == tag and i.comparator.id == sur_id:
            query_change.append([i.id])
    
    for c in query_change:
        col = Survey_comparator.query.filter_by(id=c).first()
        col.status = "Deleted"
        db.session.commit()

    # temp = []
    # temp.append({'id': post.id,'status':post.status, 'job_title':post.job_title , 'grade':post.grade ,'reporting_relationship':post.reporting_relationship,'job_description' :post.job_description,'duties_and_responsibility':post.duties_and_responsibility,'financial_responsibilities':post.financial_responsibilities,'technical_qualification':post.technical_qualification,'minimum_years_of_experience':post.minimum_years_of_experience,'survey':post.comp_benchmark.id})
    return jsonify(tag)