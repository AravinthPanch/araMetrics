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


def get_day_of_operation(days_offset):
    "Create a datetime with the chosen day"
    days_offset = int(days_offset)

    day_of_operation = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                                         datetime.datetime.now().day - days_offset).date()

    return day_of_operation


def clean_up_time_entries(cal_service, todo_cal_events, workspace_id, day_of_operation):
    "Get events from all the calendars, merge them and cross check them with time entries in Clockify and clean up the time entries, if they are still on the calendar as tasks"

    days_offset = 1
    x_day_of_operation = datetime.datetime(day_of_operation.year, day_of_operation.month,
                                           day_of_operation.day - days_offset).date()

    done_cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_DONE'], x_day_of_operation)
    progress_cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_PROGRESS'], x_day_of_operation)
    incomplete_cal_events = google_api_get_cal_events(
        cal_service, GOOGLE_CALENDARS['TASKS_INCOMPLETE'], x_day_of_operation)

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

    all_tasks = utils_parse_cal_events(all_cal_events, x_day_of_operation)
    clockify_api_update_time_entries(all_tasks, x_day_of_operation, workspace_id)


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

    # Get the day of operation from commandline
    days_offset = get_commandline_arguments()
    day_of_operation = get_day_of_operation(days_offset)
    print('=== Setting the day of operation to ' + str(day_of_operation))

    # Get the events from the calendar
    print('\n=== Getting events from Google Calendar')
    cal_service = google_api_login()
    cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_TODO'], day_of_operation)

    # Clean up unused tasks on the previous day in araMetrics workspace
    print('\n=== Cleaning up unused tasks in Clockify on the previous day')
    clean_up_time_entries(cal_service, cal_events, CLOCKFIFY_ARAMETRICS_WORKSPACE_ID, day_of_operation)

    # Add events from the calendar to araMetrics workspace
    print('\n=== Adding events from Google Calendar to Clockify')
    tasks = utils_parse_cal_events(cal_events, day_of_operation)
    clockify_api_set_time_entries(tasks, day_of_operation, CLOCKFIFY_ARAMETRICS_WORKSPACE_ID)

    # Duplicate time entries from araMetrics workspace to dreamspace workspace
    print('\n=== Duplicating Clockify araMetrics to DreamSpace')
    clockify_api_copy_entries_to_another_workspace(
        day_of_operation, CLOCKFIFY_ARAMETRICS_WORKSPACE_ID, CLOCKFIFY_DREAMSPACE_WORKSPACE_ID)

    # Clean up unused day-to-day tasks on the previous day in araMetrics workspace
    print('\n=== Cleaning up unused day-to-day tasks')
    clockify_api_clean_day_to_day_tasks(day_of_operation, CLOCKFIFY_ARAMETRICS_WORKSPACE_ID)

    # Create usual day-to-day tasks on the current day in araMetrics workspace
    print('\n=== Creating usual day-to-day tasks')
    clockify_api_create_day_to_day_tasks(day_of_operation, CLOCKFIFY_ARAMETRICS_WORKSPACE_ID)
