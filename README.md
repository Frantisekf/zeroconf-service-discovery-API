# Zeroconf Service Discovery API

This service browses the published zeroconf services in the local network of the server where the service is running and returns the results of the browse through the specified API GET endpoint. A service can be also registered by the API user through the POST method in /services endpoint. Primary usage of this service is to be used on devices such as Raspberry pi which is situated in the local network.

## Installing and running a development server on Rpi
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

## API Usage
### List all services

**Definition**

`GET /services`

**Response**

- `200 OK` on success

```json
[
  {
    "identifier": "smart-bulp",
    "name": "smart-bulp",
    "device_type": "<type>",
    "controller_gateway": "192.1.68.0.1"
  },
  {
    "identifier": "smart-tv",
    "name": "smart-tv",
    "device_type": "<type>",
    "controller_gateway": "192.168.0.3"
  }
]
```
### Register a service

`POST /services`

**Response**

- `201 created` on successful register 

### Lookup single service details

`GET /service/<identifier>`

**Response**

- `404 Not Found` if the service does not exists 
- `200 OK` on success

```json
{
  "identifier": "smart-bulp",
  "name": "smart-bulp",
  "device_type": "<type>",
  "controller_gateway": "192.1.68.0.1s"
}
```
