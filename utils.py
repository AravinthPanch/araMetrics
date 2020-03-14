#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : This contains various utilities used in this project

# Mappings

# Projects #tag1
# - AC - araCreate (GIG, GreenBuzz, Zerosec)
# - WG - Watergenics
# - DS - DreamSpace (Sri Lanka, Kenya)
# - ML - MotionLab
# - BS - Berlin Senate (Startup AsiaBerlin, APW, enpact)
# - PL - Personal Life

# Sub #tag2
# - TK - TasK
# - ET - EvenT
# - LG - LearninG
# - TG - TeachinG
# - MM - Match Making
# - MG - MeetinG
# - EG - EntertaininG


import pprint
import json
import datetime
import logging
from pprint import pformat

from config import *


def utils_parse_cal_events(cal_events, cal_date):
    "Parse calendar events with the mapping protocol to include Clockify IDs"

    if not cal_events:
        logging.debug('utils_parse_cal_events : No tasks are found in the calendar')
        return

    tasks = []
    time_entry_start = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 01).isoformat() + 'Z'
    time_entry_end = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 00, 00, 02).isoformat() + 'Z'

    for event in cal_events:
        # Separate the calendar event summary by #
        task_str_array = event['summary'].split('#')

        # Ignore calendar events which are not tasks
        if len(task_str_array) > 3:
            task = {
                'PROJECT_ID': CLOCKFIFY_ARAMETRICS_PROJECT_IDS[str(task_str_array[1]).strip()],
                'TODO': event['summary'],
                'TAG_ID': CLOCKFIFY_ARAMETRICS_TAG_IDS[str(task_str_array[2]).strip()],
                'START': time_entry_start,
                'END': time_entry_end
            }
            tasks.extend([task])

    logging.debug('utils_parse_cal_events : response : \n %s\n', pformat(tasks))
    return tasks


def utils_parse_workspace_time_entries(time_entries):
    "Parse time entries from one workspace to another by updating"

    dreamspace_time_entries = []

    for time_entry in time_entries:
        if time_entry['projectId'] == CLOCKFIFY_ARAMETRICS_PROJECT_IDS['DS']:
            if time_entry['timeInterval']['duration'] != 'PT1S':
                entry = {
                    'PROJECT_ID': CLOCKFIFY_DREAMSPACE_PROJECT_IDS['DS'],
                    'TODO': time_entry['description'],
                    'TAG_ID': CLOCKFIFY_DREAMSPACE_TAG_IDS['TK'],
                    'START': time_entry['timeInterval']['start'],
                    'END': time_entry['timeInterval']['end']
                }
                dreamspace_time_entries.extend([entry])

    logging.debug('utils_parse_workspace_time_entries : dreamspace_time_entries : \n %s\n',
                  pformat(dreamspace_time_entries))

    return dreamspace_time_entries
