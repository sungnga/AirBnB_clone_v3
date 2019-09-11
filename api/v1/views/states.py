#!/usr/bin/python3
"""State file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get():
    """Retrieve all state objects"""
    # l = []
    # for obj in storage.all("State").values():
    #     l.append(obj.to_dict())
    l = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(l)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_by_id(state_id):
    """Retrieve a state object by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    """Delete a state object by id"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    storage.reload()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """Create a state object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in request.get_json():
        return jsonify({'error': 'Missing name'}), 400
    name = request.get_json().get('name')
    obj = State(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id):
    """Updates a state object"""
    if not request.get_json():
        return jsonify({'error': 'Not a JSON'}), 400
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(obj, k, v)
    return jsonify(obj.to_dict())
