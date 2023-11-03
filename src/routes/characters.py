import os
from flask import Blueprint, request, jsonify
from utils import APIException
from models import db, Characters


characters =Blueprint('characters', __name__)

@characters.route('/characters', methods=['GET'])
def get_characters():
    characters_query = Characters.query.all()
    results = list(map(lambda item: item.serialize(),characters_query))
    if results == []:
         raise APIException('There are no characters', status_code=404)
    return jsonify(results), 200

@characters.route('/characters/<int:character_id>', methods=['GET'])
def character(character_id):
    character_query = Characters.query.filter_by(id= character_id).first()
    if character_query is None:
         raise APIException('The character does not exist', status_code=404)
    return jsonify(character_query.serialize()), 200

@characters.route('/characters', methods=['POST'])
def create_character():
    request_body_user = request.get_json()
    new_character = Characters(height=request_body_user["height"], mass=request_body_user["mass"], hair_color=request_body_user["hair_color"], skin_color=request_body_user["skin_color"], eye_color=request_body_user["eye_color"], birth_year=request_body_user["birth_year"], gender=request_body_user["gender"], name=request_body_user["name"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify(request_body_user), 200

@characters.route('/characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    chosen_character = Characters.query.get(character_id)
    if chosen_character is None:
        raise APIException('Character not found', status_code=404)
    db.session.delete(chosen_character)
    db.session.commit()
    return jsonify("Character successfully deleted"), 200