#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import pprint
import datetime
import pickle
import os.path

from config import *

metrics_table = {
    'tasks': {'done': 0, 'in-progress': 0, 'incomplete': 0},
    'events': {'done': 0, 'in-progress': 0, 'incomplete': 0}
}


def google_api_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def google_api_retrieve_cal_events(cal_service, calendar_id):
    "Call the Calendar API"

    now = datetime.datetime.now()

    # 'Z' indicates UTC time
    time_min = datetime.datetime(now.year, now.month, now.day, 0).isoformat() + 'Z'
    time_max = datetime.datetime(now.year, now.month, now.day, 23).isoformat() + 'Z'

    events_result = cal_service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                                              singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def google_api_print_cal_events(cal_events):
    if not cal_events:
        print('No upcoming cal_events found.')
    for event in cal_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def google_api_get_cal_list(cal_service):
    "Get list of all the calendars"

    cal_list = cal_service.calendarList().list(pageToken=None).execute()
    pprint.pprint(cal_list)


def google_api_get_tasks_count(cal_service):
    "Count number of tasks"

    cal_events = google_api_retrieve_cal_events(cal_service, cal_tasks['done'])
    print('cal_events')
    google_api_print_cal_events(cal_events)

    cal_events_count = 0
    for event in cal_events:
        cal_events_count = cal_events_count + 1
    print('cal_event_count')
    print(cal_events_count)

    metrics_table['tasks']['done'] = cal_events_count
    pprint.pprint(metrics_table)


def google_api_cal_events_parser(cal_events):
    # google_api_print_cal_events(cal_events)

    tasks = []

    if not cal_events:
        return None
    for event in cal_events:
        task_str_array = event['summary'].split('#')
        if len(task_str_array) > 2:
            task = {
                'project': task_str_array[1],
                'todo': task_str_array[2],
                'tag': task_str_array[3],
            }
            tasks.extend([task])

    pprint.pprint(tasks)
    return tasks


def google_api_get_todo_events(cal_service):
    "Get all today's events which have to be schduled as tasks"
    cal_events = google_api_retrieve_cal_events(cal_service, cal_tasks['todo'])
    return google_api_cal_events_parser(cal_events)
