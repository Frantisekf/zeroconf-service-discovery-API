#!/bin/sh
#uninstall.sh

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
launcher="${parent_path}/launcher.sh"
logFile="${parent_path}/logs/cronlog"

remove_cronjob () { 
    echo "Removing Zeroconf API cronjob"
    crontab -l > newcron
    sed -i 's/\@reboot.*\(launcher.sh\).*/test/g' newcron
    crontab newcron
    rm -f newcron
}



echo "Are you sure you want to proceed with uninstallation? (Y/N)"
read ANSWER

case $ANSWER in

	Y|y)
		echo "Proceeding with uninstallation ..."
		sleep 1
		check_process remove_cronjob
		echo "Removing all files and folders"
		rm -R $parent_path  2>&1 > /dev/null
		echo "Uninstallation completed!"
		
	N|n);;
		echo "Uninstallation aborted!";;
	
	*);;
esac