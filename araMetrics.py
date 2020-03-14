#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : araMetrics is a personal impact measurement system to
# track metrics such as Awards, Connections, Earnings, Emissions, Events,
# Expenses, Learnings, Match-Makings, Meetings, Minutes, Practices,
# Projects, Purchases, Tasks, Teachings, Trips

from config import *
from google_api import *
from clockify_api import *
from utils import *
import sys


def get_current_day_for_operation(days_offset):
    "Create a datetime with the chosen day"
    days_offset = int(days_offset)

    cal_date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                 datetime.datetime.now().day - days_offset).date()

    return cal_date


def clean_up_time_entries(cal_service, todo_cal_events):
    "Get events from all the calendars, merge them and cross check them with time entries in Clockify and clean up the time entries, if they are still on the calendar as tasks"
    done_cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_DONE'], cal_date)
    progress_cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_PROGRESS'], cal_date)
    incomplete_cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_INCOMPLETE'], cal_date)

    all_cal_events = []

    for cal_event in todo_cal_events:
        all_cal_events.extend([cal_event])

    for cal_event in done_cal_events:
        all_cal_events.extend([cal_event])

    for cal_event in progress_cal_events:
        all_cal_events.extend([cal_event])

    for cal_event in incomplete_cal_events:
        all_cal_events.extend([cal_event])

    logging.debug('clean_up_time_entries : all_cal_events : \n %s\n %s', pformat(all_cal_events), len(all_cal_events))

    all_tasks = utils_parse_cal_events(all_cal_events)
    clockify_api_update_time_entries(all_tasks, cal_date)


def get_commandline_arguments():
    "Get commandline arugements to get the day of operation"

    # Take only one argument, one digit and less than a week
    # If there is no argument, just choose the present day
    if len(sys.argv) == 2 and len(sys.argv[1]) == 1 and int(sys.argv[1]) <= 7:
        return sys.argv[1]
    else:
        return 0


if __name__ == '__main__':
    print('========== araMetrics ==========')

    days_offset = get_commandline_arguments()
    cal_date = get_current_day_for_operation(days_offset)
    day_before_yesterday = get_current_day_for_operation(2)

    cal_service = google_api_login()
    cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_TODO'], cal_date)

    clean_up_time_entries(cal_service, cal_events)

    tasks = utils_parse_cal_events(cal_events)
    clockify_api_set_time_entries(tasks, cal_date)
