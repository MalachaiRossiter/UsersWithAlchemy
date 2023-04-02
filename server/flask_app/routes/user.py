from flask import Flask, redirect, jsonify, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.address import Address

@app.route('/user', methods=['GET'])
def get_users():
    users = User.get_all()
    data = [user.to_dict() for user in users]
    return jsonify(data)

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.get_id(id)
    data = user.to_dict()
    return jsonify(data)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = User.create_user(data)
    return_data = user_id.to_dict()
    if not return_data:
        return jsonify({'error': 'Invalid user data'}), 400
    return jsonify({'id': return_data}), 201

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user_id = User.update_user(data, id)
    return_data = user_id.to_dict()
    if not return_data:
        return jsonify({'error': 'Invalid user data'}), 400
    return jsonify({'id': return_data}), 201

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.delete_user(id)
    return jsonify(user)
