from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

# Initialize the Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///app.db"


# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
Migrate(app, db)



# Run the application
if __name__ == '__main__':
    app.run(debug=True)
