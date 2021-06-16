# Start
Hello World

This is the new Raspberry PI scanning system. 

# Requirements 
- Raspbian Buster
- NxpRdLib
- MySQL Database
- Active Internet Connection (only to send Data)

# Installation

## Python Dependencies
All missing dependencies can be installed with the `pip3-install.sh` script. 

## Install chronos_scanner.service
The Script `chronos_scanner.py` is configured as a Service and has to be installed as such.


# After installation
## .env
copy `example.env` and rename it to `.env` and modify it to your needs.

## CronTab
Following scripts require Cron:
- chronos_sender.py
- chronos_deleter.py 

