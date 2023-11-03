import os
from flask import Blueprint, request, jsonify
from utils import APIException
from models import db, Starships


starships =Blueprint('starships', __name__)

@starships.route('/starhips', methods=['GET'])
def get_starships():
    starhips_query = Starships.query.all()
    results = list(map(lambda item: item.serialize(), starhips_query))
    if results == []:
         raise APIException('There are no starships', status_code=404)
    return jsonify(results), 200

@starships.route('/starships/<int:starship_id>', methods=['GET'])
def starship(starship_id):
    starship_query = Starships.query.filter_by(id= starship_id).first()
    if starship_query is None:
        raise APIException('The starship does not exist', status_code=404)
    return jsonify(starship_query.serialize()), 200 

@starships.route('/starships', methods=['POST'])
def create_starship():
    request_body_user = request.get_json()
    new_starship = Starships(model=request_body_user["model"], starship_class=request_body_user["starship_class"], manufacturer=request_body_user["manufacturer"], cost_in_credits=request_body_user["cost_in_credits"], length=request_body_user["length"], crew=request_body_user["crew"], passengers=request_body_user["passengers"], max_atmosphering_speed=request_body_user["max_atmosphering_speed"], hyperdrive_rating=request_body_user["hyperdrive_rating"], MGLT=request_body_user["MGLT"], cargo_capacity=request_body_user["cargo_capacity"], consumables=request_body_user["consumables"], name=request_body_user["name"])
    db.session.add(new_starship)
    db.session.commit()
    return jsonify(request_body_user), 200

@starships.route('/starships/<int:starship_id>', methods=['DELETE'])
def delete_starship(starship_id):
    chosen_starship = Starships.query.get(starship_id)
    if chosen_starship is None:
        raise APIException('Starship not found', status_code=404)
    db.session.delete(chosen_starship)
    db.session.commit()
    return jsonify("Starship successfully deleted"), 200