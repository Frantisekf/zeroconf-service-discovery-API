#!/bin/sh

#Defining variable for launcher
launcher=/home/pi/zeroconf-service-discovery-API/launcher.sh
logFile=/home/pi/zeroconf-service-discovery-API//logs/cronlog


#Testing if logs folder exists
# if [ -e "/home/pi/zeroconf/logs" ]
# then
# 	echo "Folder logs already exists"
# else
# 	echo "Creating logs folder.."
# 	mkdir /home/pi/zeroconf/logs
#     cd /home/pi/
# fi


#Adding Zeroconf API to crontab
add_cronjob () { 
    echo "Adding Zeroconf API as a cronjob"
    crontab -l > newcron
    echo "@reboot sh /etc/zeroconf-service-discovery-API/launcher.sh > $logFile 2>&1" >> newcron
    crontab newcron
    rm -f newcron
}

  
crontab -l | grep "$launcher"
if [ $? -eq 0 ]
	then
	    echo "Job already added to crontab"
    else
	    echo "Adding job to crontab..."
	    add_cronjob
fi

if [ -e $logFile ]
then
	echo "File '$logFile' is already created"
else
	echo "Please restart your raspberry pi to start the ZeroConfAPI"
fi