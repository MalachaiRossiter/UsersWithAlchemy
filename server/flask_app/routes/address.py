from flask import Flask, redirect, jsonify, request
from flask_app import app
from flask_app.models.address import Address

@app.route('/address', methods=['GET'])
def get_addresses():
    addresses = Address.get_all()
    data = [address.to_dict() for address in addresses]
    return jsonify(data)

@app.route('/address', methods=['POST'])
def create_address():
    data = request.get_json()
    address_id = Address.create_address(data)
    return_data = address_id.to_dict()
    if not return_data:
        return jsonify({'error': 'Invalid address data'}), 400
    return jsonify({'id': return_data}), 201
    