#!/bin/bash

# simple shell scritp to install required python modules
pip3 install pygame mysql-connector-python python-dotenv nxppy

mv chronos_scanner.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable chronos_scanner
systemctl start chronos_scanner

copy example.env .env