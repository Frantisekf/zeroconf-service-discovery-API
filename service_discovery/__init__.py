from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import socket
import shelve
import threading

import logging
from time import sleep

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("services")
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
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            self.infos.append(info) 


class ServicesRoute(Resource):
    logging.basicConfig(level=logging.DEBUG)

    def get(self):
        encoding = 'utf-8'
        shelf = get_db()
        keys = list(shelf.keys())
        servicesDiscovered = []

        ip_version = IPVersion.V4Only
        zeroconf = Zeroconf(ip_version=ip_version)

        services = list(ZeroconfServiceTypes.find(zc=zeroconf))

        collector = Collector()
        browser = ServiceBrowser(zeroconf, services, handlers=[collector.on_service_state_change])
        sleep(1)

        for info in collector.infos:
            item = {
                "name": info.name,
                "addresses": info.parsed_addresses(),
                "type": info.type,
                "port": info.port,
                "domain": info.server,
                "properties": {}
            }
            properties = {}
            for key, value in info.properties.items():
                properties[key.decode(encoding)] = value.decode(encoding)
            item['properties'].update(properties)
            servicesDiscovered.append(item)

        return {'message': 'Success', 'services': servicesDiscovered}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('protocol', required=True)
        parser.add_argument('port', required=True)
        parser.add_argument('domain', required=True)
        parser.add_argument('subtype', required=False)
        parser.add_argument('properties',type=dict, required=False)

        # parse arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['name']] = args

        # handle parsing object into zeroconf service
        if args:
            new_service = ServiceInfo(
                args.name,
                args.protocol,
                addresses=[socket.inet_aton("127.0.0.1")],
                port=int(args.port),
                properties=args.properties,
            )
            
            ip_version = IPVersion.V4Only
            zeroconf = Zeroconf(ip_version=ip_version)
            zeroconf.register_service(new_service)

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