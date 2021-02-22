# Zeroconf Service Discovery API

This service browses the published zeroconf services in the local network of the server where the service is running and returns the results of the browse through the specified API GET endpoint. A service can be also registered by the API user through the POST method in /services endpoint. Primary usage of this service is to be used on devices such as Raspberry pi which is situated in the local network.


Compatible with: 
  * Avahi
  * Bonjour

## Installing and running on a development server / localhost
1. Clone the repository & navigate to directory and run:
- `git clone git@github.com:Frantisekf/zeroconf-service-discovery-API.git`
- `sudo pip3 install -r requirements.txt`
- `python3 run.py`
3. You're done!


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
    "message": "Success",
    "services": [
        {
            "name": "local-service._companion-link._tcp.local.",
            "addresses": [
                "192.168.178.58",
                "fe80::1893:e42f:9c41:1427"
            ],
            "type": "_companion-link._tcp.local.",
            "port": 59848,
            "domain": "hostname.local.",
            "rpHN": "0a45831c7595",
            "rpFl": "0x20000",
            "rpVr": "220.9",
            "rpHA": "12addsds674b7",
            "rpAD": "ff57c22c0db3",
            "rpHI": "532f1596965c",
            "rpBA": "00:4E:C2:3E:3D:11"
        }
    ]
  }
]
```
### Register a service

`POST /services`
```json
"data": {
    "name": "new service._http._tcp.local.",
        "protocol": "_http._tcp.local.",
        "type": "tcp",
        "port": "7790",
        "domain": "domain.local.",
        "subtype": null
}

```
**Response**

- `201 created` on successful register 

### Lookup single service details

`GET /service/<identifier>`

**Response**

- `404 Not Found` if the service does not exists 
- `200 OK` on success

```json

  {
     "name": "local-service._companion-link._tcp.local.",
     "addresses": [
         "192.168.178.58",
         "fe80::1893:e42f:9c41:1427"
      ],
      "type": "_companion-link._tcp.local.",
      "port": 59848,
      "domain": "hostname.local.",
      "rpHN": "0a45831c7595",
      "rpFl": "0x20000",
      "rpVr": "220.9",
      "rpHA": "12addsds674b7",
      "rpAD": "ff57c22c0db3",
      "rpHI": "532f1596965c",
      "rpBA": "00:4E:C2:3E:3D:11"
   }
```

## TODO
- [ ] run each published service in a separate thread
- [ ] introduce unregister endpoint 
- [ ] improve error handling
- [ ] optimize usage of shelve
- [ ] Service discovery run globally
- [ ] write tests


