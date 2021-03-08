#!/bin/sh
# run this script as a root

cp -R ./service-discovery.service /etc/avahi/services/

echo 'service config file copied'

service avahi-daemon restart

echo 'restarting avahi-daemon'