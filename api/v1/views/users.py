#!/usr/bin/python3
"""User file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    """Retrieve all state objects"""
    l = [obj.to_dict() for obj in storage.all("User").values()]
    return jsonify(l)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """Retrieve a user object by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user object by id"""
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    d = request.get_json()
    obj = User(**d)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a user object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    obj = storage.get("User", user_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
