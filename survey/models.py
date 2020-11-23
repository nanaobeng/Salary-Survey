from survey import db, login_manager , app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Administrator(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(60),  nullable=False)


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120),  nullable=False)
    password = db.Column(db.String(60),  nullable=False)


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
    registered_name = db.Column(db.String(100), unique=True, nullable=False)
    trading_name = db.Column(db.String(100), unique=True, nullable=False)
    sector_id = db.Column(db.Integer, db.ForeignKey('sector.id'), nullable=False)
    sub_industry_id = db.Column(db.Integer, db.ForeignKey('sub_industry.id'),  nullable=False)
    financial_year_end = db.Column(db.String(50),  nullable=False)
    company_type = db.Column(db.String(50),  nullable=False)
    vat_number = db.Column(db.String(11),  nullable=False)
    telephone = db.Column(db.String(10),  nullable=False)
    fax = db.Column(db.String(10),  nullable=False)
    email = db.Column(db.String(100),  nullable=False)
    website = db.Column(db.String(200),  nullable=False)
    date_of_inception = db.Column(db.DateTime,  nullable=False)
    country_of_inception = db.Column(db.String(70),  nullable=False)
    contact_person_id = db.Column(db.Integer,  db.ForeignKey('contact_person.id'), nullable=False)
    postal_address_id = db.Column(db.Integer,  db.ForeignKey('postal_address.id'), nullable=False)
    street_address_id = db.Column(db.Integer,   db.ForeignKey('street_address.id'),nullable=False)
    company_history = db.Column(db.Text,  nullable=False)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    client_type = db.Column(db.String(50),  nullable=False)
    registration_number = db.Column(db.String(50),  nullable=False)
    tax_id = db.Column(db.String(20),  nullable=False)
    board_chairman_id = db.Column(db.Integer,  db.ForeignKey('client_governace.id'))
    ceo_id = db.Column(db.Integer ,  db.ForeignKey('client_governace.id') )
    key_management_id = db.Column(db.Integer  ,  db.ForeignKey('client_governace.id'))
    current_auditor_id = db.Column(db.Integer ,  db.ForeignKey('auditor.id'))
    previous_auditor_id = db.Column(db.Integer ,  db.ForeignKey('auditor.id'))

    def __repr__(self):
        return '<Client %r>' % self.id


class Audit_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)

    def __repr__(self):
        return '<Audit_log %r>' % self.id


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_line1 = db.Column(db.String(100),nullable=False)
    street_line2 = db.Column(db.String(100) ,nullable=False)
    city = db.Column(db.String(100))
    region = db.Column(db.String(50))
    country = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
   

    def __repr__(self):
        return '<Address %r>' % self.id

class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String(100),nullable=False)

   

    def __repr__(self):
        return '<Sector %r>' % self.id


class Contact_person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.DateTime)
    nationality = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    
   

    def __repr__(self):
        return '<Contact_person %r>' % self.id


class Sub_industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_industry = db.Column(db.String(100),nullable=False)
    industry = db.Column(db.Integer, db.ForeignKey('industry.id'))
    
   

    def __repr__(self):
        return '<Sub_industry %r>' % self.id

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry = db.Column(db.String(100),nullable=False)

   

    def __repr__(self):
        return '<Industry %r>' % self.id



class Client_governace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    other_names = db.Column(db.String(100))
    email = db.Column(db.String(100))
    mobile_number = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    position = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))




   

    def __repr__(self):
        return '<Client_governance %r>' % self.id


class Service_request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    type_of_request = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))




   

    def __repr__(self):
        return '<Service_request %r>' % self.id


class Auditor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))




   

    def __repr__(self):
        return '<Auditor %r>' % self.id



class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))




   

    def __repr__(self):
        return '<Survey %r>' % self.id


class Survey_comparator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    comparator_id = db.Column(db.Integer, db.ForeignKey('comparator.id'))




   

    def __repr__(self):
        return '<Survey_comparator %r>' % self.id


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100))
    




   

    def __repr__(self):
        return '<Department %r>' % self.id

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
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    




   

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
  

    survey_comparator_id = db.Column(db.Integer, db.ForeignKey('survey_comparator.id'))
    benchmark_job_id = db.Column(db.Integer, db.ForeignKey('benchmark_job.id'))
    




   

    def __repr__(self):
        return '<Allowance %r>' % self.id


class Incentive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monthly_base_salary = db.Column(db.Float)
    work_month = db.Column(db.Float)
    job_value_adjustment = db.Column(db.Float)
    company_performance = db.Column(db.Float)
    individual_performance = db.Column(db.Float)
    annual_incentive = db.Column(db.Float)
    stock_options = db.Column(db.Float)
    incentive = db.Column(db.Float)
    other_cash = db.Column(db.Float)
 
  

    survey_comparator_id = db.Column(db.Integer, db.ForeignKey('survey_comparator.id'))
    benchmark_job_id = db.Column(db.Integer, db.ForeignKey('benchmark_job.id'))
    




   

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
    security = db.Column(db.Float)
    petrol = db.Column(db.Float)
    vehicle_maintenance = db.Column(db.Float)
    other_benefits = db.Column(db.Float)
  
  

    survey_comparator_id = db.Column(db.Integer, db.ForeignKey('survey_comparator.id'))
    benchmark_job_id = db.Column(db.Integer, db.ForeignKey('benchmark_job.id'))
    




   

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
 
  

    survey_comparator_id = db.Column(db.Integer, db.ForeignKey('survey_comparator.id'))
    benchmark_job_id = db.Column(db.Integer, db.ForeignKey('benchmark_job.id'))
    




   

    def __repr__(self):
        return '<Comparator_job %r>' % self.id
