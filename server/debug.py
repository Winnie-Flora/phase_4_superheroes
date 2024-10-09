import ipdb
from models import Hero, HeroPower, Power
from app import app

if __name__ == '__main__':
    with app.app_context():
        ipdb.set_trace()