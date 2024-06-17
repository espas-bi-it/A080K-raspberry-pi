#!/bin/bash

apt install libgirepository1.0-dev ffmpeg libavcodec-extra python3-pip

# simple shell script to install required python modules
pip3 install mysql-connector-python python-dotenv pydub lib/nxppy

cp ./chronos_scanner.service /etc/systemd/system/

# reload the daemon, so that it actually finds the chronos_scanner service
systemctl daemon-reload
# start the chronos_scanner service on system startup
systemctl enable chronos_scanner
systemctl start chronos_scanner

cp ./example.env .env
