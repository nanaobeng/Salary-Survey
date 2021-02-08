from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,FloatField,IntegerField,RadioField,FileField,TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from survey.models import User
from wtforms_sqlalchemy.fields import QuerySelectField

from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, PasswordField, SubmitField, BooleanField, SelectField,FloatField,TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from survey.models import User,Sector,Industry,Area,Department

def survey_query():
    return Sector.query.order_by(Sector.sector.asc())

def industry_query():
    return Industry.query.all()

def area_query():
    return Area.query

def department_query():
    return Department.query



class ContactForm(FlaskForm):
   
    company_name = StringField('Company', validators=[DataRequired()])
    title =  SelectField(
        'Title',
        choices=[('dr', 'Dr.'), ('mr', 'Mr.'),('ms','Ms'),('mrs','Mrs.'),('miss','Miss'),('prof','Prof.')] , validators=[DataRequired()]
    )
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    email = StringField('Email Adress', validators=[DataRequired()])
    job_title = StringField('Job Title/Position', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    address_1 = StringField('*Address 1', validators=[DataRequired()])
    address_2 = StringField('Address 2', validators=[DataRequired()])
    city = StringField('City/Town', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')
    





class CorporateRequestForm(FlaskForm):
   
    company_name = StringField('Registered Company Name')
    sector = QuerySelectField(query_factory=survey_query,allow_blank=True,get_label='sector')
    industry = QuerySelectField(query_factory=industry_query,allow_blank=True,get_label='industry')
    area = QuerySelectField(query_factory=area_query,allow_blank=True,get_label='area')

   
    financial_year_end = StringField('Financial Year End')
    company_type =  SelectField(
        'Company Type',
        choices=[('parent', 'Parent'), ('subsidiary', 'Subsidiary'),('branch','Branch')] 
    )
    postal_address = StringField('Street Address')
    street_address = StringField('Street Address')
    reg_number = StringField('Company Registration Number')
    vat_number = StringField('VAT Number')
    tel = StringField('Telephone Number')
    fax = StringField('Fax Number')
    company_email = StringField('Company Email')
    website = StringField('Website Address')
    date_inc = DateField('Date of Incorporation')
    country_inc = StringField('Country of Incorporation')

    chair_firstname = StringField('Firstname')
    chair_lastname = StringField('Lastname')
    chair_other = StringField('Other Name')
    chair_nation = StringField('Nationality')
    chair_email = StringField('Email')
    chair_phone = StringField('Phone Number')


    ceo_firstname = StringField('Firstname')
    ceo_lastname = StringField('Lastname')
    ceo_other = StringField('Other Name')
    ceo_nation = StringField('Nationality')
    ceo_email = StringField('Email')
    ceo_phone = StringField('Phone Number')

    other_board_firstname = StringField('Firstname')
    other_board_lastname = StringField('Lastname')
    other_board_other = StringField('Other Name')
    other_board_nation = StringField('Nationality')
    other_board_email = StringField('Email')
    other_board_phone = StringField('Phone Number')

    key_firstname = StringField('Firstname')
    key_lastname = StringField('Lastname')
    key_other = StringField('Other Name')
    key_nation = StringField('Nationality')
    key_email = StringField('Email')
    key_phone = StringField('Phone Number')


    prev_name = StringField('Name')
    prev_address = StringField('Address')
    prev_city = StringField('City')
    prev_country = StringField('Country')
    
    current_name = StringField('Name')
    current_address = StringField('Address')
    current_city = StringField('City')
    current_country = StringField('Country')
    

    sec_name = StringField('Name')
    sec_address = StringField('Address')
    sec_city = StringField('City')
    sec_country = StringField('Country')


    contact_firstname = StringField('Firstname')
    contact_lastname = StringField('Lastname')
    contact_other = StringField('Other Name')
    contact_nation = StringField('Nationality')
    contact_email = StringField('Email')
    contact_dob = DateField('Date of Birth')
    contact_phone = StringField('Phone Number')

    brief_history = TextAreaField('Brief History')
    service =  SelectField(
        'Select Service',
        choices=[('survey', 'Salary Survey')] 
    )
   
    submit = SubmitField('Submit')

class IndividualRequestForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    other = StringField('Other Name', validators=[DataRequired()])

    email = StringField('Email', validators=[DataRequired()])
    dob = DateField('Date of Birth')
    phone = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])

    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    service =  SelectField(
        'Select Service',
        choices=[('industry_reports', 'Industry Reports'),('sub_industry_reports', 'Sub-Industry Reports'),('job_specific_reports', 'Job Specific Reports')] , validators=[DataRequired()]
    )
    submit = SubmitField('Submit')







