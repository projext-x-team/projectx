from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, create_engine
import json
from config import app

db = SQLAlchemy(app)

class Swimmer(db.Model):
    __tablename__ = "swimmers"
    id = db.Column(db.Integer, primary_key=True)
    swimmer_uuid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    club = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    lsc = db.Column(db.String)
    swim_meet = db.Column(db.String)
    meet_date = db.Column(db.String)
    meet_age = db.Column(db.Integer)
    event = db.Column(db.String)
    standard = db.Column(db.String)
    swim_team = db.Column(db.String)
    time=db.Column(db.DateTime) 
    time_h=db.Column(db.Integer) 
    time_m=db.Column(db.Integer) 
    time_s=db.Column(db.Integer) 
    time_ms=db.Column(db.Integer)

    def add_swimmer(_id, _swimmer_uuid, _name, _club, _age):
        new_swimmer = Swimmer(swimmer_uuid=_swimmer_uuid, name=_name, club=_club, age=_age)
        db.session.add(new_swimmer)
        db.session.commit()

    def get_all_swimmers():
        return [Swimmer.json(swimmer) for swimmer in Swimmer.query.all()]

    def get_swimmer_by_id(_id):
        return Swimmer.json(Swimmer.query.filter_by(id=_id).first())

    def get_swimmer_by_name(_name):
        #return Swimmer.json(Swimmer.query.filter(func.lower(Swimmer.name)==func.lower(_name)).first())
        swimmers=[]
        for swimmer in Swimmer.query.filter(Swimmer.name.ilike(_name)).all(): # list of dict
            swimmers.append(Swimmer.json(swimmer))
        return swimmers

    def delete_swimmer(_id):
        is_successful = Swimmer.query.filter_by(id=_id).delete()
        db.session.commit()
        return is_successful

    def update_swimmer_name(_id, _name):
        swimmer_to_update = Swimmer.query.filter_by(id=_id).first()
        swimmer_to_update.name=_name
        db.session.commit()

    def update_swimmer_club(_id, _club):
        swimmer_to_update = Swimmer.query.filter_by(id=_id).first()
        swimmer_to_update.club=_club
        db.session.commit()

    def json(self):
        if self==None:
            return {}
        else:
            return {
                'id': self.id,
                'swimmer_uuid': self.swimmer_uuid,
                'name': self.name,
                'club': self.club,
                'age': self.age,
                'gender': self.gender,
                'lsc': self.lsc,
                'swim_meet': self.swim_meet,
                'meet_date': self.meet_date,
                'meet_age': self.meet_age,
                'event': self.event,
                'standard': self.standard,
                'swim_team': self.swim_team,
                'time': self.time.strftime("%M:%S.%f") [:-4],
                'time_h': self.time_h,
                'time_m': self.time_m,
                'time_s': self.time_s,
                'time_ms': self.time_ms
            }

    def __repr__(self):
        if self==None:
            ret_obj={}
        else:
            ret_obj={
                'id': self.id,
                'swimmer_uuid': self.swimmer_uuid,
                'name': self.name,
                'club': self.club,
                'age': self.age,
                'gender': self.gender,
                'lsc': self.lsc,
                'swim_meet': self.swim_meet,
                'meet_date': self.meet_date,
                'meet_age': self.meet_age,
                'event': self.event,
                'standard': self.standard,
                'swim_team': self.swim_team,
                'time': self.time,
                'time_h': self.time_h,
                'time_m': self.time_m,
                'time_s': self.time_s,
                'time_ms': self.time_ms
            }
        return json.dumps(ret_obj)