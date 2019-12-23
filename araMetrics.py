#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

from __future__ import print_function
import json
import pprint
import datetime
import pickle
import os.path
from config import *
from api import google_api_login


def retrieve_cal_events(cal_service, calendar_id):
    "Call the Calendar API"

    # 'Z' indicates UTC time
    now = datetime.datetime(2019,12,22).isoformat() + 'Z'
    events_result = cal_service.events().list(calendarId=calendar_id, timeMin=now,
                                              singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def print_cal_events(cal_events):
    if not cal_events:
        print('No upcoming cal_events found.')
    for event in cal_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def get_cal_list(cal_service):
    "Get list of all the calendars"

    cal_list = cal_service.calendarList().list(pageToken=None).execute()
    pprint.pprint(cal_list)


def get_tasks_count(cal_service):
    "Count number of tasks"

    cal_events = retrieve_cal_events(cal_service, cal_tasks['done'])
    print_cal_events(cal_events)


def main():
    cal_service = google_api_login()
    get_tasks_count(cal_service)


if __name__ == '__main__':
    main()
