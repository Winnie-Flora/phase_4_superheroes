import os

# Get the base directory of the project in config.py location
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# Disable modification tracking to save resources (recommended by SQLAlchemy)
SQLALCHEMY_TRACK_MODIFICATIONS = False
