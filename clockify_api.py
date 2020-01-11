#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

import requests
import pprint
import json
import datetime
import logging
from pprint import pformat

from config import *


def clockify_api_get_today_time_entries():
    "Get time entries for the given day. Clockify API is not filtering with &start=' + time_entry_start+ '&end=' + time_entry_end"

    # GET request
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/user/' + CLOCKFIFY_USER_ID + '?limit=30', headers=CLOCKFIFY_HEADER)
    time_entries = r.json()

    # pprint.pprint(time_entries)
    logging.debug('clockify_api_get_today_time_entries : time_entries : \n %s', pformat(time_entries))

    # Filter them by date
    today_time_entries = []
    for time_entry in time_entries['timeEntriesList']:
        time_entry_date_time = datetime.datetime.strptime(time_entry['timeInterval']['start'], '%Y-%m-%dT%H:%M:%SZ')

        if time_entry_date_time.date() == current_date:
            today_time_entries.extend([time_entry])

    logging.warning('clockify_api_get_today_time_entries : today_time_entries : \n %s', pformat(today_time_entries))
    return today_time_entries


def clockify_api_set_tasks():
    task = {
        "name": "Task from API",
        "projectId": CLOCKFIFY_PROJECT_ID
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/projects/' + CLOCKFIFY_PROJECT_ID + '/tasks/', headers=CLOCKFIFY_HEADER, data=json.dumps(task))

    print r.text


def clockify_api_set_time_entry(task_todo, taks_project_id, task_tag_id, cal_date):

    time_entry_start = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 01).isoformat() + 'Z'
    time_entry_end = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 02).isoformat() + 'Z'

    time_entry = {
        "start": time_entry_start,
        "end": time_entry_end,
        "description": task_todo,
        "projectId": taks_project_id,
        "tagIds": [task_tag_id],
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/',
        headers=CLOCKFIFY_HEADER, data=json.dumps(time_entry))

    print r.text


def clockify_api_set_time_entries(tasks_array, cal_date):
    global current_date
    current_date = cal_date
    today_time_entries = clockify_api_get_today_time_entries()

    if len(tasks_array) is 0:
        print('No tasks are found in the calendar')
        return

    tasks_entered_cnt = 0

    # check if the task is already a time entry, sometimes there are multiple entries of same task.
    for task in tasks_array:
        is_task_already_entered = 0

        for time_entry in today_time_entries:

            if task['TODO'] == time_entry['description']:
                is_task_already_entered = is_task_already_entered + 1
            else:
                is_task_already_entered = is_task_already_entered + 0

        if is_task_already_entered == 0:
            # clockify_api_set_time_entry(task['TODO'], task['PROJECT_ID'], task['TAG_ID'], cal_date)
            tasks_entered_cnt = tasks_entered_cnt + 1

    if tasks_entered_cnt is 0:
        print('No tasks for time entry')
