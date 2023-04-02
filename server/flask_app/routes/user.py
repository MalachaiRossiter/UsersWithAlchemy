from flask import Flask, redirect, jsonify, request
from flask_app import app

@app.route('/', methods=['GET'])
def user():
    data = {"name": "timmy"}
    return jsonify(data)

@app.route('/', methods=['POST'])
def postUser():
    print(request.json['name'], request.json['address'])
    name = request.json['name']
    address = request.json['address']

    data = {"name": name, "address": address}
    return jsonify(data)
