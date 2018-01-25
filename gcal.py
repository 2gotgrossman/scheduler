from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client.file import Storage
from oauth2client import tools

from datetime import timedelta
import gdate


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = '/Users/David/code/scheduler/client_secret.json'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = '/Users/David/code/scheduler/calendar-python-quickstart.json'

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials


class Calendar():
    def __init__(self):
        self.credentials = get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def get_todays_events(self, calendar_id='primary'):
        now = gdate.get_now()
        start_of_today = gdate.get_midnight(now)
        midnight = start_of_today + timedelta(days=1)

        start_of_today = gdate.datetime_to_gdate(start_of_today)
        midnight = gdate.datetime_to_gdate(midnight)

        events_result = self.service.events().list(
            calendarId=calendar_id, timeMin=start_of_today, timeMax=midnight, singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def schedule_task(self, name, start, end, calendar_id = 'primary'):
        event = {
            'summary': name,
            'description': 'Created by David2.0',
            'start': {
                'dateTime': start,
                'timeZone': "UTC",
            },
            'end': {
                'dateTime': end,
                'timeZone': "UTC",
            },
        }
        self.service.events().insert(calendarId=calendar_id, body=event).execute()

    def delete_today(self, calendar_id):
        events = self.get_todays_events(calendar_id=calendar_id)

        for event in events:
            self.service.events().delete(calendarId=calendar_id, eventId = event['id']).execute()


def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    c = Calendar()


if __name__ == '__main__':
    main()