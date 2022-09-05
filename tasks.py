from __future__ import print_function

import datetime
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']
tasklist_id = ''


def initial():
    global tasklist_id

    def name_check(tasklist):
        global tasklist_id
        for entry in tasklist:
            if entry['title'] == 'Matched Betting Test':
                tasklist_id = entry['id']
                return True
            else:
                pass
        return False

    # Get Google Account Sign In Credentials
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Connect To Google Tasks API
    try:
        service = build('tasks', 'v1', credentials=creds)

        # Get List of TaskLists
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        # Check if Matched Betting Tasklist Exists
        check = name_check(items)
        if not check:
            # If Matched Betting List does not exist then create it
            tasklist = service.tasklists().insert(
                body={'title': 'Matched Betting Test'}
            ).execute()
            tasklist_id = tasklist['id']
        else:
            pass

    except HttpError as err:
        print(err)


def add_task(info, due):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('tasks', 'v1', credentials=creds)

    try:
        # Add Task
        service.tasks().insert(
            tasklist=tasklist_id, body={'title': info, 'due': due}
        ).execute()

    except HttpError as err:
        print(err)


def get_bets():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('tasks', 'v1', credentials=creds)

    try:
        # Add Task
        results = service.tasks().list(
            tasklist=tasklist_id
        ).execute()
        items = results.get('items', [])
        return items

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    initial()
