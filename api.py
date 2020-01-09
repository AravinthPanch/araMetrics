import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import pprint
import json
import datetime

from config import *


def google_api_login():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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


def clockify_get_tasks():
    r = requests.get(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/', headers=CLOCKFIFY_HEADER)
    tasks = r.json()
    # pprint.pprint(tasks)

    for task in tasks:
        print(task['timeInterval']['duration'])


def clockify_set_tasks():
    task = {
        "name": "Task from API",
        "projectId": CLOCKFIFY_PROJECT_ID
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/projects/' + CLOCKFIFY_PROJECT_ID + '/tasks/', headers=CLOCKFIFY_HEADER, data=json.dumps(task))

    print r.text


def clockify_set_time_entry(task_description, project_id):
    now = datetime.datetime.now()
    start = datetime.datetime(
        now.year, now.month, now.day, 00, 00, 01).isoformat() + 'Z'
    end = datetime.datetime(now.year, now.month, now.day,
                            00, 00, 02).isoformat() + 'Z'

    time_entry = {
        "start": start,
        "end": end,
        "description": task_description,
        "projectId": project_id
    }

    r = requests.post(
        CLOCKFIFY_API + '/workspaces/' + CLOCKFIFY_WORKSPACE_ID + '/timeEntries/', headers=CLOCKFIFY_HEADER, data=json.dumps(time_entry))

    print r.text
