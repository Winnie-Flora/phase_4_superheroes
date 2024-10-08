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

@app.route('/heroes')
def heroes():

    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
          "id": hero.id,
          "name": hero.name,
          "super_name": hero.super_name  
        }
        heroes.append(hero_dict)

    response = make_response(
        jsonify(heroes),
        200
    )

    return response


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

    # Return the serialized hero data as JSON
    #return jsonify(hero_data), 200



# Run the application
if __name__ == '__main__':
    app.run(debug=True)
