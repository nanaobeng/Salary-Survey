from survey import db, login_manager , app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Administrator(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(60),  nullable=False)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(120))
    password = db.Column(db.String(60),  nullable=False)
    client = db.relationship('Client', backref='user' , lazy=True)
    audit_log = db.relationship('Audit_log', backref='log' , lazy=True)
    benchmark = db.relationship('Main_benchmark_job', backref='user_account' , lazy=True)
    


    



    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return '<User %r>' % self.id


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), default = 'Inactive')

    
    company_name = db.Column(db.String(100), unique=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    financial_year_end = db.Column(db.String(50))
    company_type = db.Column(db.String(50))
    vat_number = db.Column(db.String(11))
    tel = db.Column(db.String(11))
    fax = db.Column(db.String(11))
    company_email = db.Column(db.String(100))
    website = db.Column(db.String(200))
    date_inc = db.Column(db.DateTime)
    country_inc = db.Column(db.String(70))
    contact_person_id = db.Column(db.Integer,  db.ForeignKey('contact_person.id'))
    postal_address_id = db.Column(db.Integer,  db.ForeignKey('postal_address.id'))
    street_address_id = db.Column(db.Integer,   db.ForeignKey('street_address.id'))
    user_id = db.Column(db.Integer,   db.ForeignKey('user.id'))
    company_history = db.Column(db.String(1000))
    client_type = db.Column(db.String(50))
    reg_number = db.Column(db.String(50))
    tax_id = db.Column(db.String(20))
    board_chairman_id = db.Column(db.Integer,  db.ForeignKey('board_chairman.id'))
    company_secretary_id = db.Column(db.Integer,  db.ForeignKey('company_secretary.id'))
    ceo_id = db.Column(db.Integer ,  db.ForeignKey('ceo.id') )
    key_management_id = db.Column(db.Integer  ,  db.ForeignKey('key_management.id'))
    current_auditor_id = db.Column(db.Integer ,  db.ForeignKey('current_auditor.id'))
    previous_auditor_id = db.Column(db.Integer ,  db.ForeignKey('previous_auditor.id'))
    survey = db.relationship('Survey', backref='survey_client' , lazy=True)
    comparator = db.relationship('Survey_comparator', backref='client' , lazy=True)
    
    

    # client_address = db.relationship('Address', backref='client_address' , lazy=True)
    # contact_person = db.relationship('Contact_person', backref='contact' , lazy=True)
    # governance = db.relationship('Client_governace', backref='governance' , lazy=True)
    # service_request = db.relationship('Service_request', backref='request' , lazy=True)
    # auditor = db.relationship('Auditor', backref='audit' , lazy=True)
    
    benchmark = db.relationship('Benchmark_job', backref='benchmark' , lazy=True)
    
    


    
    

    
    

    def __repr__(self):
        return '<Client %r>' % self.id

   


class Qualitative_survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), default = 'Inactive')
    emp_number = db.Column(db.Integer)
    working_hours = db.Column(db.Integer)
    overtime_policy = db.Column(db.String(1000))
    haveSalaryStructure = db.Column(db.Integer)
    salary_structure = db.Column(db.String(1000))
    salary_structure_adjustments = db.Column(db.String(300))
    salary_adjustment_date = db.Column(db.DateTime)
    avg_perc_review = db.Column(db.Integer)
    adjusment_basis = db.Column(db.String(1000))
    inflation_indicator = db.Column(db.Integer)
    business_conditions_indicator = db.Column(db.Integer)
    salary_level_indicator = db.Column(db.Integer)
    other_indicator = db.Column(db.String(1000))
    isGradesAdjustedBySamePerc = db.Column(db.Integer)
    detailed_adjustments = db.Column(db.String(1000))
    job_evaluation = db.Column(db.String(1000))
    periodic_salary_increases = db.Column(db.String(1000))
    cost_of_living_adjustments_periodically = db.Column(db.Integer)
    cost_of_living_adjustments_periodically_basis = db.Column(db.String(1000))
    grade_levels = db.Column(db.Integer)
    perc_grade_difference = db.Column(db.String(1000))
    grade_bases = db.Column(db.String(100))
    staff_progress = db.Column(db.String(100))
    education_scale = db.Column(db.Integer)
    experience_scale = db.Column(db.Integer)
    previous_scale = db.Column(db.Integer)
    other_scale = db.Column(db.String(1000))
    hiring_rate = db.Column(db.String(1000))
    max_salary_grade = db.Column(db.Integer)
    max_salary_exceeded = db.Column(db.Integer)
    max_salary_exceeded_reason = db.Column(db.String(1000))
    haveIncentivePlans = db.Column(db.Integer)
    incentive_plans = db.Column(db.String(1000))
    annual_cash_eligibility = db.Column(db.Integer)
    bonus_time = db.Column(db.String(100))
    is13th_paid = db.Column(db.Integer)
    bonus13_time = db.Column(db.String(100))
    restrictions_13 = db.Column(db.String(1000))
    direct_compensation = db.Column(db.String(1000))
    annual_leave_days = db.Column(db.Integer)
    staff_categories = db.Column(db.String(1000))
    paid_holidays = db.Column(db.Integer)
    sick_leave = db.Column(db.Integer)
    accident_leave = db.Column(db.Integer)
    maternity_leave = db.Column(db.Integer)
    paternity_leave = db.Column(db.Integer)
    compassionate_leave = db.Column(db.Integer)
    other_leave = db.Column(db.String(1000))
    entitlement_rates = db.Column(db.String(1000))
    redundancy_exercises = db.Column(db.String(1000))
    exiting_staff_payment = db.Column(db.String(1000))
    org_subsidise_transport = db.Column(db.Integer)
    org_subsidise_transport_yes = db.Column(db.String(1000))
    car_scheme = db.Column(db.Integer)
    car_scheme_yes = db.Column(db.String(200))
    car_market_val = db.Column(db.Integer)
    car_tax_issue = db.Column(db.String(1000))
    meals_senior_mgmt = db.Column(db.Integer)
    meals_senior_mgmt_yes = db.Column(db.String(1000))
    clothing_allowance = db.Column(db.String(100))
    grades_clothing_allowance = db.Column(db.String(200))
    travel_policy = db.Column(db.String(1000))
    loan_interest = db.Column(db.String(1000))
    housing_benefits = db.Column(db.String(1000))
    education_subsidy = db.Column(db.String(1000))
    provisions = db.Column(db.String(1000))
    entertainment_allowance = db.Column(db.String(1000))
    vacation_related_benefits = db.Column(db.Integer)
    entitlement_description = db.Column(db.String(1000))
    medical_scheme = db.Column(db.String(1000))
    family_scheme = db.Column(db.String(1000))
    medical_scheme_applied_overseas = db.Column(db.Integer)
    funeral_assistance = db.Column(db.Integer)
    family_benefits = db.Column(db.String(1000))
    fund_schemes = db.Column(db.String(1000))
    home_provisions = db.Column(db.String(1000))
    snr_mgmt_benefits = db.Column(db.Integer)
    additional_benefits = db.Column(db.String(1000))
    direct_reports = db.Column(db.Integer)
    direct_reports_yes = db.Column(db.String(1000))
    difficulty_recruiting_expertise = db.Column(db.Integer)
    difficulty_recruiting_expertise_yes = db.Column(db.String(1000))
    emp_turnover = db.Column(db.String(1000))
    seperate_salary_scale = db.Column(db.Integer)
    seperate_salary_scale_yes = db.Column(db.String(1000))
    
    
    def __repr__(self):
        return '<Qualitative_survey %r>' % self.id

