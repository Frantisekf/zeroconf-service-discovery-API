import sys
import os
import time
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import socket
import shelve

import argparse
import logging
from time import sleep
from typing import cast

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("services.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class Collector:
    def __init__(self):
        self.infos = []

    def on_service_state_change(
        self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
    ) -> None:
        print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
    
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            print("Info from zeroconf.get_service_info: %r" % (info))
            if info:
                addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_addresses()]
                print("  Addresses: %s" % ", ".join(addresses))
                print("  Weight: %d, priority: %d" % (info.weight, info.priority))
                print("  Server: %s" % (info.server,))
                if info.properties:
                    print("  Properties are:")
                    for key, value in info.properties.items():
                        print("    %s: %s" % (key, value))
                else:
                    print("  No properties")
            self.infos.append(info)  # <--------------------------------


class ServicesRoute(Resource):
    logging.basicConfig(level=logging.DEBUG)

    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        servicesDiscovered = []

        ip_version = IPVersion.V4Only
        zeroconf = Zeroconf(ip_version=ip_version)

        services = list(ZeroconfServiceTypes.find(zc=zeroconf))

        collector = Collector()
        browser = ServiceBrowser(zeroconf, services, handlers=[collector.on_service_state_change])
        time.sleep(10)


        for key in collector.infos:
            servicesDiscovered.append(shelf[key])

        return {'message': 'Success', 'services': servicesDiscovered}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('protocol', required=True)
        parser.add_argument('type', required=True)
        parser.add_argument('port', required=True)
        parser.add_argument('subtype', required=False)

        # parse arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['identifier']] = args

        # handle parsing object into zeroconf service

        if args:
            info = ServiceInfo(
                shelf['name'],
                shelf['protocol'],
                addresses=[socket.inet_aton("127.0.0.1")],
                port=shelf['port']
            )
            
            zeroconf = Zeroconf(IPVersion.V4Only)
            zeroconf.register_service(info)
        
        return {'message': 'Service published', 'data': args}, 201


# Get single service stored in shelf db
class ServiceRoute(Resource):
    def get(self, identifier):
        shelf = get_db()

        if not (identifier in shelf):
            return {'message': 'Service not found', 'service': {}}, 404

        return {'message': 'Service found', 'data': shelf[identifier]}, 200


api.add_resource(ServicesRoute, '/services')
api.add_resource(ServiceRoute, '/service/<string:identifier>')