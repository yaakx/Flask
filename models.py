# -*- coding: utf-8 -*-

"""Models for Place and People usin SQLAlchemy"""

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import TINYINT
from app import db


class Place(db.Model):

    """Place model for places microservice"""

    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    people = db.relationship('People', backref='places')

    def __init__(self, name):

        self.name = name

    def insert(self):

        """POST"""

        db.session.add(self)
        db.session.commit()

    def update(self, name):

        """PUT"""

        self.name = name
        db.session.commit()

    def remove(self):

        """DELETE"""

        db.session.delete(self)
        db.session.commit()

    def __repr__(self):

        return '<Place(name={})>'.format(self.name)


class People(db.Model):

    """People model for model microservice"""

    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    isAlive = Column(TINYINT(1))
    idplace = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=True)

    def __init__(self, name, isAlive, idplace):

        self.name = name
        self.isAlive = isAlive
        self.idplace = idplace

    def insert(self):

        """POST"""

        db.session.add(self)
        db.session.commit()

    def update(self, name, isAlive, idplace):

        """PUT"""

        self.name = name
        self.isAlive = isAlive
        self.idplace = idplace
        db.session.commit()

    def remove(self):

        """DELETE"""

        db.session.delete(self)
        db.session.commit()

    def IsCorrect(self, alive):

        """Limiting isAlive to 0 or 1"""
        
        self.errMsg = ""
        if alive not in ["0", "1"]:
            self.errMsg = 'isAlive value not allowed'
            return False
        return True

    def __repr__(self):
        return '<Place(name={}, isAlive={}, idplace={})>'.format(self.name, self.isAlive, self.idplace)
