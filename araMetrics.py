#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

from config import *
from google_api import *
from clockify_api import *
from utils import *


def main():
    calendar = google_api_login()
    cal_events = google_api_retrieve_cal_events(calendar, GOOGLE_CALENDARS['todo'])
    tasks = utils_cal_events_parser(cal_events)
    clockify_api_set_time_entries(tasks)


if __name__ == '__main__':
    main()
