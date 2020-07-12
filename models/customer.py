from db import db

class Customer(db.Model):
    __tablename__ = 'customer'
    phone = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(50))
    address = db.Column(db.String(250))
    city = db.Column(db.String(50))
    pincode = db.Column(db.Integer)
    taluk = db.Column(db.String(50))

    def __init__(self, phone, customer_name, address, city, pincode, taluk):
        self.phone = phone
        self.customer_name = customer_name
        self.address = address
        self.city = city
        self.pincode = pincode
        self.taluk = taluk

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"phone":self.phone, "customer_name":self.customer_name, "address":self.address, "city":self.city,"pincode":self.pincode, "taluk":self.taluk}
    
    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Customer.customer_name).all()