class Audit_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self):
        return '<Audit_log %r>' % self.id


class Street_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_line1 = db.Column(db.String(100))
    street_line2 = db.Column(db.String(100) )
    city = db.Column(db.String(100))
    region = db.Column(db.String(50))
    country = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='street_address' , lazy=True)
   

    def __repr__(self):
        return '<Address %r>' % self.id

class Postal_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_line1 = db.Column(db.String(100))
    street_line2 = db.Column(db.String(100) )
    city = db.Column(db.String(100))
    region = db.Column(db.String(50))
    country = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='postal_address' , lazy=True)
   

    def __repr__(self):
        return '<Address %r>' % self.id

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(100))
    client = db.relationship('Client', backref='sector' , lazy=True)
    industry = db.relationship('Industry', backref='business_sector' , lazy=True)
    area = db.relationship('Area', backref='broad_sector' , lazy=True)

   

    def __repr__(self):
        return '<Sector %r>' % self.id





class Contact_person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime)
    nationality = db.Column(db.String(100))
    job = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='contact_person' , lazy=True)
    
   

    def __repr__(self):
        return '<Contact_person %r>' % self.id


class Sub_industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_industry = db.Column(db.String(100))
    industry = db.Column(db.Integer, db.ForeignKey('industry.id'))
    
    
   

    def __repr__(self):
        return '<Sub_industry %r>' % self.id

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(100))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    area = db.relationship('Area', backref='industry' , lazy=True)
    
    client = db.relationship('Client', backref='industry' , lazy=True)
    

    def __repr__(self):
        return '<Industry %r>' % self.id


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(100))
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'))
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'))
    Benchmark_jobs = db.relationship('Benchmark_job_pool', backref='area' , lazy=True)
    client = db.relationship('Client', backref='area' , lazy=True)

    def __repr__(self):
        return '<Area %r>' % self.id



