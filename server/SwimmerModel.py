from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import json
from config import app

db = SQLAlchemy(app)

class Swimmer(db.Model):
    __tablename__ = "swimmers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(80))
    age = db.Column(db.Integer)

    def add_swimmer(_id, _name, _club, _age):
        new_swimmer = Swimmer(name=_name, club=_club, age=_age)
        db.session.add(new_swimmer)
        db.session.commit()

    def get_all_swimmers():
        return [Swimmer.json(swimmer) for swimmer in Swimmer.query.all()]

    def get_swimmer_by_name(_name):
        return Swimmer.json(Swimmer.query.filter(Swimmer.name.ilike(_name)).first())

    def json(self):
        if self==None:
            return {}
        else:
            return {
                'id': self.id,
                'name': self.name,
                'club': self.club,
                'age': self.age
            }

    def __repr__(self):
        swimmer_object = {
            'id': self.id,
            'name': self.name,
            'club': self.club,
            'age': self.age
        }
        return json.dumps(swimmer_object)