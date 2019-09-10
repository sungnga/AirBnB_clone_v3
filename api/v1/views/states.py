#!/usr/bin/python3
"""State file for views module"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
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


@app_views.errorhandler(400)
def resource_not_found(e):
    return jsonify(error=str(e)), 400


@app_views.route('/states', methods=['POST'])
def create():
    """Create a state object"""
    if not request.json:
        abort(400, description='Not a JSON')
    if not 'name' in request.get_json():
        abort(400, description='Not a JSON')
    name = request.get_json().get('name')
    obj = State(name=name)
    obj.save()
    return jsonify(obj.to_dict()), 201
