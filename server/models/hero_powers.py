from . import db
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.schema import UniqueConstraint

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String, nullable=False)

    __table_args__ = (
        UniqueConstraint('hero_id', 'power_id', name='uq_hero_id_powerId'),
    )

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-power.hero_powers', '-hero.hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(
                f"Invalid strength value. Must be one of: {valid_strengths}")
        return value
