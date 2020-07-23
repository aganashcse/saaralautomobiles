from db import db

class Stock(db.Model):
    __tablename__ = 'stock'
    s_no = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    invoice_no = db.Column(db.String(50))
    part_no = db.Column(db.String(50), primary_key=True)
    part_name = db.Column(db.String(50))
    price = db.Column(db.Integer, primary_key=True)
    vehicle_model = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    gst = db.Column(db.Integer)

    def __init__(self, invoice_no, part_no, part_name, price, vehicle_model, quantity, gst):
        self.invoice_no = invoice_no
        self.part_no = part_no
        self.part_name = part_name
        self.price = price
        self.vehicle_model = vehicle_model
        self.quantity = quantity
        self.gst = gst

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"invoice_no": self.invoice_no, "s_no":self.s_no,"part_no":self.part_no, "part_name":self.part_name, "price":self.price, "vehicle_model":self.vehicle_model, "quantity": self.quantity, "gst":self.gst}
    
    @classmethod
    def find_by_s_no(cls, s_no):
        return cls.query.filter_by(s_no=s_no).first()

    @classmethod
    def find_by_part_no(cls, part_no):
        return cls.query.filter_by(part_no=part_no).all()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Stock.s_no).all()
    
    @classmethod
    def find_by_part_no_price(cls, part_no, price):
        return cls.query.filter_by(part_no=part_no, price=price).first()