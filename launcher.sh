#!/bin/sh
#launcher.sh

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )


cd /
cd home/pi/zeroconf/zeroconf-service-discovery-API
sudo pip3 install -r requirements.txt
sudo python3 run.py
cd /
