# Superheroes API Project
This Flask-based web application helps us manage superheroes data. It features an interface that retrieves, updates, and creates superheroes details.

## Features
- Get heroes and powers: You can get a list of heroes or powers.
- Update powers: You can change the existing powers using PATCH request
- Create relationships: You can create hero-power relationship by assigning powers to heroes.

## Prerequisites
- Install python 3.10 or higher
- For dependency management run:
  pip install pipenv

## Installation
1. Clone the repository:
git clone git@github.com:Winnie-Flora/phase_4_superheroes.git

2. Navigate into the project directory:
cd phase-4-superheroes

3. Install the dependencies:
pipenv install 

## Running Application
1. Start virtual environment run:
pipenv shell

2. To run Flask app:
cd server
python app.py

## To Run Migrations:
1. Create a migration using:
flask db migrate -m "message"
2. Apply migrations:
flask db upgrade

## Seed Data
To populate the database run:
1. cd server
2. python seed.py

## API Endpoints
1. GET /heroes
Returns a list of all heroes, excluding powers.

2. GET /heroes/<id>
Provides details for a hero by their ID.

3. GET /powers
Returns a list of all powers.

4. GET /powers/<id>
Returns details of a specific power by ID.

5. PATCH /powers/<id>
Updates a power’s details.

6. POST /hero_powers
Creates a new hero-power, with custom strength.