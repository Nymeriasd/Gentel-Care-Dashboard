from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Farmer, Business, Situation, OrdersMaintenance, OrderStatus, Priority, Time, OrdersCleaning, ExtraService
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt
import random
import string
from datetime import datetime


ordercleaning = Blueprint('ordercleaning',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

def random_string_generator(size=5,  chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# get orders
@ordercleaning.route('/ordercleaning', methods=['POST', 'GET'])
@login_required
def get_order():
    OrdersItems = db.session.query(OrdersCleaning).all()
    OrderStatusItems = db.session.query(OrderStatus).all()
    ExtraServiceItems = db.session.query(ExtraService).join(Situation).filter(Situation.Situation == 'Enabled').all()

    return render_template('ordercleaning.html', OrdersItems = OrdersItems, OrderStatusItems = OrderStatusItems, ExtraServiceItems = ExtraServiceItems)

# add new order
@ordercleaning.route('/ordercleaning/new', methods=['POST', 'GET'])
@login_required
def add_order():
    if request.method == 'POST':
        GetService = db.session.query(Service).filter(Service.IdService == request.form['Services']).one()
        NewOrder = OrdersMaintenance(OrderNumber = "O"+random_string_generator(), FirstName = request.form['CustomerFirstName'], LastName = request.form['CustomerLastName'], PhoneNumber = request.form['CustomerPhone'], Address = request.form['CustomerAddress'], Email = request.form['CustomerEmail'], IdService = request.form['Services'], IdPriority = request.form['Priority'], IdOrderStatus = 1, Ordertime = request.form['Ordertime'], Price = GetService.Price, Comment = request.form['comment'], Time = request.form['Time'])
        try :
            db.session.add(NewOrder)
            db.session.commit()
    
            flash('Yes !! Order inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('ordercleaning.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order did not insert successfully . Please check insertion ', 'danger')
 
    return redirect(url_for('ordercleaning.get_order'))

# edit order
@ordercleaning.route('/ordercleaning/<int:IdOrder>/edit', methods=['POST', 'GET'])
@login_required
def edit_order(IdOrder):
    if request.method == 'POST':
        EditOrder = db.session.query(OrdersMaintenance).filter_by(IdOrder = IdOrder).one()
        EditOrder.FirstName = request.form['CustomerFirstName']
        EditOrder.FirstName  = request.form['CustomerLastName']
        EditOrder.PhoneNumber = request.form['CustomerPhone']
        EditOrder.Address = request.form['CustomerAddress']
        EditOrder.Email  = request.form['CustomerEmail']
        EditOrder.IdService  = request.form['Services']
        GetService = db.session.query(Service).filter(Service.IdService == EditOrder.IdService).one()
        EditOrder.IdPriority  = request.form['Priority']
        EditOrder.Ordertime  = request.form['Ordertime']
        EditOrder.Price  = GetService.Price
        EditOrder.Comment  = request.form['comment']
        EditOrder.Time  = request.form['Time']
        try :
            db.session.add(EditOrder)
            db.session.commit()
            flash('Yes !! Order is edited successfully '+ Happy , 'success')
            return redirect(url_for('ordercleaning.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order did not edit successfully . Please check insertion ' , 'danger')
           
    return redirect(url_for('ordercleaning.get_order'))


# edit status order
@ordercleaning.route('/ordercleaning/<int:IdOrder>/status', methods=['POST', 'GET'])
@login_required
def edit_status_order(IdOrder):
    if request.method == 'POST':
        EditOrder = db.session.query(OrdersCleaning).filter_by(IdOrder = IdOrder).one()
        EditOrder.IdOrderStatus = request.form['OrderStatusName']
       
        try :
            db.session.add(EditOrder)
            db.session.commit()
            flash('Yes !! Order status is edited successfully '+ Happy , 'success')
            return redirect(url_for('ordercleaning.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order status did not edit successfully . Please check insertion ' , 'danger')
         
    return redirect(url_for('ordercleaning.get_order'))


# delete Order
@ordercleaning.route('/order/<int:IdOrder>/delete', methods=['POST', 'GET'])
@login_required
def delete_order(IdOrder):
    if request.method == 'GET':
        DeleteOrder = db.session.query(OrdersCleaning).filter_by(IdOrder = IdOrder).one()
        try :
            db.session.delete(DeleteOrder)
            db.session.commit()
            flash('Yes !! Order is deleted successfully '+ Happy , 'success')
            return redirect(url_for('ordercleaning.get_order'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
        
    return redirect(url_for('ordercleaning.get_order'))
