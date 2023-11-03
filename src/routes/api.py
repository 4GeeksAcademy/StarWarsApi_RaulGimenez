from flask import Blueprint
from users import users
from characters import characters
from planets import planets
from starships import starships

api = Blueprint('api', __name__)
api.register_blueprint(users)
api.register_blueprint(characters)
api.register_blueprint(planets)
api.register_blueprint(starships)