# Zeroconf Service Discovery API

This service browses the published zeroconf services in the local network of the server where the service is running and returns the results of the browse through the specified API endpoint. A service can be also registered by the API user through the POST method in /services endpoint.

## Installation


## List all services

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
## Register a service

`POST /services`

**Response**

- `201 created` on successful register 

## Lookup single service details

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
