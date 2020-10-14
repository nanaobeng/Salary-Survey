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
    name = db.Column(db.String(200), unique=True, nullable=False)
    sector = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120),  nullable=False)
    contact_person = db.Column(db.String(200),  nullable=False)
    street_address = db.Column(db.String(500),  nullable=False)
    mailing_address = db.Column(db.String(500),  nullable=False)
    registration_number = db.Column(db.String(120),  nullable=False)
    tax_id = db.Column(db.String(60),  nullable=False)



    def __repr__(self):
        return '<Client %r>' % self.id


class Sector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
 



    def __repr__(self):
        return '<Sector %r>' % self.id

class Industry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
 



    def __repr__(self):
        return '<Industry %r>' % self.id

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50), nullable=False)

 



    def __repr__(self):
        return '<Address %r>' % self.id

class Audit_Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity= db.Column(db.String(120), nullable=False)
    user = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
 



    def __repr__(self):
        return '<Audit_Log %r>' % self.id


class Contact_Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50),  nullable=False)
    middlename = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120),  nullable=False)
    job_title = db.Column(db.String(120),  nullable=False)
    email = db.Column(db.String(120),  nullable=False)
    mobile_number = db.Column(db.String(60),  nullable=False)


    def __repr__(self):
        return '<Contact_Person %r>' % self.id


class Comparator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    industry_id = db.Column(db.String(50),  nullable=False)
    sector_id = db.Column(db.String(120),  nullable=False)
    contact_person_id = db.Column(db.String(120),  nullable=False)
    street_address_id = db.Column(db.String(120),  nullable=False)
    mailing_address_id = db.Column(db.String(120),  nullable=False)



    def __repr__(self):
        return '<Comparator %r>' % self.id



class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.String(120), unique=True, nullable=False)
    start_date = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    
    end_date =db.Column(db.DateTime,nullable=False)
    status = db.Column(db.String(60),  nullable=False)



    def __repr__(self):
        return '<Survey %r>' % self.id


class Survey_Comparator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.String(50),  nullable=False)
    comparator_id = db.Column(db.String(120), nullable=False)
    



    def __repr__(self):
        return '<Survey_Comparator %r>' % self.id

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(2000),  nullable=False)
    



    def __repr__(self):
        return '<Questions %r>' % self.id


class Job_Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120) ,nullable=False)
    industry_id = db.Column(db.String(120), nullable=False)




    def __repr__(self):
        return '<Job Title %r>' % self.id


class Question_Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.String(120),  nullable=False)
    industry_id = db.Column(db.String(120),  nullable=False)
    question_id = db.Column(db.String(120),  nullable=False)
    answer = db.Column(db.String(120),  nullable=False)




    def __repr__(self):
        return '<Question Answer %r>' % self.id



class Base_Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120), unique=True, nullable=False)
    survey_id = db.Column(db.String(120), unique=True, nullable=False)
    comparator_id = db.Column(db.String(120), unique=True, nullable=False)
    annual_base_salary = db.Column(db.Float, nullable=False)




    def __repr__(self):
        return '<Base Salary %r>' % self.id


class Bonus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120),  nullable=False)
    survey_id = db.Column(db.String(120),  nullable=False)
    comparator_id = db.Column(db.String(120),  nullable=False)
    company_performance_bonus = db.Column(db.Float,  nullable=True)
    indiviudal_performance_bonus = db.Column(db.Float,  nullable=True)
    annual_bonus = db.Column(db.Float,  nullable=True)
    incentive_bonus = db.Column(db.Float,  nullable=True)
    other_bonus = db.Column(db.Float,  nullable=True)

    




    def __repr__(self):
        return '<Bonus %r>' % self.id


class Benefit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120),  nullable=False)
    survey_id = db.Column(db.String(120),  nullable=False)
    comparator_id = db.Column(db.String(120),  nullable=False)
    staff_bus = db.Column(db.Float,  nullable=True)
    company_car = db.Column(db.Float,  nullable=True)
    club_membership = db.Column(db.Float,  nullable=True)
    school_fees_paid_by_employer = db.Column(db.Float,  nullable=True)
    health_insurance = db.Column(db.Float,  nullable=True)
    medical_insurance = db.Column(db.Float,  nullable=True)
    funeral_insurance = db.Column(db.Float,  nullable=True)
    life_insurance = db.Column(db.Float,  nullable=True)
    group_personnel_accident = db.Column(db.Float,  nullable=True)
    vacation = db.Column(db.Float,  nullable=True)
    personal_travel = db.Column(db.Float,  nullable=True)
    housing = db.Column(db.Float,  nullable=True)
    telephone = db.Column(db.Float,  nullable=True)
    driver = db.Column(db.Float,  nullable=True)
    security = db.Column(db.Float,  nullable=True)
    petrol = db.Column(db.Float,  nullable=True)
    vehicle_maintenance = db.Column(db.Float,  nullable=True)
    other_benefits = db.Column(db.Float,  nullable=True)

    




    def __repr__(self):
        return '<Benefit %r>' % self.id



class Allowance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(120), nullable=False)
    survey_id = db.Column(db.String(120), nullable=False)
    comparator_id = db.Column(db.String(120), nullable=False)
    vehicle = db.Column(db.Float, nullable=True)
    transport = db.Column(db.Float, nullable=True)
    utilities = db.Column(db.Float, nullable=True)
    domestic_safety_and_security = db.Column(db.Float, nullable=True)
    entertainment = db.Column(db.Float, nullable=True)
    car = db.Column(db.Float, nullable=True)
    meal = db.Column(db.Float, nullable=True)
    education = db.Column(db.Float, nullable=True)
    vacation = db.Column(db.Float, nullable=True)
    uniform = db.Column(db.Float, nullable=True)
    housing = db.Column(db.Float, nullable=True)
    telephone = db.Column(db.Float, nullable=True)
    driver = db.Column(db.Float, nullable=True)
    mobile_money = db.Column(db.Float, nullable=True)
    fuel = db.Column(db.Float, nullable=True)
    vehicle_maintenance = db.Column(db.Float, nullable=True)
    miscellaenous = db.Column(db.Float, nullable=True)

    




    def __repr__(self):
        return '<Allowance %r>' % self.id
  