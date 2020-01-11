#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : This contains the functions to get and set time entries from Clockify via REST API

import requests
import pprint
import json
import datetime
import logging
from pprint import pformat

from config import *


def clockify_api_get_current_date_time_entries():
    "Get time entries for the given day. Clockify API is not filtering with &start=' + time_entry_start+ '&end=' + time_entry_end"

    # GET request
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/user/' + CLOCKFIFY_USER_ID + '?limit=30', headers=CLOCKFIFY_HEADER)
    time_entries = r.json()

    # pprint.pprint(time_entries)
    logging.debug('clockify_api_get_current_date_time_entries : time_entries : \n %s', pformat(time_entries))

    # Filter them by date
    current_date_time_entries = []
    for time_entry in time_entries['timeEntriesList']:
        time_entry_date_time = datetime.datetime.strptime(time_entry['timeInterval']['start'], '%Y-%m-%dT%H:%M:%SZ')

        if time_entry_date_time.date() == current_date:
            current_date_time_entries.extend([time_entry])

    logging.debug('clockify_api_get_current_date_time_entries : current_date_time_entries : \n %s',
                  pformat(current_date_time_entries))
    return current_date_time_entries


def clockify_api_set_time_entry(task_todo, taks_project_id, task_tag_id, cal_date):
    "Create a time entry for the given project, tag and date"

    time_entry_start = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 01).isoformat() + 'Z'
    time_entry_end = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 02).isoformat() + 'Z'

    # Request body
    time_entry = {
        "start": time_entry_start,
        "end": time_entry_end,
        "description": task_todo,
        "projectId": taks_project_id,
        "tagIds": [task_tag_id],
    }

    # POST request
    response = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/',
        headers=CLOCKFIFY_HEADER, data=json.dumps(time_entry))

    logging.debug('clockify_api_set_time_entry : response : \n %s', pformat(response.text))


def clockify_api_set_time_entries(tasks_array, cal_date):
    "Create time entries for the given list of tasks and date "

    # Set current date and get time entries for the given date
    global current_date
    current_date = cal_date
    current_date_time_entries = clockify_api_get_current_date_time_entries()

    if len(tasks_array) is 0:
        print('No tasks are found in the calendar')
        return

    # Check if the task is already entered as a time entry.
    tasks_already_entered_cnt = 0
    for task in tasks_array:
        is_task_already_entered = 0

        # Sometimes there are multiple entries of same task.
        for time_entry in current_date_time_entries:
            if task['TODO'] == time_entry['description']:
                is_task_already_entered = is_task_already_entered + 1
            else:
                is_task_already_entered = is_task_already_entered + 0

        # If task is not already entered as a time entry, create one.
        if is_task_already_entered == 0:
            clockify_api_set_time_entry(task['TODO'], task['PROJECT_ID'], task['TAG_ID'], cal_date)
            tasks_already_entered_cnt = tasks_already_entered_cnt + 1

    if tasks_already_entered_cnt is 0:
        logging.error('clockify_api_set_time_entries : No tasks for time entry')
