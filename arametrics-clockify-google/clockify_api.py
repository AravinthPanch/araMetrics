#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : This contains the functions to get and set time entries from Clockify via REST API

import requests
import pprint
import json
import datetime
import logging
from pprint import pformat
from datetime import timedelta

from config import *
from utils import *


def clockify_api_get_time_entries_on_day_of_operation(day_of_operation, workspace_id):
    "Get time entries for the given day. Clockify API is not filtering with &start=' + time_entry_start+ '&end=' + time_entry_end"

    # GET request
    # Change the limit for accessing older time entries
    nr_of_time_entries_to_fetch = 100
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + workspace_id + '/timeEntries/user/' + CLOCKFIFY_USER_ID + '?limit=' + str(nr_of_time_entries_to_fetch), headers=CLOCKFIFY_HEADER)
    time_entries = r.json()

    logging.debug('clockify_api_get_time_entries_on_day_of_operation : time_entries : \n %s\n', pformat(time_entries))

    # Filter them by date
    time_entries_on_day_of_operation = []
    for time_entry in time_entries['timeEntriesList']:
        time_entry_date_time = datetime.datetime.strptime(time_entry['timeInterval']['start'], '%Y-%m-%dT%H:%M:%SZ')

        if time_entry_date_time.date() == day_of_operation:
            time_entries_on_day_of_operation.extend([time_entry])

    logging.debug('clockify_api_get_time_entries_on_day_of_operation : time_entries_on_day_of_operation : \n %s\n',
                  pformat(time_entries_on_day_of_operation))
    logging.error('clockify_api_get_time_entries_on_day_of_operation : Found %s Clockify entries on %s',
                  len(time_entries_on_day_of_operation), day_of_operation)

    return time_entries_on_day_of_operation


def clockify_api_set_time_entry(task_todo, taks_project_id, task_tag_id, task_start, task_end, workspace_id):
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


def clockify_api_set_time_entries(tasks_array, day_of_operation, workspace_id):
    "Create time entries for the given list of tasks and date "

    # Get time entries for the given date
    time_entries_on_day_of_operation = clockify_api_get_time_entries_on_day_of_operation(day_of_operation, workspace_id)

    if tasks_array is None or len(tasks_array) is 0:
        logging.error('clockify_api_set_time_entries : No tasks are found in the calendar on %s', day_of_operation)
        return

    if len(time_entries_on_day_of_operation) is 0:
        logging.error('clockify_api_set_time_entries : No time entries are found in clockify on %s', day_of_operation)

    # Check if the task is already entered as a time entry.
    tasks_already_entered_cnt = 0
    for task in tasks_array:
        is_task_already_entered = 0

        # Sometimes there are multiple entries of same task.
        for time_entry in time_entries_on_day_of_operation:
            if task['TODO'] == time_entry['description']:
                is_task_already_entered = is_task_already_entered + 1
            else:
                is_task_already_entered = is_task_already_entered + 0

        # If task is not already entered as a time entry, create one.
        if is_task_already_entered == 0:
            clockify_api_set_time_entry(task['TODO'], task['PROJECT_ID'], task['TAG_ID'],
                                        task['START'], task['END'], workspace_id)
            tasks_already_entered_cnt = tasks_already_entered_cnt + 1
            logging.error('clockify_api_set_time_entries : A task is entered as a time entry on %s', day_of_operation)

    if tasks_already_entered_cnt is 0:
        logging.error('clockify_api_set_time_entries : No tasks for time entry on %s', day_of_operation)


def clockify_api_delete_time_entry(time_entry_id, workspace_id):
    "Delete a time entry for the given time entry id"

    # DELETE request
    response = requests.delete(
        CLOCKFIFY_API + '/workspaces/' + workspace_id + '/timeEntries/' + time_entry_id,
        headers=CLOCKFIFY_HEADER)

    logging.debug('clockify_api_delete_time_entry : response : \n %s\n', pformat(response.text))


