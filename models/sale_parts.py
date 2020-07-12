from db import db

class SaleParts(db.Model):
    __tablename__ = 'sale_parts'
    bill_id = db.Column(db.Integer)
    part_no = db.Column(db.Integer)
    quanity = db.Column(db.Integer)

    def __init__(self, bill_id, part_no, quanity):
        self.bill_id = bill_id
        self.part_no = part_no
        self.quanity = quanity

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"bill_id":self.bill_id, "part_no":self.part_no}
    
    @classmethod
    def find_by_bill_id(cls, bill_id):
        return cls.query.filter_by(bill_id=bill_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(SaleParts.service_id).all()