from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config')

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)  # Make sure the db is properly initialized with the app
migrate = Migrate(app, db)

# Import models
from models.heroes import Hero
from models.powers import Power
from models.hero_powers import HeroPower

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
