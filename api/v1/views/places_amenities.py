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
    if storage_t == 'db':
        amenities = place.amenities
        for r in amenities:
            r_list.append(r.to_dict())
    else:
        amenities = place.amenity_ids
        for ids in amenities:
            amenity = storage.get('Amenity', ids)
            r_list.append(amenity.to_dict())
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
    # if storage_t == 'db':
    #     l = place.amenities
    #     if obj not in l:
    #         abort(404)
    #     del l[l.index(obj)]
    # else:
    #     l = place.amenity_ids
    #     if amenity_id not in l:
    #         abort(404)
    #     del l[l.index(amenity_id)]
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

    if storage_t == 'db':
        if obj in place.amenities:
            return jsonify(place.to_dict())
        place.amenities.append(obj)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(place.to_dict())
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(place.to_dict()), 201
