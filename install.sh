#!/bin/bash

add_cronjob () { 
    echo "Adding Zeroconf API as a cronjob"
    crontab -l > newcron
    echo "@reboot sh /home/pi/zeroconf.api.service/launcher.sh >/home/pi/logs/cronlog 2>&1" >> file
    crontab newcron
    rm -f newcron
}

dir=/home/pi/logs

if [ ! -d $dir ]; then
    mkdir $dir
fi

add_cronjob()

echo "please restart your raspberry pi to start the ZeroConfAPI"