class Key_management(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    nationality = db.Column(db.String(100))

    client = db.relationship('Client', backref='key_management' , lazy=True)


    def __repr__(self):
        return '<Key_management %r>' % self.id


class Ceo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
   
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    client = db.relationship('Client', backref='ceo' , lazy=True)




   

    def __repr__(self):
        return '<Ceo %r>' % self.id


class Board_chairman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    client = db.relationship('Client', backref='board_chairman' , lazy=True)




   

    def __repr__(self):
        return '<Board_chairman %r>' % self.id


class Service_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow )
    type_of_request = db.Column(db.String(100))
    status = db.Column(db.String(50))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))



    def __repr__(self):
        return '<Service_request %r>' % self.id


class Individual_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow )
    type_of_request = db.Column(db.String(100),default='individual')
    status = db.Column(db.String(50), default="pending")
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    #other = db.Column(db.String(100))
    
    email = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(400))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    service = db.Column(db.String(200))
    
    def __repr__(self):
        return '<Individual_request %r>' % self.id

class Corporate_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow )
    type_of_request = db.Column(db.String(100),default='corporate')
    status = db.Column(db.String(50),default='pending')
    company_name = db.Column(db.String(300))
    sector = db.Column(db.Integer)
    industry = db.Column(db.Integer)
    area = db.Column(db.Integer)
    financial_year_end = db.Column(db.String(100))
    company_type = db.Column(db.String(100))
    postal_address = db.Column(db.String(1000))
    street_address = db.Column(db.String(1000))
    reg_number = db.Column(db.String(100))
    vat_number = db.Column(db.String(100))
    tel = db.Column(db.String(100))
    company_email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    date_inc = db.Column(db.DateTime)
    country_inc = db.Column(db.String(100))
    chair_firstname = db.Column(db.String(100))
    chair_lastname = db.Column(db.String(100))
    chair_other = db.Column(db.String(100))
    chair_nation = db.Column(db.String(100))
    chair_email = db.Column(db.String(100))
    chair_phone = db.Column(db.String(100))
    ceo_firstname = db.Column(db.String(100))
    ceo_lastname = db.Column(db.String(100))
    ceo_other = db.Column(db.String(100))
    ceo_nation = db.Column(db.String(100))
    ceo_email = db.Column(db.String(100))
    ceo_phone = db.Column(db.String(100))
    other_board_firstname = db.Column(db.String(100))
    other_board_lastname = db.Column(db.String(100))
    other_board_other = db.Column(db.String(100))
    other_board_nation = db.Column(db.String(100))
    other_board_email = db.Column(db.String(100))
    other_board_phone = db.Column(db.String(100))
    key_firstname = db.Column(db.String(100))
    key_lastname = db.Column(db.String(100))
    key_other = db.Column(db.String(100))
    key_nation = db.Column(db.String(100))
    key_email = db.Column(db.String(100))
    key_phone = db.Column(db.String(100))
    prev_name = db.Column(db.String(100))
    prev_address = db.Column(db.String(1000))
    prev_city = db.Column(db.String(100))
    prev_country = db.Column(db.String(100))
    current_name = db.Column(db.String(100))
    current_address = db.Column(db.String(1000))
    current_city = db.Column(db.String(100))
    current_country = db.Column(db.String(100))
    sec_name = db.Column(db.String(100))
    sec_address = db.Column(db.String(1000))
    sec_city = db.Column(db.String(100))
    sec_country = db.Column(db.String(100))
    contact_firstname = db.Column(db.String(100))
    contact_lastname = db.Column(db.String(100))
    contact_other = db.Column(db.String(100))
    contact_nation = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_dob = db.Column(db.DateTime)
    contact_phone = db.Column(db.String(100))
    brief_history = db.Column(db.String(1000))
    service = db.Column(db.String(100))


    def __repr__(self):
        return '<Corporate_request %r>' % self.id

