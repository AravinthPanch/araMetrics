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

# cal_date = datetime.datetime.now().date()
days_offset = 0
cal_date = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month,
                             datetime.datetime.now().day - days_offset).date()


def main():
    cal_service = google_api_login()
    cal_events = google_api_get_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_TODO'], cal_date)
    tasks = utils_parse_cal_events(cal_events)
    clockify_api_set_time_entries(tasks, cal_date)

    # cal_events = google_api_retrieve_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_DONE'])
    # tasks = utils_parse_cal_events(cal_events)
    # clockify_api_set_time_entries(tasks)
    # cal_events = google_api_retrieve_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_PROGRESS'])
    # tasks = utils_parse_cal_events(cal_events)
    # clockify_api_set_time_entries(tasks)
    # cal_events = google_api_retrieve_cal_events(cal_service, GOOGLE_CALENDARS['TASKS_INCOMPLETE'])
    # tasks = utils_parse_cal_events(cal_events)
    # clockify_api_set_time_entries(tasks)


if __name__ == '__main__':
    print('========== araMetrics ==========')
    main()
