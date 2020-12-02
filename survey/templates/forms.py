from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, PasswordField, SubmitField, BooleanField, SelectField,FloatField,TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from survey.models import User


class QualForm(FlaskForm):
    name = StringField('Name')
    title = StringField('Title')
    address = StringField('Address')
    phone = IntegerField('Phone')
    email =StringField('Email')
    date = StringField('Date Completed')
    totalemployeenum = IntegerField('1. Total number of employees: ')
    employeenumcat = IntegerField('2. Fill in the number of employees for each category')
    cat1 = FieldList('Type')
    cat2 = FieldList('Full Time Employees')
    cat3 = FieldList('Temporary Time Employees')
    cat4 = FieldList('Other Employees')
    cat5 = FieldList('Locally Recruited')
    input1 = StringField(' ')
    input2 = StringField(' ')
    input3 = StringField(' ')
    cat6 = FieldList('Expatriates')
    input4 = StringField(' ')
    input5 = StringField(' ')
    input6 = StringField(' ')
    cat7 = FieldList('Male')
    input7 = StringField(' ')
    input8 = StringField(' ')
    input9 = StringField(' ')
    cat8 = FieldList('Female')
    input9 = StringField(' ')
    input10 = StringField(' ')
    input11 = StringField(' ')
    cat9 = FieldList('Qualified for Overtime')
    input12 = StringField(' ')
    input13 = StringField(' ')
    input14 = StringField(' ')
    workhours =IntegerField('3. Number of working hours in a week:')
    overtime = TextAreaField('4. Describe your overtime policy. This includes information on eligibility, payments and approvals: ')
    marketpos = SelectField(u'1. As an organisation, where (i.e. percentile terms) do you want to positionyourself on the market?', choices=[('twentyfive', '25'), ('forty', '40'),('fifty', '50'),
    ('sixty', '60'),('eighty', '80'),('ninety', '90')])
    salstruct = RadioField(u' 2a. Does your organisation have a formal salary structure for staff ?', choices=[('yes', 'Yes'), ('no', 'No')])
    fileupload = FileField(u'2b. If Yes, please upload a copy of your current salary structure(s). Upload File', [validators.regexp(u'^[^/\\]\.pdf$')])
    salarylevel = TextAreaField('2c. If No, how are salary level(s) established?')
    salstructadjust = SelectField(u'3. How often is salary structure(s) adjusted?', choices = [('annually','Annually'),('quarterly','Quarterly'),('bi-monthly','Bi-monthly'),('monthly','Monthly'),('other','Other')])
    specifyother = StringField('If other, please specify: ')
    adjdate = DateField('4. Date of last adjustment:')
    percentage  = IntegerField('5. Average percentage increase in last reviews')
    basis = StringField('6. Basis of adjustment:')
    indicator = StringField('7. Give the percentage adjustment for the following indicators: ')
    Indicator
    Percentage 
    col = IntegerField('Cost of living changes/inflation')                                               
    buscon = IntegerField('Business conditions')
    sallevel = IntegerField('Salary levels of other organizations/market')
    other = IntegerField('Other (please specify): ') 
    grades = RadioField(u'8a. Are all grades adjusted by the same percentage?',choices = [('yes','Yes'),('no','No')])
    howadjust = StringField('8b. If No, how are adjustments made?')
    evalsys = RadioField(u'9a. Does your organisation use a formal Job Evaluation System?',choices = [('yes','Yes'),('no','No')])
    altyes =  TextAreaField('9b. If Yes, what method of job evaluation is used?')
    periodicsal = SelectField(u'10. What types of periodic salary increases are granted?',
                choices = [('check1','Performance/Merit increases'),('check2','General increases (across board)'),('check3','Cost of living increases'),('check4','Other')])
    autocost = RadioField(u'11a. Do your staff receive automatic cost of living salary adjustments at periodic intervals?',choices = [('yes','Yes'),('no','No')])
    yesbasis = TextAreaField('11b. If Yes, on what basis are increments computed and what are the normalintervals?')
    gradenum = IntegerField('12. How many grade levels do you have?')
    percdiff = StringField('13. What is the percentage difference in salary between the notches within a grade?')
    gradebasis = RadioField(u'14. Salary increments in the same grade are based on: ',choices = [('notches','Notches'),('percentages','Percentages')])
    staffprogress =  RadioField(u'15. How do your staff progress through the steps? ',choices = [('performance/ Merits','Performance/ Merit'),('automatic annual salary increments','Automatic annual salary increments')])
    order = TextField('16. In order of importance, what factors are considered in placing your new staff on your salary scale (please rank as 1st, 2nd, 3rd, etc)?')
    firstprior = SelectField(u'1st Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')])
    secprior = SelectField(u'2nd Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')])
    thirdprior = SelectField(u'3rd Priority: ', choices = [('education','Education'),('experience','Experience'),('prev-salary','Previous Salary')])
    otherproir = StringField('Other (please specify):')
    hiringrate = RadioField(u' 17a. Is there a hiring rate for each grade or job which differs from the minimum of the scale?',choices = [('yes','Yes'),('no','No')])
    explain = TextAreaField('17b. Please explain your above response: ')
    minsal = RadioField(u' 18. Is there a maximum salary for each grade which cannot be exceeded?',choices = [('yes','Yes'),('no','No')])
    instances = RadioField(u'  19. Are there instances where the maximum salary for a grade has been exceeded?',choices = [('yes','Yes'),('no','No')])
    yesexplain = TextAreaField('19b. If Yes, please explain')
    incentive = RadioField(u'1a. Does the organisation provide an annual cash bonus or other short term incentive plan (excluding 13th month pay) for employees?',choices = [('yes','Yes'),('no','No')])
    plans = TextAreaField('1b. Please list and describe these plans (provide copy of the plan or policy)')
    staffC1 = RadioField(u'2. Are all staff including executives eligible for C1?',choices = [('yes','Yes'),('no','No')])
    explainno = TextAreaField('2b. If No, explain:')
    bonuses = RadioField(u'3. When does your company pay the bonuses listed in 1b?',choices = [('option11','At the end of the year as a lump sum'),('option12','At completion of appraisal'),('option13','onthly as part of the salary'),('option14','Other (please sepcify)'))])
    month13bonus = RadioField(u'4. Does your company pay 13th month bonus?',choices = [('yes','Yes'),('no','No')])
    bonustime = nuses = RadioField(u'5. When is the 13th month bonus paid?',choices = [('option11','At the end of the year as a lump sum'),('option12','At completion of appraisal'),('option13','onthly as part of the salary'),('option14','Other (please sepcify)'))])
    restrictions = TextAreaField('6. List any restrictions on paying out the 13th month.')
    compensations = TextAreaField('7. Apart from the direct compensations above (sections B&C) (and excluding employee benefits,perquisites and in-kind allowances, which are reviewed in other sections of this questionnaire), what other forms of direct compensation are available to employees? (Please describe in detail)')
    leavedays = IntegerField('1. What is the number of leave days granted to staff annually?')
    numincrease =  RadioField(u'D2. Does the number of leave days increase per employee tenure?',choices = [('yes','Yes'),('no','No')])
    staffcat = TextField('D3. Add staff categories and the number of leave days granted: ')
    staffcatopt = StringField('Staff Category')
    numleavedays = IntegerField('Number of Leave days')
    paidholidaysnum = StringField('D4. What is the number of paid holidays granted to staff?')
    sickness = IntegerField('Sickness')
    accident = IntegerField('Accident')
    maternity = IntegerField('Maternity')
    paternity = IntegerField('Paternity')
    emergency = IntegerField('Emergency/Compassionate')
    othernum = IntegerField('Other (please specify')
    empgrade = StringField('Employee Grade')
    options = StringField('Options')
    rates = StringField('Rates')
    explanation = StringField('Any Explanation')
    gratuity = StringField('Gratuity')
    longterm = StringField('Long term service awards')
    severance = StringField('Severance awards/Redundancy')
    endofservice = StringField('End of services benefits (indicate if different based on years of service)')
    termination = StringField('Termination (including notice period')
    resignation = StringField('Resignation (including notice period)')
    othertype = StringField('Other (please specify)')
    redexercise = DateField('D8. When was the last time you undertook redundancy exercises?')
    staffcategory = SelectField(u'Staff Category', choices = [('cat1','Category 1'),('cat2','Category 2'),('cat3','Category 3')])
    packagepaid = SelectField(u'Package Paid', choices[('cat1','Category 1'),('cat1','Category 1'),('cat1','Category 1')])
    trans = RadioField(u'D10. Does the organisation subsidise/provid transportation to and from work(includes vehicle type, fuel, personal driver)?',choices = [('yes','Yes'),('no','No')])
    fullymained = StringField('Fully maintained company car? (Indicate car type, engine capacity)')
    carallawa = StringField('Car maintenance allowance per what period?')
    fuelallawa = StringField('Fuel allowance per what period?') 
    transallawa = StringField('Transport allowance per what period?')
    kilo = StringField('Kilometric')
    driver = StringField('Company paid driver (Yes/No)')
    otherallawa = StringField('Others (please specify)') 
    carscheme = RadioField(u'D11. Do you have a car scheme in which an employee uses a company car and after some years, the car is sold to the employee at a discounted rate?',choices = [('yes','Yes'),('no','No')])
    carschemeyes = IntegerField('D11(b). If Yes, after how many years of use is the car sold?')
    mktpercentage = StringField('D11(c). At what percentage of market value is the car sold?')
    tax = StringField('D11(d). Based on the scheme you have described, how do you deal with tax issues?')
    carscheme = RadioField(u'D12. Does the organisation subsidise meal costs for senior management staff/executives (includes meal allowance as cash benefit and cafeteria service as kind benefit)?',choices = [('yes','Yes'),('no','No')])
    empgrade = StringField('Employee Grade')
    cash = StringField('Cash amount/value')
    period = StringField('Period (i.e. daily, weekly, etc)')
    clothing = RadioField(u'D13. Does the organisation subsidise/provide clothing allowance for staff?',choices = [('yes','Yes'),('no','No')])
    clothingallawa = IntegerField('D13.(b) How much clothing allowance is given per year?')
    grades = TextAreaField('D13(c). Which grades qualify for the clothing allowance?')
    overseas = TextAreaField('Overseas rates (please specify separately if different for various grades):')
    incountry = TextAreaField('Out of location allowance (in country):') 
    loans = RadioField(u'D15. Does the organisation provide interest free or low interest bearingloans (including salary advances) to employees for personal effects?',choices = [('yes','Yes'),('no','No')])
    employmentgrade = StringField('Employment Grade')
    loantype = StringField('Type of Loan')
    ptginterest = IntegerField('Percentage of Interest')
    repay = StringField('Repayment Period')
    limit = StringField('Limit of Facility')
    housingbenefits = RadioField(u'D16. Does the organisation provide housing benefits to staff (includes house allowance as cash benefit and accommodation, furnishing, residence utilities, etc)?',choices = [('yes','Yes'),('no','No')])
    detailsempgrade = StringField('Employee Grade')
    facility = StringField('Type of Facility')
    amount = StringField('Cash Amount')
    kind = StringField('If in kind (please indicate size of facility)')
    items = TextAreaField('D16(c).List all household benefits provided, if any (e.g. Security, Cook, House-help, etc):')
    educ = RadioField(u'D17. Do you provide education subsidy for staff and/or their dependents?',choices = [('yes','Yes'),('no','No')])
    entitlement = TextAreaField('Staff entitlements (cash/year)')
    children = TextAreaField('Dependent/children (cash/year)')
    courses = StringField('Short Courses')
    profprog = StringField('Professional Programmes')
    postgrad = StringField('Post Graduate')
    otheredu = StringField('Other (please specify)')
    entertainment = RadioField(u'D19. Do you provide entertainment allowance for staff?',choices = [('yes','Yes'),('no','No')])
    entdetails = TextAreaField('If Yes, please provide details.')
    vacay = RadioField(u'D20. Are vacation related benefits offered to senior management staff?',choices = [('yes','Yes'),('no','No')])
    dometravel = StringField('Personal domestic travel?')
    foreigntravel = StringField('Personal foreign travel including warm clothing and flight type?')
    hotel=StringField('Hotel Accomodation?')
    comfac = StringField('Use of company owned facilities for vacation e.g. accommodation?')
    telephone = StringField('Telephone (roaming facility)?')
    otherfac = StringField('Other (please specify)')
    med = TextAreaField('Employee: medical')
    pres= TextAreaField('Employee: prescribed glasses')
    empother = TextAreaField('Employee: other e.g. dentures')
    spouse = TextAreaField('Spouse')
    child = TextAreaField('Children (number and age limit)')
    otherdep = TextAreaField('Others: ')
    coveroverseas = RadioField(u'D22.  Does the medical scheme cover overseas treatments?',choices = [('yes','Yes'),('no','No')])
    fambenefits = RadioField(u'D23. Do you have a funeral assistance/ death benefits arrangement for your staff and family members?',choices = [('yes','Yes'),('no','No')])
    benempedetails= StringField('Employee')
    spousedetails= StringField('Spouse')
    childetails = StringField('Children')
    parents = StringField('Parents')
    otherbens= StringField('Other')
    provfund = StringField('Provident Fund')
    schemes = StringField('Other Schemes (please specify)')
    elec = StringField('Electricity')
    water = StringField('Water')
    telephone = StringField('Telephone and mobile phone')
    otherfacility = StringField('Other (please specify)')
    senior = RadioField(u'D26. Are there any other benefits provided to senior management staff/executives not mentioned in this questionnaire?',choices = [('yes','Yes'),('no','No')])
    benefititems = TextAreaField('D26(b). Please describe these benefit items using a separate sheet if needed. Probable benefit items not covered in this questionnaire may be: Managing Director on contract?')
    indicatebenefits = TextField('If Yes, please indicate below, the positions: ')
    expertise = RadioField(u'D28. Are there expertise/skills you find difficult to recruit from the Ghanaian labour market?',choices = [('yes','Yes'),('no','No')])
    expertiselist = TextAreaField('D28(b). If Yes, please list them below:')
    turnover = TextAreaField('D29. Please indicate frequent reasons for employee turnover.:')
    scale = RadioField(u'D30. As an organisation, do you have a separate salary scale for local employees who have regional responsibilities within Africa?',choices = [('yes','Yes'),('no','No')])
    reason= TextAreaField('D30(b). If Yes, please provide the reasons for a having a separate scale:')








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
   
    name = StringField('Area of Operation', validators=[DataRequired()])
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
    mailing_building = StringField('Street Line 1', validators=[DataRequired()])
    mailing_street = StringField('Street Line 2', validators=[DataRequired()])
    mailing_city = StringField('City/Town', validators=[DataRequired()])
    mailing_region = StringField('Region', validators=[DataRequired()])
    mailing_country = StringField('Country', validators=[DataRequired()])


    street_building = StringField('Building', validators=[DataRequired()])
    street_street = StringField('Street', validators=[DataRequired()])
    street_city = StringField('City/Town', validators=[DataRequired()])
    street_country = StringField('Country', validators=[DataRequired()])


    contact_firstname = StringField('Firstname', validators=[DataRequired()])
    contact_middlename = StringField('Middlename', validators=[DataRequired()])
    contact_lastname = StringField('Lastname', validators=[DataRequired()])
    job = StringField('Job Title', validators=[DataRequired()])
     
    # job =  SelectField(
    #     'Job Title',
    #     choices=[('manager', 'Manager'), ('associate', 'Associate')] , validators=[DataRequired()]
    # )
    email = StringField('Email Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])


   


    registration = StringField('Registration Number', validators=[DataRequired()])

    tax_id = StringField('Tax ID', validators=[DataRequired()])

    submit = SubmitField('Submit')





class SurveyForm(FlaskForm):
   
    base_salary = FloatField('Annual Base Salary (GHS)', validators=[DataRequired()])
    
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