class Current_auditor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='current_auditor' , lazy=True)


    def __repr__(self):
        return '<Current_Auditor %r>' % self.id


class Company_secretary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='company_secretary' , lazy=True)


    def __repr__(self):
        return '<Current_Auditor %r>' % self.id

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    contact_id = db.Column(db.Integer,  db.ForeignKey('contact.id'))

    def __repr__(self):
        return '<Comment %r>' % self.id

class RequestComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500))
    service_id = db.Column(db.Integer,  db.ForeignKey('service_request.id'))

    def __repr__(self):
        return '<RequestComment %r>' % self.id




class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address_1 = db.Column(db.String(300))
    address_2 = db.Column(db.String(300))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    comment = db.relationship('Comment', backref='new_comment' , lazy=True)
    status = db.Column(db.String(10), default='Open')
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self):
        return '<Contact %r>' % self.id



class Previous_auditor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref='previous_auditor' , lazy=True)


    def __repr__(self):
        return '<Previous_uditor %r>' % self.id



class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    comparator = db.relationship('Survey_comparator', backref='comparator' , lazy=True)
    benchmark = db.relationship('Benchmark_job', backref='comp_benchmark' , lazy=True)




   

    def __repr__(self):
        return '<Survey %r>' % self.id


class Survey_comparator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    comparator_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    status = db.Column(db.String(100))



    def __repr__(self):
        return '<Survey_comparator %r>' % self.id


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    benchmark = db.relationship('Benchmark_job', backref='department' , lazy=True)
    main_benchmark = db.relationship('Main_benchmark_job', backref='main_department' , lazy=True)
    job = db.relationship('Comparator_job', backref='department' , lazy=True)
    bechmark_pool = db.relationship('Benchmark_job_pool', backref='department' , lazy=True)


    def __repr__(self):
        return '<Department %r>' % self.id

class Benchmark_job_pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'))
    reporting_relationship = db.Column(db.String(100))
    job_description = db.Column(db.String(1000))
    duties_and_responsibility = db.Column(db.String(1000))
    financial_responsibilities = db.Column(db.String(1000))
    technical_qualification = db.Column(db.String(1000))
    minimum_years_of_experience = db.Column(db.String(1000))
    status = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)
    

    def __repr__(self):
        return '<Benchmark_job_pool %r>' % self.id


class Main_benchmark_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    reporting_relationship = db.Column(db.String(100))
    job_description = db.Column(db.String(1000))
    duties_and_responsibility = db.Column(db.String(1000))
    financial_responsibilities = db.Column(db.String(1000))
    technical_qualification = db.Column(db.String(1000))
    minimum_years_of_experience = db.Column(db.String(1000))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)
    status = db.Column(db.String(50))
   
    comment = db.relationship('Main_benchmark_job_comment', backref='main_benchmark_comment' , lazy=True)
    allowance = db.relationship('Allowance', backref='main_benchmark_allowance' , lazy=True)
    benefit = db.relationship('Benefit', backref='main_benchmark_benefit' , lazy=True)
    incentive = db.relationship('Incentive', backref='main_benchmark_incentive' , lazy=True)
    base = db.relationship('Base_salary', backref='main_benchmark_base' , lazy=True)


    def __repr__(self):
        return '<Main_benchmark_job %r>' % self.id

    def as_dict(self):
        return {'job_title': self.job_title}

class Main_benchmark_job_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)
    
    def __repr__(self):
        return '<Main_benchmark_job_comment %r>' % self.id

