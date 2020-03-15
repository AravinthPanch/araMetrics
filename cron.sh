#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

cd /home/aravinth/www/arametrics.aravinth.info/html/ && /usr/bin/python araMetrics.py 2>&1 | tee output.log
