from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import socket
import shelve
import markdown
import os
from flask_cors import CORS, cross_origin
import logging
from time import sleep

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

# Set CORS policy
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize shelf DB
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("services")
    return db

# shelf DB teardown
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Declare Collector object which runs the service discovery browser
class Collector:
    def __init__(self):
        self.infos = []
    
    def on_service_state_change(
        self, zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
    ) -> None:
        if state_change is ServiceStateChange.Added:
            info = zeroconf.get_service_info(service_type, name)
            self.infos.append(info) 


def getHostnameByAddress(addr):
     try:
        return socket.gethostbyaddr(addr)
     except socket.herror:
        return None, None, None

# Define the index route and display readme on the page
@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + '/README.md') as markdown_file:

        readme_content = markdown_file.read()

        return markdown.markdown(readme_content)


class ServicesRoute(Resource):
    logging.basicConfig(level=logging.DEBUG)

    def get(self):
        encoding = 'utf-8'
        shelf = get_db()

        services_discovered = []

        ip_version = IPVersion.V4Only
        zeroconf = Zeroconf(ip_version=ip_version)

        services = list(ZeroconfServiceTypes.find(zc=zeroconf))

        collector = Collector()
        browser = ServiceBrowser(zeroconf, services, handlers=[collector.on_service_state_change])
        sleep(1)

        index = 0
        for info in collector.infos:
            
            ipv4_address = info.parsed_addresses()[0] if info.parsed_addresses()[0:] else ''
            ipv6_address = info.parsed_addresses()[1] if info.parsed_addresses()[1:] else ''
            
            hostname = getHostnameByAddress(ipv4_address)[0] if getHostnameByAddress(ipv4_address)[0:] else '' 

            # parse discovery results into a serializable object
            item = {
                "name": info.name,
                "hostName": hostname,
                "domainName": info.server,
                "addresses": {
                    "ipv4" : ipv4_address,
                    "ipv6": ipv6_address
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
            services_discovered.append(shelf[str(index)])
            index += 1
            
        return {'services': services_discovered}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=False, type=str)
        parser.add_argument('replaceWildcards', required=False, type=bool)
        parser.add_argument('serviceProtocol', required=False, type=str)
        parser.add_argument('type', required=False, type=str)
        parser.add_argument('port', required=False, type=int)
        parser.add_argument('subtype', required=False, type=str)
        parser.add_argument('txtRecords', required=False, type=dict)

        # parse arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[str(args.name)] = args

        if str(args.serviceProtocol).lower() == 'ipv6':
                service_protocol = IPVersion.V6Only
        elif str(args.serviceProtocol).lower() == 'ipv4':
                service_protocol = IPVersion.V4Only
        else: 
             service_protocol = IPVersion.V4Only

        wildcard_name = args.name

        if (args.replaceWildcards):
            wildcard_name = str(args.name).split('.')[0] + ' at ' + socket.gethostname() + '.' + args.type

        if (args.txtRecords == None): 
                args.txtRecords = {}
                
        if (not args.type.endswith('.') or len(str(args.name)) == 0):
                return {'code': 400, 'message': 'Bad parameter in request', 'data': args}, 400
            
        if args:
            new_service = ServiceInfo(
                    args.type,
                    wildcard_name,
                    addresses=[socket.inet_aton("127.0.0.1")],
                    port=args.port,
                    server=str(socket.gethostname() + '.'),
                    properties=args.txtRecords
                
            )
            ip_version = service_protocol
            zeroconf = Zeroconf(ip_version=ip_version)
            zeroconf.register_service(new_service)
            
        return {'code': 201, 'message': 'Service registered', 'data': args}, 201

class ServiceRoute(Resource):
    # Get single service stored in shelf db
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
            return {'code': 404, 'message': 'Device not found', 'data': {}}, 404

        #del shelf[identifier]
        return {'code': 204, 'message': 'Service unregistered', 'data': {shelf[identifier]} }, 204

# Define routes
api.add_resource(ServicesRoute, '/v1/zeroconf')
api.add_resource(ServiceRoute, '/v1/zeroconf/<string:identifier>')