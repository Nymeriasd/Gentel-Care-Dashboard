from dashboard import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(IdUser):
    return Users.query.get(int(IdUser))





class Service(db.Model):
    IdService = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    CreatedAt = db.Column(db.DateTime, nullable=False) 
    situation = db.relationship('Situation', backref='Service')


    def __repr__(self) :
        return f"Service('{self.IdService}','{self.Name},'{self.Enabled}','{self.CreatedAt}')"



class Role(db.Model):
    IdRole = db.Column(db.Integer, primary_key=True)
    Role = db.Column(db.String(250), nullable=False)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Role('{self.IdRole}','{self.Role},'{self.CreatedAt}')"

class Users(db.Model, UserMixin):
    IdUser = db.Column(db.Integer, primary_key=True)
    IdRole = db.Column(db.Integer, db.ForeignKey('role.IdRole'))
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    Email = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    Pasword = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    role = db.relationship('Role',  backref="Users")
    situation = db.relationship('Situation', backref='Users')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.IdUser}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except TypeError :
            print('Type error in verify reset token') 
        except Exception as e :
            print("Error '{0}' occurred. Arguments {1}.".format(e.message, e.args))
        finally :
            if user_id is None :
                user_id = None
        return Users.query.get(user_id)
    def __repr__(self) :
        return f"Users('{self.IdUser}','{self.IdRole},'{self.FirstName}','{self.LastName}','{self.Email}','{self.PhoneNumber}','{self.Address}','{self.Pasword}','{self.CreatedAt}','{self.Enabled}')"        

    def get_id(self):
        return (self.IdUser)

class Farmer(db.Model):
    Idfarmer = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    # IdCrop = db.Column(db.Integer , db.ForeignKey('crop.IdCrop'))
    Harvestime = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Farmer('{self.Idfarmer}',{self.FirstName}','{self.LastName}','{self.PhoneNumber}','{self.Address}','{self.IdCrop}','{self.Harvestime}','{self.CreatedAt}')"        



class Business(db.Model):
    IdBusines = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    Email = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    BusinesName = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Business('{self.IdBusines}',{self.FirstName}','{self.LastName}','{self.Email}','{self.PhoneNumber}','{self.Address}','{self.BusinesName}','{self.CreatedAt}')"        

class Price(db.Model):
    IdPrice = db.Column(db.Integer, primary_key=True)
    # IdCrop = db.Column(db.Integer, db.ForeignKey('crop.IdCrop'))
    IdService = db.Column(db.Integer, db.ForeignKey('Service.IdService'))
    IdQty = db.Column(db.Integer, db.ForeignKey('quantity.IdQty'))
    IdUser  = db.Column(db.Integer, db.ForeignKey('users.IdUser'))
    Price  = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False)
    # crop = db.relationship("Crop", backref="Price") 
    # Service = db.relationship("Service", backref="Price")
    # qty = db.relationship("Quantity", backref="Price")
    user = db.relationship("Users", backref="Price")


    def __repr__(self) :
        return f"Price('{self.IdPrice}',{self.IdCrop}','{self.IdService}','{self.IdQty}','{self.IdUser}','{self.Price}','{self.CreatedAt}')"        


class Situation(db.Model):
    IdSituation = db.Column(db.Integer, primary_key=True)
    Situation  = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Situation('{self.IdSituation}','{self.Situation}','{self.CreatedAt}')"


class Orders(db.Model):
    IdOrder = db.Column(db.Integer, primary_key=True)
    OrderNumber = db.Column(db.String(250), nullable=True)
    IdBusines = db.Column(db.Integer, db.ForeignKey('business.IdBusines'))
    # IdCrop = db.Column(db.Integer, db.ForeignKey('crop.IdCrop'))
    # IdQty = db.Column(db.Integer, db.ForeignKey('quantity.IdQty'))
    IdOrderStatus  = db.Column(db.Integer, db.ForeignKey('order_status.IdOrderStatus'))
    Price  = db.Column(db.String(250), nullable=True)
    Ordertime = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False)
    # crop = db.relationship("Crop", backref="Orders") 
    # qty = db.relationship("Quantity", backref="Orders")
    orderstatus = db.relationship("OrderStatus", backref="Orders")
    business = db.relationship("Business", backref="Orders") 

    def __repr__(self) :
        return f"Orders('{self.IdOrder}',{self.OrderNumber}','{self.IdBusines}','{self.IdCrop}','{self.IdQty}','{self.IdOrderStatus}','{self.Price}','{self.Ordertime}','{self.CreatedAt}')"        

class OrderStatus(db.Model):
    IdOrderStatus = db.Column(db.Integer, primary_key=True)
    OrderStatus  = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"OrderStatus('{self.IdOrderStatus}','{self.OrderStatus}','{self.CreatedAt}')"