def clockify_api_update_time_entries(tasks_array, day_of_operation, workspace_id):
    "Clean up time entries by cross checking the current list of tasks and date"

    # Get time entries for the given date
    time_entries_on_day_of_operation = clockify_api_get_time_entries_on_day_of_operation(day_of_operation, workspace_id)

    if len(tasks_array) is 0:
        logging.error('clockify_api_update_time_entries : No tasks are found in the calendar on %s', day_of_operation)

    if len(time_entries_on_day_of_operation) is 0:
        logging.error('clockify_api_update_time_entries : No time entries are found in clockify on %s', day_of_operation)

    # Check if the time entry is still on the calendar as task
    time_entries_removed_cnt = 0
    for time_entry in time_entries_on_day_of_operation:
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
                clockify_api_delete_time_entry(time_entry['id'], workspace_id)
                time_entries_removed_cnt = time_entries_removed_cnt + 1
                logging.debug('clockify_api_update_time_entries : A time entry should be removed %s\n', pformat(time_entry))

    if time_entries_removed_cnt == 0:
        logging.error(
            'clockify_api_update_time_entries : All time entries are cross checked with calendar events on %s', day_of_operation)
    else:
        logging.error('clockify_api_update_time_entries : %s time entries are removed on %s',
                      time_entries_removed_cnt, day_of_operation)


def clockify_api_create_day_to_day_tasks(day_of_operation, workspace_id):
    "Create usual day-to-day tasks such as commuting, learning, sleeping"

    day_to_day_tasks = [
        {'summary': '#PL #LF #Sport #health'},
        {'summary': '#PL #LF #Movie #fun'},
        {'summary': '#PL #LF #Commute #travel'},
        # {'summary': '#PL #LF #Wash #health'},
        {'summary': '#PL #LF #Sleep #health'},
        {'summary': '#AC #LG #Learning #GK'},
        {'summary': '#AC #LG #BioTech + Khan Academy #bio'},
        {'summary': '#AC #TK #Follow up #org'},
        {'summary': '#DS #TK #Follow up #org'},
        {'summary': '#BS #TK #Follow up #org'},
        # {'summary': '#ML #TK #Follow up #org'}
        {'summary': '#AC #TK #Branding Daily #araBrand'},
    ]
    tasks = utils_parse_cal_events(day_to_day_tasks, day_of_operation)
    clockify_api_set_time_entries(tasks, day_of_operation, workspace_id)


def clockify_api_clean_day_to_day_tasks(day_of_operation, workspace_id):
    "Clean up unused daily tasks"

    days_offset = 1
    x_day_of_operation = day_of_operation - timedelta(days=days_offset)

    time_entries_on_day_of_operation = clockify_api_get_time_entries_on_day_of_operation(
        x_day_of_operation, workspace_id)

    time_entries_removed_cnt = 0
    for time_entry in time_entries_on_day_of_operation:

        if time_entry['timeInterval']['duration'] == 'PT1S':
            clockify_api_delete_time_entry(time_entry['id'], workspace_id)
            time_entries_removed_cnt = time_entries_removed_cnt + 1
            logging.debug('clockify_api_update_time_entries : A time entry should be removed %s\n', pformat(time_entry))

    if time_entries_removed_cnt > 0:
        logging.error('clockify_api_update_time_entries : %s time entries are removed on %s',
                      time_entries_removed_cnt, x_day_of_operation)


def clockify_api_copy_entries_to_another_workspace(day_of_operation, workspace_1_id, workspace_2_id):
    "Duplicate time entries from araMetrics workspace to dreamspace workspace"

    print('\naraMetrics Workspace')
    days_offset = 2
    x_day_of_operation = day_of_operation - timedelta(days=days_offset)
    workspace_1_time_entries = clockify_api_get_time_entries_on_day_of_operation(x_day_of_operation, workspace_1_id)

    print('\nDreamspace Workspace')
    workspace_2_time_entries = utils_parse_workspace_time_entries(workspace_1_time_entries)
    clockify_api_set_time_entries(workspace_2_time_entries, x_day_of_operation, workspace_2_id)
