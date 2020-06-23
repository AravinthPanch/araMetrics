from keys import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Calendars
GOOGLE_CALENDARS = {
    'TASKS_TODO': 'primary',
    'TASKS_DONE': 'aravinth.info_br3mmn53o62l518pb8b91rc10k@group.calendar.google.com',
    'TASKS_PROGRESS': 'aravinth.info_eklo4n5fmduvgfd4tdrnjahjbs@group.calendar.google.com',
    'TASKS_INCOMPLETE': 'aravinth.info_4i7u5rc7km6k313hatp43qti44@group.calendar.google.com'
}

CLOCKFIFY_API = 'https://api.clockify.me/api'
CLOCKFIFY_HEADER = {'content-type': 'application/json', 'X-Api-Key': CLOCKFIFY_API_KEY}

# araMetrics workspace
CLOCKFIFY_ARAMETRICS_PROJECT_IDS = {
    'AC': '5e175b681cda2a26697c6afc',
    'WG': '5e17a67570e4883ef699688b',
    'DS': '5e17a6c21cda2a26697c99aa',
    'ML': '5e17a66b0c1cd15d4a80712b',
    'BS': '5e17a6a30c1cd15d4a807147',
    'PL': '5e17a6f770e4883ef69968cf',
    'BO': '5ef1bc700218eb6f56fca928'
}
CLOCKFIFY_ARAMETRICS_TAG_IDS = {
    'TK': '5e175f7370e4883ef6993f6d',
    'ET': '5e175fad0c1cd15d4a804819',
    'LG': '5e18e8a70c1cd15d4a81b973',
    'TG': '5e18e8df70e4883ef69ab2db',
    'MM': '5e18e8e41cda2a26697de539',
    'MG': '5e18e8ea70e4883ef69ab2de',
    'LF': '5e1a4fdb0c1cd15d4a820c4e'
}

# dreamspace-academy workspace
CLOCKFIFY_DREAMSPACE_PROJECT_IDS = {
    'DS': '5e4a7200cdcf30080a1134ad'
}
CLOCKFIFY_DREAMSPACE_TAG_IDS = {
    'TK': '5e4e810435012561077bc83f'
}
