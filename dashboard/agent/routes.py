from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt

agent = Blueprint('agent',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get all business
@agent.route('/agent', methods=['POST', 'GET'])
@login_required
def get_business():
    AgentItems = db.session.query(Agent).all()
    return render_template('agent.html', AgentItems = AgentItems)

# add Business
@agent.route('/agent/new', methods=['POST', 'GET'])
@login_required
def add_business():
    if request.method == 'POST' :
        NewBusiness = Business(FirstName = request.form['FirstName'], LastName = request.form['LastName'], Email = request.form['Email'], PhoneNumber = request.form['PhoneNumber'], Address = request.form['Address'], BusinesName = request.form['BusinesName'])
        try :
            db.session.add(NewBusiness)
            db.session.commit()
            flash('Yes !! Agent inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('agent.get_business'))
        except Exception as err :
            flash('No !! ' + Sad + ' Agent did not insert successfully . Please check insertion ', 'danger')
        
    return redirect(url_for('agent.get_business'))

# edit business
@agent.route('/agent/<int:IdBusines>/edit', methods=['POST', 'GET'])
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
            flash('Yes !! Agent is edited successfully '+ Happy , 'success')
            return redirect(url_for('agent.get_business'))
        except Exception as err :
            flash('No !! ' + Sad + ' Agent did not edit successfully . Please check insertion ' , 'danger')
        
    return redirect(url_for('agent.get_business'))

        

# delete Business
@agent.route('/agent/<int:IdBusines>/delete', methods=['POST', 'GET'])
@login_required
def delete_business(IdBusines):
    if request.method == 'GET':
        DeleteBusines = db.session.query(Business).filter_by(IdBusines = IdBusines).one()
        try :
            db.session.delete(DeleteBusines)
            db.session.commit()
            flash('Yes !! Agent is deleted successfully '+ Happy , 'success')
            return redirect(url_for('agent.get_business'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
          
    return redirect(url_for('agent.get_business'))