class QualForm(FlaskForm):
    
    total_employee_num = IntegerField('A1. What is the total number of employees in the company? ')   
    work_hours = IntegerField('A2.How many working hours are there in a normal week?')   
    employee_num_cat = IntegerField('A3. Fill in the number of employees for each category')
    cat1 = FieldList('Type', validators=[DataRequired()])
    cat2 = FieldList('Full Time Employees', validators=[DataRequired()])
    cat3 = FieldList('Temporary Time Employees', validators=[DataRequired()])
    cat4 = FieldList('Other Employees', validators=[DataRequired()])
    cat5 = FieldList('Locally Recruited', validators=[DataRequired()])
    cat6 = FieldList('Expatriates', validators=[DataRequired()])
    cat7 = FieldList('Male', validators=[DataRequired()])
    cat8 = FieldList('Female', validators=[DataRequired()])
    cat9 = FieldList('Qualified for Overtime', validators=[DataRequired()])
    overtime = TextAreaField('A4. Describe your overtime policy(eligibility, payments, approvals etc):', validators=[DataRequired()])
                                                                                                                                                  
    market_pos = SelectField(u'B1. As an organisation, where (i.e. percentile terms) do you want to position yourself on the market?', choices=[('twentyfive', '25'), ('forty', '40'),('fifty', '50'),
    ('sixty', '60'),('eighty', '80'),('ninety', '90')], validators=[DataRequired()])
    sal_struct = RadioField(u' B2(a). Does your organisation have a formal salary structure for staff ?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    file_upload = FileField(u'B2(b). If Yes, please upload a copy of your current salary structure(s). Upload File', validators=[DataRequired()])
    salary_level = TextAreaField('B2(c). If No, how are salary level(s) established?', validators=[DataRequired()])
    sal_struct_adjust = SelectField(u'B3. How often is salary structure(s) adjusted?', choices = [('annually','Annually'),('quarterly','Quarterly'),('bi-monthly','Bi-monthly'),('monthly','Monthly'),('other','Other')],validators=[DataRequired()])
    specify_other = StringField('If other, please specify: ', validators=[DataRequired()])
    adjustment_date = DateField('B4. Date of last adjustment:', validators=[DataRequired()])
    percentage  = IntegerField('B5. Average percentage increase in last reviews', validators=[DataRequired()])
    basis = StringField('B6. Basis of adjustment:', validators=[DataRequired()])
    indicator = StringField('B7. Give the percentage adjustment for the following indicators: ', validators=[DataRequired()])
    col = IntegerField('Cost of living changes/inflation', validators=[DataRequired()])                                               
    bus_con = IntegerField('Business conditions', validators=[DataRequired()])
    salary_level = IntegerField('Salary levels of other organizations/market', validators=[DataRequired()])
    other = IntegerField('Other (please specify): ', validators=[DataRequired()]) 
    grades = RadioField(u'B8(a). Are all grades adjusted by the same percentage?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    how_adjust = StringField('B8(b). If No, how are adjustments made?', validators=[DataRequired()])
    review_date = StringField('B9(a). When are allowance offerings reviewed?', validators=[DataRequired()])
    effective_date = StringField('B9(b). What is the typical effective date once reviewed (i.e. back to January 1 of that year or the first date of the month in which they are reviewed)?', validators=[DataRequired()])
    eval_system = RadioField(u'B10(a). Does your organisation use a formal Job Evaluation System?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    eval_method =  TextAreaField('B10(b). If Yes, what method of job evaluation is used?', validators=[DataRequired()])
    periodic_sal = SelectField(u'B11. What types of periodic salary increases are granted?',
                choices = [('check1','Performance/Merit increases'),('check2','General increases (across board)'),('check3','Cost of living increases'),('check4','Other')], validators=[DataRequired()])
    auto_cost = RadioField(u'B12. Do your staff receive automatic cost of living salary adjustments at periodic intervals?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    yes_basis = TextAreaField('B12(b). If Yes, on what basis are increments computed and what are the normalintervals?', validators=[DataRequired()])
    grade_num = IntegerField('B13. How many grade levels do you have?', validators=[DataRequired()])
    perc_diff = StringField('B14. What is the percentage difference in salary between the notches within a grade?', validators=[DataRequired()])
    grade_basis = RadioField(u'B15. Salary increments in the same grade are based on: ',choices = [('notches','Notches'),('percentages','Percentages')], validators=[DataRequired()])
    staff_progress =  RadioField(u'B16. How do your staff progress through the steps? ',choices = [('performance/ Merits','Performance/ Merit'),('automatic annual salary increments','Automatic annual salary increments')], validators=[DataRequired()])
    first_priority = SelectField(u'1st Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')], validators=[DataRequired()])
    second_priority = SelectField(u'2nd Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')], validators=[DataRequired()])
    third_priority = SelectField(u'3rd Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')], validators=[DataRequired()])
    other_proirity = StringField('Other (please specify):')
    hiring_rate = RadioField(u' B18(a). Is there a hiring rate for each grade or job which differs from the minimum of the scale?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    explain = TextAreaField('B18(b). Please explain your above response: ', validators=[DataRequired()])
    max_salary = RadioField(u' B19(a). Is there a maximum salary for each grade which cannot be exceeded?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    explain_max = TextAreaField('B19(b). Please explain your above response: ', validators=[DataRequired()])
    instances = RadioField(u'  B20(a). Are there instances where the maximum salary for a grade has been exceeded?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    yes_explain = TextAreaField('B20(b). If Yes, please explain')
    
    incentive = RadioField(u'C1(a). Does the organisation provide an annual cash bonus or other short term incentive plan (excluding 13th month pay) for employees?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    plans = TextAreaField('C1(b). Please list and describe these plans (provide copy of the plan or policy)')
    staffC1 = RadioField(u'C2(a). Are all staff including executives eligible for C1?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    explain_no = TextAreaField('C2(b). If No, explain:')
    bonuses = RadioField(u'C3. When does your company pay the bonuses listed in 1b?',choices = [('option11','At the end of the year as a lump sum'),('option12','At completion of appraisal'),
    ('option13','onthly as part of the salary'),('option14','Other (please sepcify)')] )
    month13_bonus = RadioField(u'C4(a). Does your company pay 13th month bonus?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    bonus_time = nuses = RadioField(u'C4(b). When is the 13th month bonus paid?',choices = [('option11','At the end of the year as a lump sum'),('option12','At completion of appraisal'),
    ('option13','onthly as part of the salary'),('option14','Other (please sepcify)')])
    restrictions = TextAreaField('C5. List any restrictions on paying out the 13th month.', validators=[DataRequired()])
    compensations = TextAreaField('C6. Apart from the direct compensations above (sections B&C) (and excluding employee benefits,perquisites and in-kind allowances, which are reviewed in other sections of this questionnaire), what other forms of direct compensation are available to employees? (Please describe in detail)', validators=[DataRequired()])
    
    leavedays = IntegerField('D1. What is the number of leave days granted to staff annually?', validators=[DataRequired()])
    numincrease =  RadioField(u'D2. Does the number of leave days increase per employee tenure?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    staffcat = TextField('D3. Choose the staff categories and the number of leave days granted: ', validators=[DataRequired()])
    staffcatopt = StringField('Staff Category', validators=[DataRequired()])
    numleavedays = IntegerField('Number of Leave days', validators=[DataRequired()])
    paidholidaysnum = StringField('D4. What is the number of paid holidays granted to staff?', validators=[DataRequired()])
    sickness = IntegerField('Sickness', validators=[DataRequired()])
    accident = IntegerField('Accident', validators=[DataRequired()])
    maternity = IntegerField('Maternity', validators=[DataRequired()])
    paternity = IntegerField('Paternity', validators=[DataRequired()])
    emergency = IntegerField('Emergency/Compassionate', validators=[DataRequired()])
    othernum = IntegerField('Other (please specify')
    empgrade = StringField('Employee Grade', validators=[DataRequired()])
    options = StringField('Options', validators=[DataRequired()])
    rates = StringField('Rates', validators=[DataRequired()])
    explanation = StringField('Any Explanation', validators=[DataRequired()])
    gratuity = StringField('Gratuity', validators=[DataRequired()])
    longterm = StringField('Long term service awards', validators=[DataRequired()])
    severance = StringField('Severance awards/Redundancy', validators=[DataRequired()])
    endofservice = StringField('End of services benefits (indicate if different based on years of service)', validators=[DataRequired()])
    termination = StringField('Termination (including notice period', validators=[DataRequired()])
    resignation = StringField('Resignation (including notice period)', validators=[DataRequired()])
    othertype = StringField('Other (please specify)', validators=[DataRequired()])
    redexercise = DateField('D8. When was the last time you undertook redundancy exercises?', validators=[DataRequired()])
    staffcategory = SelectField(u'Staff Category', choices = [('cat1','Category 1'),('cat2','Category 2'),('cat3','Category 3')], validators=[DataRequired()])
    packagepaid = SelectField(u'Package Paid', choices=[('cat1','Category 1'),('cat1','Category 1'),('cat1','Category 1')], validators=[DataRequired()])
    trans = RadioField(u'D10(a). Does the organisation subsidise/provid transportation to and from work(includes vehicle type, fuel, personal driver)?',choices = [('yes','Yes'),('no','No')])
    fullymained = StringField('Fully maintained company car? (Indicate car type, engine capacity)', validators=[DataRequired()])
    carallawa = StringField('Car maintenance allowance per what period?', validators=[DataRequired()])
    fuelallawa = StringField('Fuel allowance per what period?', validators=[DataRequired()]) 
    transallawa = StringField('Transport allowance per what period?', validators=[DataRequired()])
    kilo = StringField('Kilometric', validators=[DataRequired()])
    driver = StringField('Company paid driver (Yes/No)', validators=[DataRequired()])
    otherallawa = StringField('Others (please specify)') 
    carscheme = RadioField(u'D11. Do you have a car scheme in which an employee uses a company car and after some years, the car is sold to the employee at a discounted rate?',choices = [('yes','Yes'),('no','No')])
    carschemeyes = IntegerField('D11(b). If Yes, after how many years of use is the car sold?', validators=[DataRequired()])
    mktpercentage = StringField('D11(c). At what percentage of market value is the car sold?', validators=[DataRequired()])
    tax = StringField('D11(d). Based on the scheme you have described, how do you deal with tax issues?', validators=[DataRequired()])
    carscheme = RadioField(u'D12(a). Does the organisation subsidise meal costs for senior management staff/executives (includes meal allowance as cash benefit and cafeteria service as kind benefit)?',choices = [('yes','Yes'),('no','No')])
    empgrade = StringField('Employee Grade', validators=[DataRequired()])
    cash = StringField('Cash amount/value', validators=[DataRequired()])
    period = StringField('Period (i.e. daily, weekly, etc)', validators=[DataRequired()])
    clothing = RadioField(u'D13. Does the organisation subsidise/provide clothing allowance for staff?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    clothingallawa = IntegerField('D13.(b) How much clothing allowance is given per year?', validators=[DataRequired()])
    grades = TextAreaField('D13(c). Which grades qualify for the clothing allowance?', validators=[DataRequired()])
    overseas = TextAreaField('Overseas rates (please specify separately if different for various grades):', validators=[DataRequired()])
    incountry = TextAreaField('Out of location allowance (in country):', validators=[DataRequired()]) 
    loans = RadioField(u'D15. Does the organisation provide interest free or low interest bearingloans (including salary advances) to employees for personal effects?',choices = [('yes','Yes'),('no','No')])
    employmentgrade = StringField('Employment Grade', validators=[DataRequired()])
    
    loan_type = StringField('Type of Loan', validators=[DataRequired()])
    ptg_interest = IntegerField('Percentage of Interest', validators=[DataRequired()])
    repay = StringField('Repayment Period', validators=[DataRequired()])
    limit = StringField('Limit of Facility', validators=[DataRequired()])
    housing_benefits = RadioField(u'D16. Does the organisation provide housing benefits to staff (includes house allowance as cash benefit and accommodation, furnishing, residence utilities, etc)?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    details_emp_grade = StringField('Employee Grade', validators=[DataRequired()])
    facility = StringField('Type of Facility', validators=[DataRequired()])
    amount = StringField('Cash Amount', validators=[DataRequired()])
    kind = StringField('If in kind (please indicate size of facility)', validators=[DataRequired()])
    items = TextAreaField('D16(c).List all household benefits provided, if any (e.g. Security, Cook, House-help, etc):', validators=[DataRequired()])
    educ = RadioField(u'D17. Do you provide education subsidy for staff and/or their dependents?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    entitlement = TextAreaField('Staff entitlements (cash/year)', validators=[DataRequired()])
    children = TextAreaField('Dependent/children (cash/year)', validators=[DataRequired()])
    courses = StringField('Short Courses', validators=[DataRequired()])
    prof_prog = StringField('Professional Programmes', validators=[DataRequired()])
    post_grad = StringField('Post Graduate', validators=[DataRequired()])
    other_edu = StringField('Other (please specify)', validators=[DataRequired()])
    entertainment = RadioField(u'D19. Do you provide entertainment allowance for staff?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    entdetails = TextAreaField('If Yes, please provide details.', validators=[DataRequired()])
    vacay = RadioField(u'D20. Are vacation related benefits offered to senior management staff?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    domestic_travel = StringField('Personal domestic travel?', validators=[DataRequired()])
    foreign_travel = StringField('Personal foreign travel including warm clothing and flight type?', validators=[DataRequired()])
    hotel=StringField('Hotel Accomodation?')
    comfac = StringField('Use of company owned facilities for vacation e.g. accommodation?', validators=[DataRequired()])
    telephone = StringField('Telephone (roaming facility)?', validators=[DataRequired()])
    other_facility = StringField('Other (please specify)', validators=[DataRequired()])
    med = TextAreaField('Employee: medical', validators=[DataRequired()])
    pres= TextAreaField('Employee: prescribed glasses', validators=[DataRequired()])
    emp_other = TextAreaField('Employee: other e.g. dentures', validators=[DataRequired()])
    spouse = TextAreaField('Spouse', validators=[DataRequired()])
    child = TextAreaField('Children (number and age limit)', validators=[DataRequired()])
    other_dep = TextAreaField('Others: ')
    cover_overseas = RadioField(u'D22.  Does the medical scheme cover overseas treatments?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    family_benefits = RadioField(u'D23. Do you have a funeral assistance/ death benefits arrangement for your staff and family members?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    emp_details= StringField('Employee', validators=[DataRequired()])
    spouse_details= StringField('Spouse', validators=[DataRequired()])
    children_details = StringField('Children', validators=[DataRequired()])
    parents = StringField('Parents', validators=[DataRequired()])
    otherbens= StringField('Other')
    prov_fund = StringField('Provident Fund', validators=[DataRequired()])
    schemes = StringField('Other Schemes (please specify)', validators=[DataRequired()])
    elec = StringField('Electricity', validators=[DataRequired()])
    water = StringField('Water', validators=[DataRequired()])
    telephone = StringField('Telephone and mobile phone', validators=[DataRequired()])
    other_facility = StringField('Other (please specify)', validators=[DataRequired()])
    senior = RadioField(u'D26. Are there any other benefits provided to senior management staff/executives not mentioned in this questionnaire?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    benefit_items = TextAreaField('D26(b). Please describe these benefit items using a separate sheet if needed. Probable benefit items not covered in this questionnaire may be: Managing Director on contract?', validators=[DataRequired()])
    indicate_benefits = TextField('If Yes, please indicate below, the positions: ', validators=[DataRequired()])
    expertise = RadioField(u'D28. Are there expertise/skills you find difficult to recruit from the Ghanaian labour market?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    expertise_list = TextAreaField('D28(b). If yes, please list them below:', validators=[DataRequired()])
    turnover = TextAreaField('D29. Please indicate frequent reasons for employee turnover.:', validators=[DataRequired()])
    scale = RadioField(u'D30. As an organisation, do you have a separate salary scale for local employees who have regional responsibilities within Africa?',choices = [('yes','Yes'),('no','No')], validators=[DataRequired()])
    reason= TextAreaField('D30(b). If Yes, please provide the reasons for a having a separate scale:', validators=[DataRequired()])





class RegistrationForm(FlaskForm):
    username = StringField('Username',
                                validators=[DataRequired(), Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])

    role =  SelectField(
        'Role',
        choices=[('admin', 'Admin'), ('client', 'Client')] , validators=[DataRequired()]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

    submit = SubmitField('Save')

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
   
    name = StringField('Sector', validators=[DataRequired()])
    update = SubmitField('Update')
    submit = SubmitField('Submit')

class IndustryForm(FlaskForm):
    
    name = StringField('Industry Name', validators=[DataRequired()])
    sector = QuerySelectField(query_factory=survey_query,allow_blank=True,get_label='sector')

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
    name = StringField('Area of Operation')
    sector = QuerySelectField(query_factory=survey_query,allow_blank=True,get_label='sector')
    industry = QuerySelectField(query_factory=industry_query,allow_blank=True,get_label='industry')
    submit = SubmitField('Submit')







# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                                 validators=[DataRequired(), Length(min=2,max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])

#     role =  SelectField(
#         'Role',
#         choices=[('admin', 'Admin'), ('client', 'Client'), ('associate', 'Associate'), ('manager', 'Manager'), ('director', 'Director')] , validators=[DataRequired()]
#     )
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

#     submit = SubmitField('Save')

#     def validate_username(self,username):
#         user = User.query.filter_by(username = username.data).first()
#         if user:
#             raise ValidationError('Username is already taken')
    
#     def validate_email(self,email):
#         user = User.query.filter_by(email= email.data).first()
#         if user:
#             raise ValidationError('Email is already in use')



# class LoginForm(FlaskForm):
   
#     email = StringField('Email', validators=[DataRequired(), Email()])

#     password = PasswordField('Password', validators=[DataRequired()])
    
#     remember = BooleanField('Remember Me')
#     submit = SubmitField('Login')



# class RequestResetForm(FlaskForm):
   
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')

#     def validate_email(self,email):
#         user = User.query.filter_by(email= email.data).first()
#         if user is None:
#             raise ValidationError('There is no account with this email')


# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])

#     submit = SubmitField('Reset Password')


# class SectorForm(FlaskForm):
   
#     name = StringField('Sector', validators=[DataRequired()])
#     update = SubmitField('Update')
#     submit = SubmitField('Submit')

# class IndustryForm(FlaskForm):
   
#     name = StringField('Industry Name', validators=[DataRequired()])
#     sector =  SelectField(
#         'Sector',
#         choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
#     )

#     submit = SubmitField('Submit')


# class JobForm(FlaskForm):
   
#     name = StringField('Job Title', validators=[DataRequired()])
#     sector =  SelectField(
#         'Sector',
#         choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
#     )
#     industry =  SelectField(
#         'Industry',
#         choices=[('banking', 'Banking'), ('mining', 'Mining')] , validators=[DataRequired()]
#     )
#     area =  SelectField(
#         'Area of Operation',
#         choices=[('public', 'Area 1'), ('private', 'Area 2')] , validators=[DataRequired()]
#     )
   

#     submit = SubmitField('Submit')

# class AreaForm(FlaskForm):
   
#     name = StringField('Area of Operation', validators=[DataRequired()])
#     sector =  SelectField(
#         'Sector',
#         choices=[('public', 'Public'), ('private', 'Private')] , validators=[DataRequired()]
#     )
#     industry =  SelectField(
#         'Industry',
#         choices=[('banking', 'Banking'), ('mining', 'Mining')] , validators=[DataRequired()]
#     )
    
   

#     submit = SubmitField('Submit')



class ClientForm(FlaskForm):
   
    name = StringField('Registered Company Name')
    reg = StringField('Company Registration Number')
    financial_year_end = StringField('Financial Year End')
    company_type = StringField('Company Type')
    vat = StringField('VAT Number')
    telephone = StringField('Telephone Number')
    fax = StringField('Fax Number')
    email = StringField('Email Address')
    website = StringField('Website Address')
    date_of_incorporation = DateField('Date of Incorporation')
    country_of_incorporation = StringField('Country of Incorporation')
    chairman_firstname = StringField(" Firstname")
    chairman_lastname = StringField(" Lastname")
    chairman_other_names = StringField(" Other Name")
    chairman_email = StringField(" Email Address")
    chairman_nationality = StringField(" Nationality")
    chairman_phone = StringField(" Phone ")
    key_firstname = StringField("Firstname")
    key_lastname = StringField("Lastname")
    key_other_names = StringField(" Other Name")
    key_email = StringField(" Email Address")
    key_nationality = StringField(" Nationality")
    key_phone = StringField(" Phone Number")
    ceo_firstname = StringField("Firstname")
    ceo_lastname = StringField("Lastname")
    ceo_other_names = StringField(" Other Name")
    ceo_email = StringField(" Email Address")
    ceo_nationality = StringField(" Nationality")
    ceo_phone = StringField(" Phone Number")

    current_auditor_name = StringField("Name")
    current_auditor_address = StringField("Address")
    current_auditor_city = StringField(" City")
    current_auditor_country = StringField(" Country")

    previous_auditor_name = StringField("Name")
    previous_auditor_address = StringField("Address")
    previous_auditor_city = StringField(" City")
    previous_auditor_country = StringField(" Country")


    company_secretary_name = StringField("Name")
    company_secretary_address = StringField("Address")
    company_secretary_city = StringField(" City")
    company_secretary_country = StringField(" Country")

    
    sector = QuerySelectField(query_factory=survey_query,allow_blank=True,get_label='sector')
    industry = QuerySelectField(query_factory=industry_query,allow_blank=True,get_label='industry')
    area = QuerySelectField(query_factory=area_query,allow_blank=True,get_label='area')

    mailing_building = StringField('Street Line 1')
    mailing_street = StringField('Street Line 2')
    mailing_city = StringField('City/Town')
    mailing_region = StringField('Region')
    mailing_country = StringField('Country')


    street_building = StringField('Building')
    street_street = StringField('Street')
    street_city = StringField('City/Town')
    street_country = StringField('Country')


    contact_firstname = StringField('Firstname')
    contact_middlename = StringField('Other Name')
    contact_lastname = StringField('Lastname')
    c_email = StringField('Email')
    c_phone = StringField('Phone')
    job = StringField('Job Title')
    contact_nationality = StringField('Nationality')
    contact_dob = DateField('Date of Birth')

    company_history = StringField('Company History')
     
    # job =  SelectField(
    #     'Job Title',
    #     choices=[('manager', 'Manager'), ('associate', 'Associate')] , validators=[DataRequired()]
    # )
    email = StringField('Email Address')
    phone = StringField('Phone')


   


    registration = StringField('Registration Number')

    tax_id = StringField('Tax ID')

#     submit = SubmitField('Submit')





class SurveyForm(FlaskForm):
    job_title = StringField('Job Title')
    grade = StringField('Grade')
    reporting_relationship = TextField('Reporting Relationship')
    job_desc = TextField('Job Description')
    key_duties = TextField('Key Duties and Scope of Responsibility')
    fin_res = StringField('Financial Responsibilities')
    tech_qual = TextField('Technical/Professional Qualification')
    exp_years = StringField('Minimum Years of Experience')

    
    department = QuerySelectField(query_factory=department_query,allow_blank=True,get_label='department')
   
    base_salary = FloatField('Annual Base Salary (GHS)')
    
    company_bonus_performance = FloatField('Company Performance Bonus')
    individual_bonus_performance = FloatField('Individual Performance Bonus')
    annual_bonus = FloatField('Annual Bonus')
    incentive_bonus = FloatField('Incentive Bonus')
    other_bonus = FloatField('Other bonus')


    staff_bus = FloatField('Staff Bus')
    company_car = FloatField('Company Car')
    personal_travel = FloatField('Personal Travel')
    petrol = FloatField('Petrol')
    vehicle = FloatField('Vehicle')
    driver = FloatField('Driver')

    health_insurance = FloatField('Health')
    medical_assistance = FloatField('Medical Assistance')
    funeral_assistance = FloatField('Funeral Assistance')
    life_insurance = FloatField('Life Insurance')
    group_accident = FloatField('Group Personnel Accident')


    club_membership = FloatField('Club Membership')
    school_fees = FloatField('School fees (Paid by employer)')
    vacation = FloatField('Vacation')
    housing = FloatField('Housing')
    telephone = FloatField('Telephone')
    security = FloatField('Security')
    other_benefits = FloatField('Other Benefits')

    
    vehicle_maintenance = FloatField('Vehicle Maintenance')
    allowance_vehicle = FloatField('Vehicle')
    transport = FloatField('Transport')
    fuel = FloatField('Fuel')
    car = FloatField('Car')
    allowance_driver = FloatField('Driver')
    

    domestic = FloatField('Domestic Safety and Security')
    allowance_housing = FloatField('Housing')
    utilities = FloatField('Utilities')
    meal = FloatField('Meal')
    allowance_telephone = FloatField('Telephone')


    entertainment = FloatField('Entertainment')
    education = FloatField('Education')
    vacation_allowance = FloatField('Vacation')
    uniform = FloatField('Uniform')
    mobile_money = FloatField('Mobile Money')
    misc = FloatField('Miscellaneous')
    

   
    
    


    



#     submit = SubmitField('Submit')
