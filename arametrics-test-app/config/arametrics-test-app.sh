#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

app_root='/home/aravinth/www/apps'
app_name='arametrics-test-app'
aracloud_root='/var/www/aracloud'
run_command='/usr/bin/python arametrics_test_app.py'

cd $app_root/$app_name/app/ && $run_command 2>&1 | tee $aracloud_root/logs/$app_name.log
