from flask_sqlalchemy import SQLAlchemy


# Initialize the database instance
db = SQLAlchemy()

# Import the models
from .heroes import Hero
from .powers import Power
from .hero_powers import HeroPower
