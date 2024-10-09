from flask import Flask, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Hero, HeroPower, Power

# Initialize the Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"
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
    hero_dict_list = [hero.to_dict(rules=('-hero_powers',)) for hero in hero_list]

    response = make_response(
        jsonify(hero_dict_list),
        200
    )

    return response

# Get heroes by id
@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):

    hero = Hero.query.get(id)
    
    # If the hero doesn't exist, return a 404 error
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    # Serialize the hero's data
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": []
    }

    # Loop through hero's powers (HeroPower relationship) and serialize them
    for hero_power in hero.hero_powers:
        power_data = {
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power": {
                "id": hero_power.power.id,
                "name": hero_power.power.name,
                "description": hero_power.power.description
            },
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
        }
        hero_data["hero_powers"].append(power_data)

    response = make_response(
        jsonify(hero_data),
        200
    )

    return response



# Get all powers
@app.route('/powers')
def powers():

    powers = []

    for power in Power.query.all():
        power_dict = {
          "description": power.description,  
          "id": power.id,
          "name": power.name,
        }
        powers.append(power_dict)

    response = make_response(
        jsonify(powers),
        200
    )

    return response

# Get powers by id
@app.route('/powers/<int:id>', methods=['GET'])
def power_by_id(id):

    power=Power.query.get(id)

    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    power_data={
        "description": power.description,  
        "id": power.id,
        "name": power.name,
    }

    response = make_response(
        jsonify(power_data),
        200
    )

    return response

# Update powers by id
@app.route('/powers/<int:id>', methods=['PATCH'])
def add_power():

    for attr in request.form:
        setattr(power, attr, request.form.get(attr))

        db.session.add(power)
        db.session.commit()

        power_dict = power.to_dict()

        response = make_response(
            power_dict,
            200
        )

        return response 

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=5555)
