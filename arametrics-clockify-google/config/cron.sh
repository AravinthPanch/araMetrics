#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

# crontab: 0 5 * * * -> at 5AM every day
# crontab: 0 12 * * * -> at 12PM every day
# crontab: 0 20 * * * -> at 8PM every day

cd /home/aravinth/www/apps.aravinth.info/arametrics-clockify-google/app/ && /usr/bin/python arametrics_clockify_google.py 2>&1 | tee logs/output.log
