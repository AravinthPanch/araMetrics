from keys import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Calendars
GOOGLE_CALENDARS = {
    'todo': 'primary',
    'done': 'aravinth.info_br3mmn53o62l518pb8b91rc10k@group.calendar.google.com',
    'in-progress': 'aravinth.info_eklo4n5fmduvgfd4tdrnjahjbs@group.calendar.google.com',
    'incomplete': 'aravinth.info_4i7u5rc7km6k313hatp43qti44@group.calendar.google.com'
}

CLOCKFIFY_API = 'https://api.clockify.me/api'
CLOCKFIFY_HEADER = {'content-type': 'application/json', 'X-Api-Key': CLOCKFIFY_API_KEY}
CLOCKFIFY_PROJECT_IDS = {
    'AC': '5e175b681cda2a26697c6afc',
    'WG': '5e17a67570e4883ef699688b',
    'DS': '5e17a6c21cda2a26697c99aa',
    'ML': '5e17a66b0c1cd15d4a80712b',
    'BS': '5e17a6a30c1cd15d4a807147',
    'PL': '5e17a6f770e4883ef69968cf'
}
