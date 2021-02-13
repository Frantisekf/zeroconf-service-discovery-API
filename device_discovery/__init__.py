import sys
import os
from flask import Flask, g
from flask_restful import Resource, Api
import shelve


# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("devices.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class Devices(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        devices = []

        for key in devices:
            devices.append(shelf[key])

        return {'message': 'Success', 'data': devices}, 200


class Device(Resource):
    def get(self, identifier):
        shelf = get_db()

        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        return {'message': 'Device found', 'data': shelf[identifier]}, 200


api.add_resource(Devices, '/devices')
api.add_resource(Device, '/device/<string:identifier>')
