#!/usr/bin/python3
""" Artisans API Blueprint """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.city import City
from models.artisan import Artisan
from models import storage
import json


@app_views.route('/artisans', methods=['GET'], strict_slashes=False)
def get_all_artisans():
    """ returns all astisans """
    artisans = []
    for artisan in storage.all(Artisan).values():
        artisans.append(artisan.to_dict())
    return jsonify(artisans)


@app_views.route('/artisans/<artisan_id>', methods=['GET'], strict_slashes=False)
def get_artisan(artisan_id):
    """ returns the artisan with the specified id """
    retrieved_artisan = storage.get(Artisan, artisan_id)
    if retrieved_artisan:
        return jsonify(retrieved_artisan.to_dict())
    else:
        abort(404)


@app_views.route('/artisans/<artisan_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_artisan(artisan_id):
    """ deletes an artisan with the sepcified id """
    retrieved_artisan = storage.get(Artisan, artisan_id)
    if retrieved_artisan:
        storage.delete(retrieved_artisan)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/artisans', methods=['POST'], strict_slashes=False)
def create_artisan(city_id):
    """ creates a new artisan shop in a city """
    # check if the city exists
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    # check if data is a json
    try:
        artisan_dict = json.loads(request.data)
    except json.JSONDecodeError:
        abort(400, "Not a JSON")

    # check again if data is json, for good measure
    artisan_dict = request.get_json()
    if not artisan_dict:
        abort(400, "Not a JSON")

    # make sure all the attributes (that can't be null) exist
    if "name" not in artisan_dict.keys():
        abort(400, "Missing name")
    
    if "description" not in artisan_dict.keys():
        abort(400, "Missing description")
    
    if "email" not in artisan_dict.keys():
        abort(400, "Missing email")
    
    if "password" not in artisan_dict.keys():
        abort(400, "Missing password")

    # create and save the new Artisan instance
    new_artisan = Artisan(**artisan_dict)
    storage.new(new_artisan)
    storage.save()

    return make_response(jsonify(new_artisan.to_dict()), 201)


@app_views.route('/artisans/<artisan_id>', methods=['PUT'], strict_slashes=False)
def update_artisan(artisan_id):
    """ updates an artisan """
    artisan = storage.get(Artisan, artisan_id)

    # make sure the instance exists first
    if not artisan:
        abort(404)

    # check if data is json
    try:
        artisan_dict = json.loads(request.data)
    except json.JSONDecodeError:
        abort(400, "Not a JSON")

    artisan_dict = request.get_json()

    if not artisan_dict:
        abort(400, "Not a JSON")

    # update the instance
    for key, value in artisan_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(artisan, key, value)

    storage.save()

    return make_response(jsonify(artisan.to_dict()), 200)
