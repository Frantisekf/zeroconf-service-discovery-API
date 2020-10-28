# Device Discovery Service

Service would gather the MAC addresses of the devices in the local area network of the server where the service is running. Parses the output from the discovery and picks only the supported smart devices based on their MAC addresses. List of these devices can be then fetched through this REST API

## List all devices

**Definition**

`GET /devices`

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

## Lookup single device details

`GET /device/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
  "identifier": "smart-bulp",
  "name": "smart-bulp",
  "device_type": "<type>",
  "controller_gateway": "192.1.68.0.1s"
}
```
