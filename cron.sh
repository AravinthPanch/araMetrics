#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

# crontab: 0 5 * * * -> at 5AM every day
# crontab: 0 12 * * * -> at 12PM every day
# crontab: 0 20 * * * -> at 8PM every day

cd /home/aravinth/www/arametrics.aravinth.info/ && /usr/bin/python araMetrics.py 2>&1 | tee output.log
