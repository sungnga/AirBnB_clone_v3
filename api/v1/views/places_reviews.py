#!/usr/bin/python3
"""City file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all review objects of a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    r_list = []
    for r in reviews:
        r_list.append(r.to_dict())
    return jsonify(r_list)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review_by_id(review_id):
    """Retrieve a review object by id"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review object by id"""
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a review object"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in request.get_json():
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", request.get_json().get('user_id'))
    if user is None:
        abort(404)
    user_id = request.get_json().get('user_id')
    if 'text' not in request.get_json():
        return jsonify({'error': 'Missing text'}), 400
    text = request.get_json().get('text')
    obj = Review(text=text, place_id=place_id, user_id=user_id)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a review object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
