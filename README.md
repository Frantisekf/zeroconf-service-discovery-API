![Github Actions Pipeline](https://github.com/Frantisekf/zeroconf-service-discovery-API/actions/workflows/python-app.yml/badge.svg)


# Zeroconf Service Discovery API

This service browses the published zeroconf services in the local network of the server where the service is running and returns the results of the browse through the specified API GET endpoint. A service can be also registered by the API user through the POST method in /services endpoint.


Compatible with: 
  * Avahi
  * Bonjour

## Installing and running on a development server / localhost
1. Clone the repository & navigate to directory and run:
- `git clone git@github.com:Frantisekf/zeroconf-service-discovery-API.git`
- `sudo pip3 install -r requirements.txt`
- `python3 run.py`
3. You're done!

## Deploying
To deploy the Zeroconf service/API on a device such as Rpi. make sure you have avahi installed on the device
1. Run the launcher.sh script by running `sh launcher.sh`.

   This will set the launch of the API/Zeroconf service on the start of the system.
2. Run `sudo sh setup-avahi-service.sh` to publish the API as a zeroconf service in the local network.   


Note: you can configure the `port`, `hostname` and set`DEBUG` level in the `.env` file


## Installing and running in a docker container
1. Install Docker.
- `curl -sSL https://get.docker.com | sh`
2. Add permission to user.
- `sudo usermod -aG docker <user>`
3. Install additional dependencies.
- `sudo apt-get install -y libffi-dev libssl-dev`
- `sudo apt-get install -y python3 python3-pip`
- `sudo apt-get remove python-configparser`
4. Install docker compose.
- `sudo pip3 -v install docker-compose`
5. After finishing docker installation make sure to logout and login to your system user account.
6. Navigate to a folder of your choice and clone this repository
- `git clone git@github.com:Frantisekf/zeroconf-service-discovery-API.git`
8. After cloning the repository step into it and build the application:
- `cd zeroconf-service-discovery`
- `docker-compose build`
9. To run the application, run this command from the zeroconf-service-discovery-API directory:
- `docker-compose up`
10. You're done!



Note: you can configure the `port`, `hostname` and set`DEBUG` level in the `.env` file

## API Usage
### List all services

**Definition**

`GET /services`

**Response**

- `200 OK` on success

```json
[
  {
            "name": "Fran's MacBook Pro._rfb._tcp.local.",
            "hostName": "frans-mbp.fritz.box",
            "domainName": "Frans-MacBook-Pro.local.",
            "addresses": {
                "ipv4": "192.168.178.58",
                "ipv6": "fe80::1893:e42f:9c41:1427"
            },
            "service": {
                "type": "_rfb._tcp.local.",
                "port": 5900,
                "txtRecord": {}
            }
        },
        {
            "name": "Fran's MacBook Pro._flametouch._tcp.local.",
            "hostName": "frans-mbp.fritz.box",
            "domainName": "Frans-MacBook-Pro.local.",
            "addresses": {
                "ipv4": "192.168.178.58",
                "ipv6": "fe80::1893:e42f:9c41:1427"
            },
            "service": {
                "type": "_flametouch._tcp.local.",
                "port": 1812,
                "txtRecord": {}
            }
        },
]
```
### Register a service

`POST /services`
```json
{
     "name": "New test service._http._tcp.local.",
     "replaceWildcards": false,
     "serviceProtocol": "any",
     "protocol": "_http._tcp.local.",
     "port": 7790
}

```
**Response**

- `201 created` on successful register 


## TODO
- [x] run each published service in a separate thread
- [x] introduce unregister endpoint 
- [x] improve error handling
- [x] optimize usage of shelve
- [ ] write tests
- [ ] Logging 


