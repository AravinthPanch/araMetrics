#!/usr/bin/env python

# description : araMetrics is a personal impact measurement system to track metrics such as tasks, events, contacts, expenses, purchases, travels, behaviour, etc
# author : Aravinth Panch

from __future__ import print_function
import datetime
import pickle
import os.path
from config import *
from api import google_api_login


def retrieve_cal_events(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()

    events = events_result.get('items', [])

    # print results
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def main():
    service = google_api_login()
    retrieve_cal_events(service)


if __name__ == '__main__':
    main()
