import os
from flask import Blueprint, request, jsonify
from utils import APIException
from models import db, Planets


planets =Blueprint('planets', __name__)

@planets.route('/planets', methods=['GET'])
def get_planets():
    planets_query = Planets.query.all()
    results = list(map(lambda item: item.serialize(),planets_query))
    if results == []:
         raise APIException('There are no planets', status_code=404)
    return jsonify(results), 200

@planets.route('/planets/<int:planet_id>', methods=['GET'])
def planet(planet_id):
    planet_query = Planets.query.filter_by(id= planet_id).first()
    if planet_query is None:
         raise APIException('The planet does not exist', status_code=404)
    return jsonify(planet_query.serialize()), 200

@planets.route('/planets', methods=['POST'])
def create_planet():
    request_body_user = request.get_json()
    new_planet = Planets(diameter=request_body_user["diameter"], rotation_period=request_body_user["rotation_period"], orbital_period=request_body_user["orbital_period"], gravity=request_body_user["gravity"], population=request_body_user["population"], climate=request_body_user["climate"], terrain=request_body_user["terrain"], surface_water=request_body_user["surface_water"], name=request_body_user["name"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(request_body_user), 200

@planets.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    chosen_planet = Planets.query.get(planet_id)
    if chosen_planet is None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(chosen_planet)
    db.session.commit()
    return jsonify("Planet successfully deleted"), 200