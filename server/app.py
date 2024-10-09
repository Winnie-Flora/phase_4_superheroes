from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

# Initialize the Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
Migrate(app, db)


@app.route('/')
def home():
    return 'Superheroes Data'


# Get all heroes
@app.route('/heroes')
def heroes():
    hero_list = Hero.query.all()
    hero_dict_list = [
        hero.to_dict(rules=('-hero_powers', )) for hero in hero_list
    ]

    response = make_response(jsonify(hero_dict_list), 200)
    return response


# Get hero by id
@app.route('/heroes/<int:id>')
def hero_by_id(id):

    hero = Hero.query.get(id)

    # If the hero doesn't exist, return a 404 error
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    # Serialize the hero's data
    hero_dict = hero.to_dict()

    response = make_response(jsonify(hero_dict), 200)
    return response


# Get all powers
@app.route('/powers')
def powers():
    power_list = Power.query.all()

    power_dict_list = [
        power.to_dict(rules=('-hero_powers', )) for power in power_list
    ]

    response = make_response(jsonify(power_dict_list), 200)
    return response


# Get powers by id
@app.route('/powers/<int:id>', methods=['GET'])
def power_by_id(id):

    power = Power.query.get(id)

    if not power:
        return jsonify({"error": "Power not found"}), 404

    power_dict = power.to_dict(rules=('-hero_powers',))

    response = make_response(jsonify(power_dict), 200)

    return response


# Update powers by id
@app.route('/powers/<int:id>', methods=['PATCH'])
def add_power():

    for attr in request.form:
        setattr(power, attr, request.form.get(attr))

        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()

        response = make_response(power_dict, 200)

        return response


# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5555)
