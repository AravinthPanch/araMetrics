#!/usr/bin/env python

# Author        : Aravinth Panch
# Description   : This contains the functions to get calendar events from Google via Google API Client

from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import pprint
import datetime
import pickle
import os.path
import logging
from pprint import pformat

from config import *


def google_api_login():
    "Authenticate Google API with given credentials and return the calendar service"

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service


def google_api_get_cal_events(cal_service, calendar_id, cal_date):
    "Get all the calendar events for the given calendar and date"

    # 'Z' indicates UTC time
    # Use timeframe to cover CET and IST zone, otherwise events from other days are retrieved.
    time_min = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 5).isoformat() + 'Z'
    time_max = datetime.datetime(cal_date.year, cal_date.month, cal_date.day, 20).isoformat() + 'Z'

    # GET request
    response = cal_service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                                         singleEvents=True, orderBy='startTime').execute()
    cal_events = response.get('items', [])

    logging.debug('google_api_get_cal_events : response : \n %s\n', pformat(cal_events))

    if calendar_id == GOOGLE_CALENDARS['TASKS_TODO']:
        logging.error('google_api_get_cal_events : Found %s Calendar events on %s', len(cal_events), cal_date)

    return cal_events
