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
 
1. Make sure you have git version control installed. if not run `sudo apt-get install git` 
2. navigate to your home directory on raspberry pi should be `/home/pi/`
And create directory for logs using `sudo mkdir logs` 
3. Type in `sudo crontab -e` to open a the crontab config file
4. in the crontab config file add the following line to the bottom of the file `@reboot sh /home/pi/zeroconf.api.service/launcher.sh  >/home/pi/logs/cronlog 2>&1`
Make sure that the directory path leads to launcher.sh file in the project folder /home/pi/zeroconf.api.service/launcher.sh.
5. Restart the Rpi using the command `sudo reboot`
6. After the restart type the command `cat /home/pi/logs/cronlog` to see if the log is populated with logging output from API
7. You can configure the port to be used by the API in `/zeroconf.api.service/.env` file



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
     "name": "new2 test service._http._tcp.local.",
     "replaceWildcards": false,
     "serviceProtocol": "any",
     "service": {
        "type": "_http._tcp.local.",
        "port": 7790,
        "txtRecord": {
            "property1": "prop",
            "property2": "prop",
            "property3": "prop"
        }
     }
}

```
**Response**

- `201 created` on successful register 


