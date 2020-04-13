from flask_login import login_user, current_user, logout_user, login_required
from dashboard.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from dashboard import db, bcrypt

agent_login = Blueprint('agent_login',__name__)


# index page
@agent_login.route('/agent_login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated :
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        Agent = db.session.query(Agent).filter_by(PhoneNumber = request.form['PhoneNumber']).first()
        if Agent and bcrypt.check_password_hash(Agent.Pasword, request.form['Pasword']):
            login_user(Agent)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else :
            return render_template('login_agent.html')
    return render_template('login_agent.html')

    
# index page
@agent_login.route('/index', methods=['POST','GET'])
@login_required
def index():
    OrdersNumbers  = db.session.query(OrdersMaintenance).count()
    AgentNumbers = db.session.query(Agent).count()
    ServiceNumbers = db.session.query(Service).count()
    UsersNumbers = db.session.query(Users).count()
    return render_template('index.html', OrdersNumbers = OrdersNumbers, AgentNumbers = AgentNumbers, ServiceNumbers = ServiceNumbers, UsersNumbers = UsersNumbers)
    
# logout route
@agent_login.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))
    