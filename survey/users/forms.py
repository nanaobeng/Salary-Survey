from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from survey.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                                validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    role =  SelectField(
        'Role',
        choices=[('admin', 'Admin'), ('client', 'Client'), ('comparator', 'Comparator')] , validators=[DataRequired()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username is already taken')
    
    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Email is already in use')



class LoginForm(FlaskForm):
   
    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class RequestResetForm(FlaskForm):
   
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Reset Password')


class SectorForm(FlaskForm):
   
    name = StringField('Name', validators=[DataRequired()])

    submit = SubmitField('Submit')

class IndustryForm(FlaskForm):
   
    name = StringField('Industry Name', validators=[DataRequired()])
    sector =  SelectField(
        'Sector',
        choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
    )

    submit = SubmitField('Submit')


class JobForm(FlaskForm):
   
    name = StringField('Job Title', validators=[DataRequired()])
    sector =  SelectField(
        'Sector',
        choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
    )
    industry =  SelectField(
        'Industry',
        choices=[('banking', 'Banking'), ('mining', 'Mining')] , validators=[DataRequired()]
    )
    area =  SelectField(
        'Area of Operation',
        choices=[('public', 'Area 1'), ('private', 'Area 2')] , validators=[DataRequired()]
    )
   

    submit = SubmitField('Submit')

class AreaForm(FlaskForm):
   
    name = StringField('Title', validators=[DataRequired()])
    sector =  SelectField(
        'Sector',
        choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
    )
    industry =  SelectField(
        'Industry',
        choices=[('banking', 'Banking'), ('mining', 'Mining')] , validators=[DataRequired()]
    )
    
   

    submit = SubmitField('Submit')



class ClientForm(FlaskForm):
   
    name = StringField('Client Name', validators=[DataRequired()])
    sector =  SelectField(
        'Sector',
        choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
    )
    industry =  SelectField(
        'Industry',
        choices=[('banking', 'Banking'), ('mining', 'Mining')] , validators=[DataRequired()]
    )
    area =  SelectField(
        'Area of Operation',
        choices=[('public', 'Area 1'), ('private', 'Area 2')] , validators=[DataRequired()]
    )
    mailing_building = StringField('Building', validators=[DataRequired()])
    mailing_street = StringField('Street', validators=[DataRequired()])
    mailing_city = StringField('City', validators=[DataRequired()])
    mailing_country = StringField('Country', validators=[DataRequired()])


    street_building = StringField('Building', validators=[DataRequired()])
    street_street = StringField('Street', validators=[DataRequired()])
    street_city = StringField('City', validators=[DataRequired()])
    street_country = StringField('Country', validators=[DataRequired()])


    contact_firstname = StringField('Firstname', validators=[DataRequired()])
    contact_middlename = StringField('Middlename', validators=[DataRequired()])
    contact_lastname = StringField('Lastname', validators=[DataRequired()])
     
    job =  SelectField(
        'Job Title',
        choices=[('manager', 'Manager'), ('associate', 'Associate')] , validators=[DataRequired()]
    )
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])


   


    registration = StringField('Registration Number', validators=[DataRequired()])

    tax_id = StringField('Tax ID', validators=[DataRequired()])

    submit = SubmitField('Submit')





class SurveyForm(FlaskForm):
   
    base_salary = FloatField('Annual Base Salary', validators=[DataRequired()])
    
    company_bonus_performance = FloatField('Company Performance Bonus', validators=[DataRequired()])
    individual_bonus_performance = FloatField('Individual Performance Bonus', validators=[DataRequired()])
    annual_bonus = FloatField('Annual Bonus', validators=[DataRequired()])
    incentive_bonus = FloatField('Incentive Bonus', validators=[DataRequired()])
    other_bonus = FloatField('Other bonus', validators=[DataRequired()])


    staff_bus = FloatField('Staff Bus', validators=[DataRequired()])
    company_car = FloatField('Company Car', validators=[DataRequired()])
    personal_travel = FloatField('Personal Travel', validators=[DataRequired()])
    petrol = FloatField('Petrol', validators=[DataRequired()])
    vehicle = FloatField('Vehicle', validators=[DataRequired()])
    driver = FloatField('Driver', validators=[DataRequired()])

    health_insurance = FloatField('Health', validators=[DataRequired()])
    medical_assistance = FloatField('Medical Assistance', validators=[DataRequired()])
    funeral_assistance = FloatField('Funeral Assistance', validators=[DataRequired()])
    life_insurance = FloatField('Life Insurance', validators=[DataRequired()])
    group_accident = FloatField('Group Personnel Accident', validators=[DataRequired()])


    club_membership = FloatField('Club Membership', validators=[DataRequired()])
    school_fees = FloatField('School fees (Paid by employer)', validators=[DataRequired()])
    vacation = FloatField('Vacation', validators=[DataRequired()])
    housing = FloatField('Housing', validators=[DataRequired()])
    telephone = FloatField('Telephone', validators=[DataRequired()])
    security = FloatField('Security', validators=[DataRequired()])
    other_benefits = FloatField('Other Benefits', validators=[DataRequired()])

    
    vehicle_maintenance = FloatField('Vehicle Maintenance', validators=[DataRequired()])
    allowance_vehicle = FloatField('Vehicle', validators=[DataRequired()])
    transport = FloatField('Transport', validators=[DataRequired()])
    fuel = FloatField('Fuel', validators=[DataRequired()])
    car = FloatField('Car', validators=[DataRequired()])
    allowance_driver = FloatField('Driver', validators=[DataRequired()])
    

    domestic = FloatField('Domestic Safety and Security', validators=[DataRequired()])
    allowance_housing = FloatField('Housing', validators=[DataRequired()])
    utilities = FloatField('Utilities', validators=[DataRequired()])
    meal = FloatField('Meal', validators=[DataRequired()])
    allowance_telephone = FloatField('Telephone', validators=[DataRequired()])


    entertainment = FloatField('Entertainment', validators=[DataRequired()])
    education = FloatField('Education', validators=[DataRequired()])
    vacation = FloatField('Vacation', validators=[DataRequired()])
    uniform = FloatField('Uniform', validators=[DataRequired()])
    mobile_money = FloatField('Mobile Money', validators=[DataRequired()])
    misc = FloatField('Miscellaneous', validators=[DataRequired()])
    

   
    
    


    



    submit = SubmitField('Submit')