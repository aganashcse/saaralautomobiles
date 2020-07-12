from db import db

class ServiceEntry(db.Model):
    __tablename__ = 'service_entry'
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(50))
    vehicle_no = db.Column(db.String(50))
    engine_no = db.Column(db.String(50))
    chasis_no = db.Column(db.String(50))
    hoursmeter = db.Column(db.Integer)
    complaint = db.Column(db.String(500))
    engineer_name = db.Column(db.String(50))

    def __init__(self, phone, vehicle_no, engine_no, chasis_no, hoursmeter, complaint, engineer_name):
        self.phone = phone
        self.vehicle_no = vehicle_no
        self.engine_no = engine_no
        self.chasis_no = chasis_no
        self.hoursmeter = hoursmeter
        self.complaint = complaint
        self.engineer_name = engineer_name

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def update_record(self):
        db.session.merge(self)
        db.session.flush()
        db.session.commit()
    
    def json(self):
        return {"service_id":self.service_id, "phone":self.phone, "vehicle_no":self.vehicle_no, "engine_no":self.engine_no, "chasis_no":self.chasis_no, "hoursmeter":self.hoursmeter, "complaint":self.complaint, "engineer_name":self.engineer_name}
    
    @classmethod
    def find_by_service_id(cls, service_id):
        return cls.query.filter_by(service_id=service_id).first()
    
    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.order_by(ServiceEntry.service_id).all()