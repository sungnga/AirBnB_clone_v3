#!/usr/bin/python3
"""City file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """Retrieve all amenities objects of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    r_list = []
    amenities = place.amenities
    for r in amenities:
        r_list.append(r.to_dict())
    return jsonify(r_list)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from_places(place_id, amenity_id):
    """Delete a amenity object by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    if obj not in place.amenities:
        abort(404)
    place.amenities.remove(obj)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenity_places(place_id, amenity_id):
    """Create a amenity object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    obj = storage.get("Amenity", amenity_id)
    if obj is None:
        abort(404)
    if obj in place.amenities:
        return jsonify(obj.to_dict()), 200
    place.amenities.append(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
