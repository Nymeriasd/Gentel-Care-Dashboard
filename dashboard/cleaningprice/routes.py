from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Agent,Situation, OrdersMaintenance, OrderStatus, CleaningPrice
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt

cleaningprice = Blueprint('cleaningprice',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

# get all services
@cleaningprice.route('/cleaningprice', methods=['POST','GET'])
@login_required
def get_cleaningprice():
    CleaningPriceItems = db.session.query(CleaningPrice).all()
    SituationItems = db.session.query(Situation).all()
    return render_template('cleaningprice.html', CleaningPriceItems = CleaningPriceItems, SituationItems = SituationItems)

# add new services
@cleaningprice.route('/cleaningprice/new', methods=['POST','GET'])
@login_required
def add_cleaningprice():
    if request.method == 'POST':
        NewCleaningPrice = CleaningPrice(Name = request.form['ServiceName'], Price = request.form['Price'] , Enabled= request.form['Status'])
        try :
            db.session.add(NewCleaningPrice)
            db.session.commit()
            flash('Yes !! Service inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('cleaningprice.get_cleaningprice'))
        except Exception as err :
            flash('No !! ' + Sad + ' Service did not insert successfully . Please check insertion ' , 'danger')

    return redirect(url_for('cleaningprice.get_cleaningprice'))

# edit services
@cleaningprice.route('/cleaningprice/<int:IdPrice>/edit', methods=['POST','GET'])
@login_required
def edit_cleaningprice(IdPrice):
    if request.method == 'POST':
        EditCleaningPrice = db.session.query(CleaningPrice).filter_by(IdPrice = IdPrice).one()
        EditCleaningPrice.Name = request.form['ServiceName']
        EditCleaningPrice.Price = request.form['Price']
        EditCleaningPrice.Enabled = request.form['Status']
        try :
            db.session.add(EditCleaningPrice)
            db.session.commit()
            flash('Yes !! Service is edited successfully '+ Happy , 'success')
            return redirect(url_for('cleaningprice.get_cleaningprice'))
        except Exception as err :
            flash('No !! ' + Sad + ' Service did not edit successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('cleaningprice.get_cleaningprice'))

# delete services
@cleaningprice.route('/cleaningprice/<int:IdPrice>/delete', methods=['POST','GET'])
@login_required
def delete_cleaningprice(IdPrice):
    if request.method == 'GET':
        DeleteCleaningPrice = db.session.query(CleaningPrice).filter_by(IdPrice = IdPrice).one()
        try :
            db.session.delete(DeleteCleaningPrice)
            db.session.commit()
            flash('Yes !! Service is deleted successfully '+ Happy , 'success')
            return redirect(url_for('cleaningprice.get_cleaningprice'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
 
    return redirect(url_for('cleaningprice.get_cleaningprice'))
