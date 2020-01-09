#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

import pprint
import json
import datetime

from config import *


def utils_cal_events_parser(cal_events):
    tasks = []

    if not cal_events:
        return None
    for event in cal_events:
        task_str_array = event['summary'].split('#')
        if len(task_str_array) > 2:
            task = {
                'PROJECT_ID': CLOCKFIFY_PROJECT_IDS[str(task_str_array[1]).strip()],
                'TODO': str(task_str_array[2]).strip(),
                'TAG': str(task_str_array[3]).strip(),
            }
            tasks.extend([task])

    pprint.pprint(tasks)
    return tasks
