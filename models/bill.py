from db import db

class Bill(db.Model):
    __tablename__ = 'bill'
    phone = db.Column(db.String(50))
    bill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    time = db.Column(db.DateTime)
    total = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    billing_person = db.Column(db.String(50))

    def __init__(self, service_id=None, phone, date, time, total, status, billing_person):
        self.phone = phone
        self.service_id = service_id
        self.date = date
        self.time = time
        self.total = total
        self.status = status
        self.billing_person = billing_person

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"bill_id":self.bill_id, "phone":self.phone, "service_id":self.service_id, "date":self.date, "time":self.time, "total":self.total, "status":self.status,"billing_person":self.billing_person}
    
    @classmethod
    def find_by_bill_id(cls, bill_id):
        return cls.query.filter_by(bill_id=bill_id).first()
    
    @classmethod
    def find_by_service_id(cls, service_id):
        return cls.query.filter_by(service_id=service_id).first()
    
    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(Bill.service_id).all()