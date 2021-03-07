from flask import Flask, g
from flask.globals import request
from flask_restful import Resource, Api, reqparse
import socket
import shelve
import threading

from flask_cors import CORS, cross_origin
import logging
from time import sleep

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})

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
        servicesDiscovered = []

        ip_version = IPVersion.V4Only
        zeroconf = Zeroconf(ip_version=ip_version)

        services = list(ZeroconfServiceTypes.find(zc=zeroconf))

        collector = Collector()
        browser = ServiceBrowser(zeroconf, services, handlers=[collector.on_service_state_change])
        sleep(1)

        for info in collector.infos:
            
            index = 0
            ipv4Address = info.parsed_addresses()[0] if info.parsed_addresses()[0] is not None else ''
            ipv6Address = info.parsed_addresses()[1] if info.parsed_addresses()[1] is not None else ''
            hostname = socket.gethostbyaddr(ipv4Address)[0] if socket.gethostbyaddr(ipv4Address)[0] is not None else ''

            item = {
                "name": info.name,
                "hostName": hostname,
                "domainName": info.server,
                "addresses": {
                    "ipv4" : ipv4Address,
                    "ipv6": ipv6Address
                },
                "service": {
                    "type": info.type, 
                    "port": info.port,
                    "txtRecord": {}
                },
            }

            properties = {}
            for key, value in info.properties.items():
                properties[key.decode(encoding)] = value.decode(encoding)
            item['service']['txtRecord'].update(properties)
            shelf[str(index)] = item
            servicesDiscovered.append(shelf[str(index)])
            index += 1
            
        return {'message': 'Success', 'services': servicesDiscovered}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',required=False, type=int )
        parser.add_argument('name', required=False, type=str)
        parser.add_argument('replaceWildcards', required=False, type=bool)
        parser.add_argument('serviceProtocol', required=False, type=bool)
        parser.add_argument('protocol', required=False, type=str)
        parser.add_argument('port', required=False, type=int)
        parser.add_argument('subtype', required=False, type=str)
        parser.add_argument('properties', required=False, type=dict)

        # parse arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['id']] = args

        if args['serviceProtocol'].lower() == 'ipv6':
                serviceProtocol = IPVersion.V6Only
        elif args['serviceProtocol'].lower() == 'ipv4':
                serviceProtocol = IPVersion.V4Only
        else: 
             serviceProtocol = IPVersion.V4Only

        #set default name 
        wildcardName = args.name

        if (args['replaceWildcards']):
            wildcardName = args.name + ' at ' + socket.gethostname()
            
        
        # handle parsing object into zeroconf service
        if args:
            new_service = ServiceInfo(
                str(wildcardName),
                args.protocol,
                addresses=[socket.inet_aton("127.0.0.1")],
                port=args.port,
                properties=args.properties,
            )
            ip_version = serviceProtocol
            zeroconf = Zeroconf(ip_version=ip_version)
            zeroconf.register_service(new_service)

            # add id as a key to service and store in db

        return {'message': 'Service registered', 'data': args}, 201


# Get single service stored in shelf db
class ServiceRoute(Resource):
    def get(self, identifier):
        shelf = get_db()

        if not (identifier in shelf):
            return {'message': 'Service not found', 'service': {}}, 404

        return {'message': 'Service found', 'data': shelf[identifier]}, 200
    
    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        # if the key.name equals the name of the service running in thread
        # kill the thread 
        if not (identifier in shelf):
            return {'message': 'Device not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204


api.add_resource(ServicesRoute, '/services')
api.add_resource(ServiceRoute, '/service/<string:identifier>')