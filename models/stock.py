from db import db

class Stock(db.Model):
    __tablename__ = 'stock'
    part_no = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    vehicle_model = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    gst = db.Column(db.Integer)

    def __init__(self, part_no, part_name, price, vehicle_model, quantity, gst):
        self.part_no = part_no
        self.part_name = part_name
        self.price = price
        self.vehicle_model = vehicle_model
        self.quantity = quantity
        self.gst = gst

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"part_no":self.part_no, "part_name":self.part_name, "price":self.price, "vehicle_model":self.vehicle_model, "quantity": self.quantity, "gst":self.gst}
    
    @classmethod
    def find_by_part_no(cls, part_no):
        return cls.query.filter_by(part_no=part_no).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Stock.part_name).all()