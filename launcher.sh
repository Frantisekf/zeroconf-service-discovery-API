#!/bin/sh
#launcher.sh

parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

echo $parent_path

cd /
cd $parent_path
sudo pip3 install -r requirements.txt
sudo python3 run.py
cd /
