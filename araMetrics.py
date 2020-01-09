#!/usr/bin/env python

# Author : Aravinth Panch
# araMetrics is a personal impact measurement system to track metrics such
# as tasks, events, contacts, expenses, purchases, travels, behaviour, etc

from config import *
from google_api import *
from clockify_api import *


def main():
    calendar = google_api_login()
    google_api_get_tasks_count(calendar)
    clockify_api_set_time_entry(
        '#AC #Develop araMetrics #araMetrics', CLOCKFIFY_PROJECT_ID)


if __name__ == '__main__':
    main()
