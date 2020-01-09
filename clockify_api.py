#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

import requests
import pprint
import json
import datetime

from config import *


def clockify_api_get_tasks():
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/', headers=CLOCKFIFY_HEADER)
    tasks = r.json()
    # pprint.pprint(tasks)

    for task in tasks:
        print(task['timeInterval']['duration'])


def clockify_api_set_tasks():
    task = {
        "name": "Task from API",
        "projectId": CLOCKFIFY_PROJECT_ID
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/projects/' + CLOCKFIFY_PROJECT_ID + '/tasks/', headers=CLOCKFIFY_HEADER, data=json.dumps(task))

    print r.text


def clockify_api_set_time_entry(task_description, project_id):
    now = datetime.datetime.now()
    start = datetime.datetime(now.year, now.month, now.day, 00, 00, 01).isoformat() + 'Z'
    end = datetime.datetime(now.year, now.month, now.day, 00, 00, 02).isoformat() + 'Z'

    time_entry = {
        "start": start,
        "end": end,
        "description": task_description,
        "projectId": project_id
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/',
        headers=CLOCKFIFY_HEADER, data=json.dumps(time_entry))

    print r.text

def clockify_api_set_time_entries(tasks_array):
    for task in tasks_array:
        clockify_api_set_time_entry(task['TODO'], task['PROJECT_ID'])
