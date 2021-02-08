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
    company_history = db.Column(db.Text)
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
   
    # client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

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
    other = db.Column(db.String(100))
    
    email = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(400))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    service = db.Column(db.String(200))
    
    def __init__(self, id,firstname, lastname,email,service,status):
        self.id = id
        self.firstname = firstname
        self.lastname=lastname
        self.email = email
        self.service=service
        self.status=status

    def __repr__(self):
     # return '<Individual_request %r>' % self.id
        return f"{self.email}:{self.id}"

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




   

    def __repr__(self):
        return '<Department %r>' % self.id



class Main_benchmark_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    reporting_relationship = db.Column(db.String(100))
    job_description = db.Column(db.Text)
    duties_and_responsibility = db.Column(db.Text)
    financial_responsibilities = db.Column(db.Text)
    technical_qualification = db.Column(db.Text)
    minimum_years_of_experience = db.Column(db.Text)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime , default=datetime.utcnow)
    status = db.Column(db.String(100))
   

    allowance = db.relationship('Allowance', backref='main_benchmark_allowance' , lazy=True)
    benefit = db.relationship('Benefit', backref='main_benchmark_benefit' , lazy=True)
    incentive = db.relationship('Incentive', backref='main_benchmark_incentive' , lazy=True)
    base = db.relationship('Base_salary', backref='main_benchmark_base' , lazy=True)

    




   

    def __repr__(self):
        return '<Main_benchmark_job %r>' % self.id

    def as_dict(self):
        return {'job_title': self.job_title}




class Benchmark_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    grade = db.Column(db.String(50))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    reporting_relationship = db.Column(db.String(100))
    job_description = db.Column(db.Text)
    duties_and_responsibility = db.Column(db.Text)
    financial_responsibilities = db.Column(db.Text)
    technical_qualification = db.Column(db.Text)
    minimum_years_of_experience = db.Column(db.Text)
    status = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

    benefit_id = db.Column(db.Integer, db.ForeignKey('benefit.id'))
    incentive_id = db.Column(db.Integer, db.ForeignKey('incentive.id'))
    allowance_id = db.Column(db.Integer, db.ForeignKey('allowance.id'))
    base_salary_id = db.Column(db.Integer, db.ForeignKey('base_salary.id'))


    

    
 




   

    def __repr__(self):
        return '<Benchmark_job %r>' % self.id

class Allowance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_maintenance = db.Column(db.Float)
    housing = db.Column(db.Float)
    vehicle = db.Column(db.Float)
    transport = db.Column(db.Float)
    utilities = db.Column(db.Float)
    domestic_safety = db.Column(db.Float)
    fuel = db.Column(db.Float)
    entertainment = db.Column(db.Float)
    car = db.Column(db.Float)
    meal = db.Column(db.Float)
    education_support = db.Column(db.Float)
    vacation = db.Column(db.Float)
    uniform = db.Column(db.Float)
    mobile_money = db.Column(db.Float)
    telephone = db.Column(db.Float)
    miscellaenous = db.Column(db.Float)
    driver = db.Column(db.Float)
    rent = db.Column(db.Float)
  

    
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_allowance' , lazy=True)
    




   

    def __repr__(self):
        return '<Allowance %r>' % self.id

class Base_salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monthly_base_salary = db.Column(db.Float)
   
 
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_base' , lazy=True)
    




   

    def __repr__(self):
        return '<Base_salary %r>' % self.id



class Incentive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
  
    work_month = db.Column(db.Float)
    job_value_adjustment = db.Column(db.Float)
    company_performance = db.Column(db.Float)
    individual_performance = db.Column(db.Float)
    annual_incentive = db.Column(db.Float)
    stock_options = db.Column(db.Float)
    incentive = db.Column(db.Float)
    other_cash = db.Column(db.Float)
 
  


    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_incentive' , lazy=True)
    




   

    def __repr__(self):
        return '<Incentive %r>' % self.id



class Benefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_bus = db.Column(db.Float)
    company_car = db.Column(db.Float)
    club_membership = db.Column(db.Float)
    school_fees = db.Column(db.Float)
    health_insurance = db.Column(db.Float)
    medical_assistance = db.Column(db.Float)
    life_insurance = db.Column(db.Float)
    vacation = db.Column(db.Float)
    personal_travel = db.Column(db.Float)
    housing = db.Column(db.Float)
    telephone = db.Column(db.Float)
    driver = db.Column(db.Float)
    funeral_assistance = db.Column(db.Float)
    security = db.Column(db.Float)
    petrol = db.Column(db.Float)
    vehicle_maintenance = db.Column(db.Float)
    other_benefits = db.Column(db.Float)
    group_accident = db.Column(db.Float)
  
  

 
    
    main_benchmark_job_id = db.Column(db.Integer, db.ForeignKey('main_benchmark_job.id'))
    comp_benchmark = db.relationship('Benchmark_job', backref='comp_benchmark_benefit' , lazy=True)
    




   

    def __repr__(self):
        return '<Benefit %r>' % self.id


class Comparator_job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    grade = db.Column(db.String(50))
    reporting_relationship = db.Column(db.Text)
    job_match = db.Column(db.Text)
    comment = db.Column(db.Text)
 
  





   

    def __repr__(self):
        return '<Comparator_job %r>' % self.id