class Benchmark_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    reporting_relationship = db.Column(db.String(100))
    job_description = db.Column(db.String(1000))
    duties_and_responsibility = db.Column(db.String(1000))
    financial_responsibilities = db.Column(db.String(1000))
    technical_qualification = db.Column(db.String(1000))
    minimum_years_of_experience = db.Column(db.String(1000))
    status = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    benefit_id = db.Column(db.Integer, db.ForeignKey('benefit.id'))
    incentive_id = db.Column(db.Integer, db.ForeignKey('incentive.id'))
    allowance_id = db.Column(db.Integer, db.ForeignKey('allowance.id'))
    base_salary_id = db.Column(db.Integer, db.ForeignKey('base_salary.id'))
    # comment = db.relationship('Comparator_job_comment', backref='comparator_job' , lazy=True)

    def __repr__(self):
        return '<Benchmark_job %r>' % self.id

class Comparator_job_comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    # comparator_job_id = db.Column(db.Integer, db.ForeignKey('Benchmark_job.id'))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)
    
    def __repr__(self):
        return '<Comparator_job_comment %r>' % self.id


class Allowance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_maintenance = db.Column(db.Float,default=0)
    housing = db.Column(db.Float,default=0)
    vehicle = db.Column(db.Float,default=0)
    transport = db.Column(db.Float,default=0)
    utilities = db.Column(db.Float,default=0)
    domestic_safety = db.Column(db.Float,default=0)
    fuel = db.Column(db.Float,default=0)
    entertainment = db.Column(db.Float,default=0)
    car = db.Column(db.Float,default=0)
    meal = db.Column(db.Float,default=0)
    education_support = db.Column(db.Float,default=0)
    vacation = db.Column(db.Float,default=0)
    uniform = db.Column(db.Float,default=0)
    mobile_money = db.Column(db.Float,default=0)
    telephone = db.Column(db.Float,default=0)
    miscellaenous = db.Column(db.Float,default=0)
    driver = db.Column(db.Float,default=0)
    rent = db.Column(db.Float,default=0)
  

    
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_allowance' , lazy=True)
    




   

    def __repr__(self):
        return '<Allowance %r>' % self.id

class Base_salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monthly_base_salary = db.Column(db.Float,default=0)
   
 
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_base' , lazy=True)
    




   

    def __repr__(self):
        return '<Base_salary %r>' % self.id



class Incentive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
  
    work_month = db.Column(db.Float,default=0)
    job_value_adjustment = db.Column(db.Float,default=0)
    company_performance = db.Column(db.Float,default=0)
    individual_performance = db.Column(db.Float,default=0)
    annual_incentive = db.Column(db.Float,default=0)
    stock_options = db.Column(db.Float,default=0)
    incentive = db.Column(db.Float,default=0)
    other_cash = db.Column(db.Float,default=0)
 
  


    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_incentive' , lazy=True)
    




   

    def __repr__(self):
        return '<Incentive %r>' % self.id



class Benefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_bus = db.Column(db.Float,default=0)
    company_car = db.Column(db.Float,default=0)
    club_membership = db.Column(db.Float,default=0)
    school_fees = db.Column(db.Float,default=0)
    health_insurance = db.Column(db.Float,default=0)
    medical_assistance = db.Column(db.Float,default=0)
    life_insurance = db.Column(db.Float,default=0)
    vacation = db.Column(db.Float,default=0)
    personal_travel = db.Column(db.Float,default=0)
    housing = db.Column(db.Float,default=0)
    telephone = db.Column(db.Float,default=0)
    driver = db.Column(db.Float,default=0)
    funeral_assistance = db.Column(db.Float,default=0)
    security = db.Column(db.Float,default=0)
    petrol = db.Column(db.Float,default=0)
    vehicle_maintenance = db.Column(db.Float,default=0)
    other_benefits = db.Column(db.Float,default=0)
    group_accident = db.Column(db.Float,default=0)
  
  

 
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_benefit' , lazy=True)
    




   

    def __repr__(self):
        return '<Benefit %r>' % self.id


class Comparator_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    grade = db.Column(db.String(50))
    reporting_relationship = db.Column(db.String(1000))
    job_match = db.Column(db.String(1000))
    comment = db.Column(db.String(1000))
 
  





   

    def __repr__(self):
        return '<Comparator_job %r>' % self.id


