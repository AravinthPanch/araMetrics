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


def utils_parse_cal_events(cal_events):
    "Parse calendar events with the mapping protocol to include Clockify IDs"

    if not cal_events:
        logging.error('utils_parse_cal_events : No tasks are found in the calendar')
        return

    tasks = []
    for event in cal_events:
        # Separate the calendar event summary by #
        task_str_array = event['summary'].split('#')

        # Ignore calendar events which are not tasks
        if len(task_str_array) > 3:
            task = {
                'PROJECT_ID': CLOCKFIFY_PROJECT_IDS[str(task_str_array[1]).strip()],
                'TODO': event['summary'],
                'TAG_ID': CLOCKFIFY_TAG_IDS[str(task_str_array[2]).strip()],
            }
            tasks.extend([task])

    logging.debug('utils_parse_cal_events : response : \n %s\n', pformat(tasks))
    return tasks
