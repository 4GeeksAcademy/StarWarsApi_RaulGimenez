import os
from flask import Blueprint, request, jsonify
from utils import APIException
from models import db, User,  Planets, Characters, Starships, Favorites


users =Blueprint('users', __name__)

@users.route('/user', methods=['GET'])
def get_users():
    users= User.query.all()
    all_users = list(map(lambda item: item.serialize(), users))
    if all_users == []:
         raise APIException('There are no users', status_code=404)
    return jsonify(all_users), 200

@users.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    chosen_user = User.query.filter_by(id=user_id).first()
    if chosen_user is None:
         raise APIException('User does not exist', status_code=404)
    return jsonify(chosen_user.serialize()), 200

@users.route('/user', methods=['POST'])
def create_user():
    request_body_user = request.get_json()
    new_user = User(username=request_body_user["username"], email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(request_body_user), 200

@users.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    request_body_user = request.get_json()
    chosen_user = User.query.get(user_id)
    if chosen_user is None:
        raise APIException('User not found', status_code=404)
    if "username" in request_body_user:
        chosen_user.username = request_body_user["username"]
    if "password" in request_body_user:
        chosen_user.password = request_body_user["password"]
    if "email" in request_body_user:
        chosen_user.email = request_body_user["email"]
    db.session.commit()
    return jsonify(request_body_user), 200

@users.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    chosen_user = User.query.get(user_id)
    if chosen_user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(chosen_user)
    db.session.commit()
    return jsonify("User successfully deleted"), 200

@users.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    user_favorites = Favorites.query.filter_by(user_id=user_id).all()
    if not user_favorites:
        raise APIException('User has no favorites', status_code=404)
    serialized_favorites = [favorite.serialize() for favorite in user_favorites]
    return jsonify(serialized_favorites), 200

@users.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_character_favorite(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    character = Characters.query.get(character_id)
    if not character:
        raise APIException('Character not found', status_code=404)
    if Favorites.query.filter_by(user_id=user_id, character_id=character_id).first():
        raise APIException('The character is already on the favorites list', status_code=400)
    favorite = Favorites(user_id=user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify("Character added to favorites successfully"), 200

@users.route('/user/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_character_favorite(user_id, character_id):
    favorite = Favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favorite:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite successfully deleted"), 200

@users.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_planet_favorite(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    planet = Planets.query.get(planet_id)
    if not planet:
        raise APIException('Planet not found', status_code=404)
    if Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first():
        raise APIException('The planet is already on the favorites list', status_code=400)
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify("Planet added to favorites successfully"), 200

@users.route('/user/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(user_id, planet_id):
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite successfully deleted"), 200
    
@users.route('/user/<int:user_id>/favorites/starships/<int:starship_id>', methods=['POST'])
def add_starship_favorite(user_id, starship_id):
    user = User.query.get(user_id)
    if not user:
        raise APIException('User not found', status_code=404)
    starship = Starships.query.get(starship_id)
    if not starship:
        raise APIException('Starship not found', status_code=404)
    if Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first():
        raise APIException('The planet is already on the favorites list', status_code=400)
    favorite = Favorites(user_id=user_id, starship_id=starship_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify("Starship added to favorites successfully"), 200

@users.route('/user/<int:user_id>/favorites/starships/<int:starship_id>', methods=['DELETE'])
def delete_starship_favorite(user_id, starship_id):
    favorite = Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if not favorite:
        raise APIException('Favorite not found', status_code=404)
    db.session.delete(favorite)
    db.session.commit()
    return jsonify("Favorite successfully deleted"), 200