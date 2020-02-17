from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Farmer, Business, Price, Situation, Orders, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt

business = Blueprint('business',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get all business
@business.route('/business', methods=['POST', 'GET'])
@login_required
def get_business():
    BusinessItems = db.session.query(Business).all()
    return render_template('business.html', BusinessItems = BusinessItems)

# add Business
@business.route('/business/new', methods=['POST', 'GET'])
@login_required
def add_business():
    if request.method == 'POST' :
        NewBusiness = Business(FirstName = request.form['FirstName'], LastName = request.form['LastName'], Email = request.form['Email'], PhoneNumber = request.form['PhoneNumber'], Address = request.form['Address'], BusinesName = request.form['BusinesName'])
        try :
            db.session.add(NewBusiness)
            db.session.commit()
            flash('Yes !! Business inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('business.get_business'))
        except Exception as err :
            flash('No !! ' + Sad + ' Business did not insert successfully . Please check insertion ', 'danger')
        
    return redirect(url_for('business.get_business'))

# edit business
@business.route('/business/<int:IdBusines>/edit', methods=['POST', 'GET'])
@login_required
def edit_busines(IdBusines):
    if request.method == 'POST':
        EditBusiness = db.session.query(Business).filter_by(IdBusines = IdBusines).one()
        EditBusiness.FirstName = request.form['FirstName']
        EditBusiness.LastName = request.form['LastName']
        EditBusiness.Email = request.form['Email']
        EditBusiness.PhoneNumber = request.form['PhoneNumber']
        EditBusiness.Address = request.form['Address']
        EditBusiness.BusinesName = request.form['BusinesName']
        try :
            db.session.add(EditBusiness)
            db.session.commit()
            flash('Yes !! Business is edited successfully '+ Happy , 'success')
            return redirect(url_for('business.get_business'))
        except Exception as err :
            flash('No !! ' + Sad + ' Business did not edit successfully . Please check insertion ' , 'danger')
        
    return redirect(url_for('business.get_business'))

        

# delete Business
@business.route('/business/<int:IdBusines>/delete', methods=['POST', 'GET'])
@login_required
def delete_business(IdBusines):
    if request.method == 'GET':
        DeleteBusines = db.session.query(Business).filter_by(IdBusines = IdBusines).one()
        try :
            db.session.delete(DeleteBusines)
            db.session.commit()
            flash('Yes !! Business is deleted successfully '+ Happy , 'success')
            return redirect(url_for('business.get_business'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
          
    return redirect(url_for('business.get_business'))
