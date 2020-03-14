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


def clockify_api_get_current_date_time_entries(cal_date, workspace_id):
    "Get time entries for the given day. Clockify API is not filtering with &start=' + time_entry_start+ '&end=' + time_entry_end"

    # GET request
    # Change the limit for accessing older time entries
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + workspace_id + '/timeEntries/user/' + CLOCKFIFY_USER_ID + '?limit=100', headers=CLOCKFIFY_HEADER)
    time_entries = r.json()

    logging.debug('clockify_api_get_current_date_time_entries : time_entries : \n %s\n', pformat(time_entries))

    # Filter them by date
    current_date_time_entries = []
    for time_entry in time_entries['timeEntriesList']:
        time_entry_date_time = datetime.datetime.strptime(time_entry['timeInterval']['start'], '%Y-%m-%dT%H:%M:%SZ')

        if time_entry_date_time.date() == cal_date:
            current_date_time_entries.extend([time_entry])

    logging.debug('clockify_api_get_current_date_time_entries : current_date_time_entries : \n %s\n',
                  pformat(current_date_time_entries))
    logging.error('clockify_api_get_current_date_time_entries : Found %s Clockify entries on %s', len(current_date_time_entries), cal_date)

    return current_date_time_entries


def clockify_api_set_time_entry(task_todo, taks_project_id, task_tag_id, task_start, task_end, cal_date, workspace_id):
    "Create a time entry for the given project, tag and date"

    # Request body
    time_entry = {
        "start": task_start,
        "end": task_end,
        "description": task_todo,
        "projectId": taks_project_id,
        "tagIds": [task_tag_id],
    }

    # POST request
    response = requests.post(CLOCKFIFY_API + '/workspaces/' + workspace_id + '/timeEntries/',
                             headers=CLOCKFIFY_HEADER, data=json.dumps(time_entry))

    logging.debug('clockify_api_set_time_entry : response : \n %s\n', pformat(response.text))


def clockify_api_set_time_entries(tasks_array, cal_date, workspace_id):
    "Create time entries for the given list of tasks and date "

    # Get time entries for the given date
    current_date_time_entries = clockify_api_get_current_date_time_entries(cal_date, workspace_id)

    if tasks_array is None or len(tasks_array) is 0:
        logging.error('clockify_api_set_time_entries : No tasks are found in the calendar on %s', cal_date)
        return

    if len(current_date_time_entries) is 0:
        logging.error('clockify_api_set_time_entries : No time entries are found in clockify on %s', cal_date)

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
            clockify_api_set_time_entry(task['TODO'], task['PROJECT_ID'], task['TAG_ID'],
                                        task['START'], task['END'], cal_date, workspace_id)
            tasks_already_entered_cnt = tasks_already_entered_cnt + 1
            logging.error('clockify_api_set_time_entries : A task is entered as a time entry on %s', cal_date)

    if tasks_already_entered_cnt is 0:
        logging.error('clockify_api_set_time_entries : No tasks for time entry on %s', cal_date)


def clockify_api_delete_time_entry(time_entry_id):
    "Delete a time entry for the given time entry id"

    # DELETE request
    response = requests.delete(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_ARAMETRICS_WORKSPACE_ID + '/timeEntries/' + time_entry_id,
        headers=CLOCKFIFY_HEADER)

    logging.debug('clockify_api_delete_time_entry : response : \n %s\n', pformat(response.text))


def clockify_api_update_time_entries(tasks_array, cal_date, workspace_id):
    "Clean up time entries by cross checking the current list of tasks and date"

    # Get time entries for the given date
    current_date_time_entries = clockify_api_get_current_date_time_entries(cal_date, workspace_id)

    if len(tasks_array) is 0:
        logging.error('clockify_api_update_time_entries : No tasks are found in the calendar on %s', cal_date)

    if len(current_date_time_entries) is 0:
        logging.error('clockify_api_update_time_entries : No time entries are found in clockify on %s', cal_date)

    # Check if the time entry is still on the calendar as task
    time_entries_removed_cnt = 0
    for time_entry in current_date_time_entries:
        is_task_on_calendar = 0
        for task in tasks_array:
            if time_entry['description'] == task['TODO']:
                is_task_on_calendar = is_task_on_calendar + 1
            else:
                is_task_on_calendar = is_task_on_calendar + 0

        if is_task_on_calendar == 0:
            # Delete if time entry in Clockify was not started. Sometimes task might
            # have been accidentally removed from the calendar, but time entry was
            # made in the clockify
            if time_entry['timeInterval']['duration'] == 'PT1S':
                clockify_api_delete_time_entry(time_entry['id'])
                time_entries_removed_cnt = time_entries_removed_cnt + 1
                logging.debug('clockify_api_update_time_entries : A time entry should be removed %s\n', pformat(time_entry))

    if time_entries_removed_cnt == 0:
        logging.error(
            'clockify_api_update_time_entries : All time entries are cross checked with calendar events on %s', cal_date)
    else:
        logging.error('clockify_api_update_time_entries : %s time entries are removed on %s',
                      time_entries_removed_cnt, cal_date)
