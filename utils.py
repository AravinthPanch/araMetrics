#!/usr/bin/env python

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


import pprint
import json
import datetime

from config import *


def utils_parse_cal_events(cal_events):
    tasks = []

    if not cal_events:
        return None
    for event in cal_events:
        task_str_array = event['summary'].split('#')
        if len(task_str_array) > 3:
            task = {
                'PROJECT_ID': CLOCKFIFY_PROJECT_IDS[str(task_str_array[1]).strip()],
                'TODO': event['summary'],
                'TAG_ID': CLOCKFIFY_TAG_IDS[str(task_str_array[2]).strip()],
            }
            tasks.extend([task])

    pprint.pprint(tasks)
    return tasks
