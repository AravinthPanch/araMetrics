#!/bin/bash

# Description:   Automatic deployment of websites on araCloud
# Author:        Aravinth Panch

app_root='/home/aravinth/www/apps'
app_name='arametrics-clockify-google'
aracloud_root='/var/www/aracloud'
run_command='/usr/bin/pip install -r requirements.txt'

cd $app_root/$app_name/app/ && $run_command 2>&1 | tee -a $aracloud_root/logs/apps-$app_name.log
