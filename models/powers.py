from . import db
from sqlalchemy.orm import validates

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='power', cascade="all, delete-orphan")
    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers')

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }
