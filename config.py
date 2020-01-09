from keys import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Calendars
cal_tasks = {
    'todo': 'primary',
    'done': 'aravinth.info_br3mmn53o62l518pb8b91rc10k@group.calendar.google.com',
    'in-progress': 'aravinth.info_eklo4n5fmduvgfd4tdrnjahjbs@group.calendar.google.com',
    'incomplete': 'aravinth.info_4i7u5rc7km6k313hatp43qti44@group.calendar.google.com'
}

CLOCKFIFY_API = 'https://api.clockify.me/api'
CLOCKFIFY_HEADER = {'content-type': 'application/json', 'X-Api-Key': CLOCKFIFY_API_KEY}
CLOCKFIFY_PROJECT_ID = '5e17555070e4883ef6992faf'
