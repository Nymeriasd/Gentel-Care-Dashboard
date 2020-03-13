from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from dashboard.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from dashboard.services.routes import services
    from dashboard.role.routes import role
    from dashboard.users.routes import users
    from dashboard.farmer.routes import farmer 
    from dashboard.business.routes import business
    from dashboard.status.routes import status
    from dashboard.order.routes import orders
    from dashboard.condition.routes import condition
    from dashboard.order_status.routes import order_status
    from dashboard.priority.routes import priority
    from dashboard.extraservices.routes import extraservices
    from dashboard.main.routes import main 

    app.register_blueprint(services)
    app.register_blueprint(role)
    app.register_blueprint(users)
    app.register_blueprint(farmer)
    app.register_blueprint(business)
    app.register_blueprint(status)
    app.register_blueprint(orders)
    app.register_blueprint(condition)
    app.register_blueprint(order_status)
    app.register_blueprint(priority)
    app.register_blueprint(extraservices)
    app.register_blueprint(main)

    return app
    