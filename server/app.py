from flask import Flask, jsonify, make_response, request
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

# Initialize and configure a Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
Migrate(app, db)

# Index route
@app.route('/')
def home():
    return 'Superheroes Data'


# Get all heroes
@app.route('/heroes')
def heroes():
    # Extract all heroes from the database
    hero_list = Hero.query.all()
    # Serialize all heroes
    hero_dict_list = [
        hero.to_dict(rules=('-hero_powers', )) for hero in hero_list
    ]
    # Return json response
    response = make_response(jsonify(hero_dict_list), 200)
    return response


# Get hero by id
@app.route('/heroes/<int:id>')
def hero_by_id(id):
    # Extract hero from the database with given id
    hero = Hero.query.get(id)

    # If the hero doesn't exist, return a 404 error
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    # Serialize the hero's data
    hero_dict = hero.to_dict()

    # Return the json response
    response = make_response(jsonify(hero_dict), 200)
    return response


# Get all powers
@app.route('/powers')
def powers():
    # Extract all powers from the database
    power_list = Power.query.all()

    # Serialize all powers
    power_dict_list = [
        power.to_dict(rules=('-hero_powers', )) for power in power_list
    ]

    # Return response as json
    response = make_response(jsonify(power_dict_list), 200)
    return response


# Get powers by id
@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):
    # Fetch power with given id from database
    power = Power.query.get(id)

    # Check if power exists, if not return appropriate error message
    if not power:
        return jsonify({"errors": ["Power not found"]}), 404

    if request.method == 'GET':
        # Serialize power instance
        power_dict = power.to_dict(rules=('-hero_powers', ))

        # Return json reponse
        response = make_response(jsonify(power_dict), 200)
        return response
    if request.method == 'PATCH':
        # Attempt to save record to database if valid
        try:
            # Extract data as json
            data = request.json
            # Dynamically update power instance
            for attr in data:
                setattr(power, attr, data[attr])

            # Save to database
            db.session.add(power)
            db.session.commit()

            # Serialize power instance
            power_dict = power.to_dict(rules=('-hero_powers', ))

            # Return json response
            response = make_response(jsonify(power_dict), 200)
            return response
        except ValueError as e:
            # return any client errors
            return jsonify({'errors': [str(e)]}), 400
        except:
            return jsonify({'errors': ['An unexpected error occurred.']}), 500


@app.route('/hero_powers', methods=['POST'])
def hero_powers():
    # Extract data as json
    data = request.json

    errors = []
    try:
        # Validate hero_id and power_id
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])

        if hero is None:
            raise ValueError(f'Invalid value for hero_id')
        if power is None:
            raise ValueError('Invalid value for power_id')

        # Save hero to database
        new_hero_power = HeroPower(strength=data['strength'],
                                   power_id=data['power_id'],
                                   hero_id=data['hero_id'])
        db.session.add(new_hero_power)
        db.session.commit()

        # Serialize model instance
        new_hero_power_dict = new_hero_power.to_dict()

        # Return json response
        response = make_response(jsonify(new_hero_power_dict), 201)
        return response
    except KeyError as e:
        errors.append(f'Missing required field: {str(e)}')
    except ValueError as e:
        errors.append(str(e))
    except IntegrityError as e:
        if 'UNIQUE' in str(e):
            errors.append('Duplicate hero_power.')
    except:
        return {'errors': ['An uknown error occcured.']}
    return jsonify({'errors': errors}), 400


# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5555)
