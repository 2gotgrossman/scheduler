

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import datetime, timedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

EST = "-05:00"

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join('.',
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class Calendar():
    def __init__(self):
        self.credentials = get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=self.http)

    def get_todays_events(self, calendar_id='primary', tz = EST):
        now = datetime.now().isoformat() # indicates UTC time
        tomorrow = datetime.now() + timedelta(1)
        midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                            day=tomorrow.day, hour=0, minute=0, second=0).isoformat()
        now = now + tz
        midnight = midnight + tz
        eventsResult = self.service.events().list(
            calendarId=calendar_id, timeMin=now, timeMax=midnight, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        for event in events:
            print(event)


print(datetime.now())
print(datetime.today())
print(datetime.utcnow())

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    c = Calendar()
    c.get_todays_events()

    # calendar_list = service.calendarList().list().execute()
    # print(calendar_list['items'][0].keys())
    # for calendar_list_entry in calendar_list['items']:
    #     print(calendar_list_entry)





    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()