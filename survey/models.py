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



    