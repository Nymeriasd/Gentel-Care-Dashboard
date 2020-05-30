from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus, OrdersCleaning
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt

main = Blueprint('main',__name__)


# index page
@main.route('/', methods=['POST','GET'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        User = db.session.query(Users).filter_by(Email = request.form['Email']).first()
        if User and bcrypt.check_password_hash(User.Pasword, request.form['Pasword']):
            login_user(User)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else :
            return render_template('login.html')
    return render_template('login.html')

    
# index page
@main.route('/index', methods=['POST','GET'])
@login_required
def index():
    OrdersNumbers  = db.session.query(OrdersMaintenance).count()
    OrderCleaningCount = db.session.query(OrdersCleaning).count()
    AgentNumbers = db.session.query(Agent).count()
    ServiceNumbers = db.session.query(Service).count()
    UsersNumbers = db.session.query(Users).count()
    OrdersMaintenanceGeo = db.session.query(OrdersMaintenance).all()
    OrderCleaningGeo = db.session.query(OrdersCleaning).all()
    AgentGeo = db.session.query(Agent).all()

    print(OrdersMaintenanceGeo)
    print(AgentGeo)
    print(OrderCleaningCount)
    # DoneOrdersGeo  =  db.session.query(OrdersMaintenance).join(OrderStatus).filter(OrdersMaintenance.IdService == current_user.IdService).filter(OrdersMaintenance.IdAgent == current_user.IdAgent).filter(OrderStatus.OrderStatus == 'Done').all()
    # PendingOrdersGeo  =  db.session.query(OrdersMaintenance).join(OrderStatus).filter(OrdersMaintenance.IdService == current_user.IdService).filter(OrderStatus.OrderStatus != 'Done').all()
   
    return render_template('index.html', OrdersNumbers = OrdersNumbers, AgentNumbers = AgentNumbers, ServiceNumbers = ServiceNumbers, UsersNumbers = UsersNumbers, OrdersMaintenanceGeo = OrdersMaintenanceGeo, AgentGeo = AgentGeo, OrderCleaningCount = OrderCleaningCount, OrderCleaningGeo = OrderCleaningGeo)
    
# logout route
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
    