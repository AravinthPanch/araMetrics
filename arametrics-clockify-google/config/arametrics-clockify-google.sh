#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

# crontab: 0 5 * * * -> at 5AM every day
# crontab: 0 12 * * * -> at 12PM every day
# crontab: 0 20 * * * -> at 8PM every day

app_root='/home/aravinth/www/apps'
app_name='arametrics-clockify-google'
aracloud_root='/var/www/aracloud'
run_command='/usr/bin/python arametrics_clockify_google.py'

cd $app_root/$app_name/app/ && $run_command 2>&1 | tee $aracloud_root/logs/$app_name.log
