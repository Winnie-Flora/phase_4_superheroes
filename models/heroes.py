from . import db

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade="all, delete-orphan")
    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes', overlaps="hero_powers")

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [hero_power.power.serialize() for hero_power in self.hero_powers]
        }
