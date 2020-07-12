from db import db

class ServiceParts(db.Model):
    __tablename__ = 'customer'
    service_id = db.Column(db.Integer)
    part_no = db.Column(db.Integer)

    def __init__(self, service_id, part_no):
        self.service_id = service_id
        self.part_no = part_no

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"service_id":self.service_id, "part_no":self.part_no}
    
    @classmethod
    def find_by_service_id(cls, service_id):
        return cls.query.filter_by(service_id=service_id).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(ServiceParts.service_id).all()