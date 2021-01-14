from flask import render_template,request,Blueprint, redirect, url_for,flash
from flask_login import login_user, current_user, logout_user , login_required
from survey.models import User,Contact,Individual_request,Corporate_request
from survey import db,bcrypt
from survey.users.forms import ContactForm,IndividualRequestForm,CorporateRequestForm
from datetime import datetime



main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def index():
    if current_user.role == 'admin':
        return redirect(url_for('users.admin_home'))
    
    return render_template('new_client_dashboard.html')
 






@main.route("/",methods=["POST","GET"])
def landing():

    form = ContactForm()
    if form.validate_on_submit():
        
        contact = Contact(title=form.title.data,firstname=form.firstname.data,lastname=form.lastname.data,email=form.email.data,job_title=form.job_title.data,company_name=form.company_name.data,phone=form.phone.data,address_1=form.address_1.data,address_2=form.address_2.data,city=form.city.data,country=form.country.data)
        db.session.add(contact)
        db.session.commit()
        flash('Request Successful','success')
       
        return redirect(url_for('main.landing'))

   
    if current_user.is_authenticated and current_user.role == 'admin':
        
        return redirect(url_for('users.admin_home'))
    if current_user.is_authenticated and current_user.role != 'admin':
        return redirect(url_for('main.index'))

    return render_template("new_landing.html",form=form)

@main.route("/requests/individual",methods=["POST","GET"])
def individual_requests():
    form = IndividualRequestForm()
    if form.validate_on_submit():
        
        indv = Individual_request(firstname=form.firstname.data,lastname=form.lastname.data,other=form.other.data,email=form.email.data,dob=form.dob.data,phone=form.phone.data,city=form.city.data,country=form.country.data,service=form.service.data,address=form.address.data)
        db.session.add(indv)
        db.session.commit()
        flash('Thank you for the request. You will be contacted by a Deloitte Professional','success')
        return redirect(url_for('main.individual_requests'))
    return render_template("individual_request.html",form=form)


@main.route("/requests/corporate",methods=["POST","GET"])
def corporate_requests():
    form = CorporateRequestForm()
    if form.validate_on_submit():
       corp = Corporate_request(
        company_name = form.company_name.data,
        sector = form.sector.data,
        industry = form.industry.data,
        area = form.area.data,
        financial_year_end = form.financial_year_end.data,
        company_type = form.company_type.data,
        postal_address = form.postal_address.data,
        street_address = form.street_address.data,
        reg_number = form.reg_number.data,
        vat_number = form.vat_number.data,
        tel = form.tel.data,
        company_email = form.company_email.data,
        website = form.website.data,
        date_inc = form.date_inc.data,
        country_inc = form.country_inc.data,
        chair_firstname = form.chair_firstname.data,
        chair_lastname = form.chair_lastname.data,
        chair_other = form.chair_other.data,
        chair_nation = form.chair_nation.data,
        chair_email = form.chair_email.data,
        chair_phone = form.chair_phone.data,
        ceo_firstname=form.ceo_firstname.data,
        ceo_lastname=form.ceo_lastname.data,
        ceo_other=form.ceo_other.data,
        ceo_nation=form.ceo_nation.data,
        ceo_email=form.ceo_email.data,
        ceo_phone=form.ceo_phone.data,
        other_board_firstname=form.other_board_firstname.data,
        other_board_lastname=form.other_board_lastname.data,
        other_board_other=form.other_board_other.data,
        other_board_nation=form.other_board_nation.data,
        other_board_email=form.other_board_email.data,
        other_board_phone=form.other_board_phone.data,
        key_firstname=form.key_firstname.data,
        key_lastname=form.key_lastname.data,
        key_other=form.key_other.data,
        key_nation=form.key_nation.data,
        key_email=form.key_email.data,
        key_phone=form.key_phone.data,
        prev_name=form.prev_name.data,
        prev_address=form.prev_address.data,
        prev_city=form.prev_address.data,
        prev_country=form.prev_country.data,
        current_name=form.current_name.data,
        current_address=form.current_address.data,
        current_city=form.current_address.data,
        current_country=form.current_country.data,
        sec_name=form.sec_name.data,
        sec_address=form.sec_address.data,
        sec_city=form.sec_address.data,
        sec_country=form.sec_country.data,
        contact_firstname=form.contact_firstname.data,
        contact_lastname=form.contact_lastname.data,
        contact_other=form.contact_other.data,
        contact_nation=form.contact_nation.data,
        contact_email=form.contact_email.data,
        contact_dob=form.contact_dob.data,
        contact_phone=form.contact_phone.data,
        brief_history=form.brief_history.data,
        service=form.service.data
        )
       db.session.add(corp)
       db.session.commit()
       flash('Thank you for the request. You will be contacted by a Deloitte Professional','success')
       return redirect(url_for('main.corporate_requests'))
    return render_template("corporate_request.html",form=form)



@main.route("/contact")
def contact():
    
    return render_template("contact.html")


@main.route("/terms")
def terms():
    
    return render_template("terms.html")


@main.route("/privacy")
def privacy():
    
    return render_template("privacy.html")




