from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

# Initialize the Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    if request.method == 'GET':
        power_dict = power.to_dict(rules=('-hero_powers', ))

        response = make_response(jsonify(power_dict), 200)
        return response
    if request.method == 'PATCH':
        try:
            data = request.json
            for attr in data:
                setattr(power, attr, data[attr])

            db.session.add(power)
            db.session.commit()

            power_dict = power.to_dict(rules=('-hero_powers', ))

            response = make_response(jsonify(power_dict), 200)
            return response
        except:
            return jsonify({'errror': ['Validation errors']})


@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    data = request.json
    errors = []
    try:
        new_hero_power = HeroPower(strength=data['strength'],
                                   power_id=data['power_id'],
                                   hero_id=data['hero_id'])
        db.session.add(new_hero_power)
        db.session.commit()
        new_hero_power_dict = new_hero_power.to_dict()
        response = make_response(jsonify(new_hero_power_dict), 201)
        return response
    except KeyError as e:
        errors.append(f'Missing required field: {str(e)}')
    except ValueError as e:
        errors.append(str(e))
    return jsonify({'errors': errors}), 400


# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5555)
