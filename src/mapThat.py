from __future__ import print_function

import datetime
import json
import os
import sys
import pytz
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


class mapThat:
    """
    This class runs the mapThat application
    """
    def __init__(self):
        """
        This is the init function. It defines all global variables.
        """
        self.creds = None
        self.events = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.api_key_1 = None  # apikey for maps distance matrix
        # the api key is stored as a local json. refer to readme for more instructions
        self.default_location = None
        self.mode = None
        self.data = {}
        self.user_data = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                      "json", "user_data.json")
        self.service = None
        self.prev_time = None
        self.prev_location = None
        self.time_bw_event = 3600
        self.prev_event_id = None
        self.prev_event_travel = 0
        self.prev_event_traversed = 1
        self.prev_travel_event_id = None

    def get_api_key(self):
        """
        This fucntion extracts the api key from the json file

        Returns
        -------
        None.

        """
        key_data = os.path.join(os.path.dirname(os.path.dirname
                                                (os.path.abspath(__file__))), "json", "key.json")
        if not os.path.exists(key_data):
            print(
                '''Api Key file does not exist. Please refer to readme to add key and restart program''')
            sys.exit("Thank You for Using MapThat")
        with open(key_data) as json_file:
            data = json.load(json_file)
            self.api_key_1 = data["key"]
            #loading the api key from json file. Due to security reasons, we store the key locally
            #our private machines as a json file which is ignored by github which making changes

    def get_default_location(self):
        """
        this accepts the default locatin from the user and stores it into the json file

        Returns
        -------
        None.

        """
        address = input("Enter Default Location: ").replace(" ", "+")
        if os.path.exists(self.user_data):
            with open(self.user_data) as infile:
                self.data = json.load(infile)
        self.data['add'] = str(address)
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)
        self.default_location = self.get_lat_log(address)
        self.prev_location = self.default_location
        #the dufalut starting location of the user can be entered for the first time or updated 
        #from here. everytime an update is made, the json file storing the data locally is also updated.
        

    def get_lat_log(self, address):
        """
        This function converst a textual address to a set of coordinates

        Parameters
        ----------
        address : String
            the location for which coordinates are needed.

        Returns
        -------
        list
            the latitude and longitude of the given address using google maps.

        """
        address2 = address.replace(" ", "+")
        url = '''https://maps.googleapis.com/maps/api/geocode/json?key={0}&address={1}&language=en-EN'''.format(self.api_key_1, str(address2))
        r = requests.get(url)
        return [r.json().get("results")[0].
                get("geometry").
                get("location").
                get('lat'),
                r.json().get("results")[0].get("geometry").get("location").get('lng')]

    def get_default_mode(self):
        """
        this accepts the default mode of transport from the user and stores it ot the json file

        Returns
        -------
        None.

        """
        mode_flag = int(input(
            "1. Select a default mode of transport\n2.Select mode of transport for each event\n"))
        if mode_flag == 1:
            self.mode = input(
                "Enter exact string out of following:[DRIVING, WALKING, BICYCLING, TRANSIT]\n")
        elif mode_flag == 2:
            self.mode = None
        else:
            self.get_default_mode()
        if os.path.exists(self.user_data):
            with open(self.user_data) as infile:
                self.data = json.load(infile)
        self.data['mode'] = self.mode
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)

    def get_default_time_bw_events(self):
        """
        This accepts the maximum time between events wherein the user would go directly from one 
        event to the other and stors it to the json file

        Returns
        -------
        None.

        """
        self.time_bw_event = int(input(
            '''Enter the max time in mins between 2 events to go directly 
             from one event to another:\n'''))*60
        if os.path.exists(self.user_data):
            with open(self.user_data) as infile:
                self.data = json.load(infile)
        self.data['time_bw_event'] = self.time_bw_event
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)

    def check_login(self):
        """
        This checks whether the login credentials are available locally

        Returns
        -------
        None.

        """
        # This function checks if the login details of the user are available with us
        cred_file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "json", "credentials.json")
        token_file = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "json", "token.json")
        # If the user has already logged in, the details are extractecd from token.js
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(
                token_file, SCOPES)
        # if the user has not logged in/ his credentials have expired, 
        #the user is prompted to login and the details are stored in token.json
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    cred_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
                print("Login Successfull")
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())

    def check_user_data(self):
        """
        this checks if the user data is present locally

        Returns
        -------
        None.

        """
        if not os.path.exists(self.user_data):
            print("User data does not exist")
            self.get_default_location()
            self.get_default_mode()
            self.get_default_time_bw_events()
        else:
            with open(self.user_data) as json_file:
                data = json.load(json_file)
                self.mode = data['mode']
                self.time_bw_event = int(data['time_bw_event'])
                self.default_location = self.get_lat_log(data['add'])
                print("Default mode of transport:", self.mode)
                print("Default Location: ", data['add'].replace("+", " "))
                print("Max time in mins between 2 events to go directly from one event to another:",
                      str(int(self.time_bw_event/60)))
                if self.default_location == "":
                    print("error reading default location")
                    self.get_default_location()

    def get_event(self):
        """
        this extracts the events from the user's calendar

        Returns
        -------
        None.

        """
        self.service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        self.prev_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True, 
                                                   orderBy='startTime').execute()
        self.events = events_result.get('items', [])
        if not self.events:
            print('No upcoming events found.')

    def check_events(self):
        """
        this checks each event from the calendar

        Returns
        -------
        None.

        """
        for event in self.events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            if len(start) < 20:  # ignore events which last all day(do not have a time)
                self.update_event(event)
                continue
            print("\n\n\n\n", start, event['summary'])
            if 'description' in event:
                if event['description'] == '#Created by MapThat#':
                    self.prev_event_travel = 1
                    self.prev_travel_event_id = event['id']
                    continue
                if ('#This event has been checked by MapThat#' in event['description'] 
                    and self.prev_event_traversed == 1):
                    #this is to make sure that there are no changes in the previous event which can affect the travel time to the current event
                    self.prev_time = datetime.datetime.strptime(
                        (event['end'].get('dateTime', event['end'].get('date'))),
                        "%Y-%m-%dT%H:%M:%S%z")
                    if 'location' in event:
                        self.prev_location = event['location']
                    self.prev_event_traversed = 1
                    self.prev_event_travel = 0
                    continue
            if self.prev_event_travel == 1 and self.prev_travel_event_id not in [None]:
                self.service.events().delete(calendarId='primary',
                                             eventId=self.prev_travel_event_id).execute()
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            self.prev_event_traversed = 0
            self.update_event(event)
            time_diff = ((start-self.prev_time).total_seconds())
                #checking if the event has a location. if it doesnt have a loction, it is flagged and we check the next event
            if 'location' in event:
                print("location: ", event['location'])
                if self.mode is None:
                    self.mode = input(
                        '''Enter exact string out of following:[DRIVING, WALKING, BICYCLING, TRANSIT]\n''')
                if time_diff >= 3600:
                    src = self.default_location
                else:
                    src = self.default_location
                    if self.prev_location not in [None]:
                        src = self.get_lat_log(self.prev_location)
                travel_time = self.get_distance(event['location'], src)
                self.event_create(start, travel_time)
                self.prev_location = event['location']
            else:
                print("no Location")
                self.prev_location = None
            self.prev_time = datetime.datetime.strptime(
                (event['end'].get('dateTime', event['end'].get('date'))), "%Y-%m-%dT%H:%M:%S%z")
            self.prev_event_travel = 0
            self.prev_event_id = None
            self.prev_travel_event_id = None
            #resetting all flags

    def get_distance(self, dest, src):
        """
        this gets the distace matrix which includes the travel time to the event

        Parameters
        ----------
        dest : String
            address of location for event.
        src : list
            coordinates of source address.

        Returns
        -------
        int
            travel time in seconds.

        """
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        dest_lat_lon = self.get_lat_log(dest)
        if dest_lat_lon is None:
            print("Location not Found")
            return 0
        orig = str(src[0]) + " " + str(src[1])
        dest = str(dest_lat_lon[0]) + " " + str(dest_lat_lon[1])
        url = '''https://maps.googleapis.com/maps/api/distancematrix/json?key={0}&origins={1}&destinations={2}&mode={3}&language=en-EN&sensor=false'''.format(
            self.api_key_1, str(orig), str(dest), self.mode)
        r = requests.get(url)
        travel_time = r.json().get('rows')[0].get("elements")[
            0].get("duration").get("value")
        print("Travel time:")
        print(travel_time)
        return travel_time

    def event_create(self, start, travel_time):
        """
        This creates the travel time event to the user's calendar

        Parameters
        ----------
        start : datetime
            the start time of the event whose location is being read.
        travel_time : int
            the travel time to the event in seconds.

        Returns
        -------
        None.

        """
        end = start.isoformat()
        start = (start - datetime.timedelta(seconds=travel_time)).isoformat()
        print("travel event created starting:")
        print(start)
        event_result = self.service.events().insert(calendarId='primary',
                                                    body={
                                                        "summary": 'Travel Time',
                                                        "description": '#Created by MapThat#',
                                                        "start": {"dateTime": str(start)},
                                                        "end": {"dateTime": str(end)},
                                                    }
                                                    ).execute()

    def update_event(self, event):
        """
        This updates the current event to add a string which prevents mapThat from processing
        the event again

        Parameters
        ----------
        event : dictionary
            the details of the event being edited.

        Returns
        -------
        None.

        """
        if 'description' in event:
            event['description'] = event['description'] + \
                "\n#This event has been checked by MapThat#"
        else:
            event['description'] = "#This event has been checked by MapThat#"
        updated_event = self.service.events().update(
            calendarId='primary', eventId=event['id'], body=event).execute()

    def driver(self):
        """
        This is the driver function.
        it drives the whole application.

        Returns
        -------
        None.

        """
        flag_loop = 1
        while flag_loop == 1:
            self.get_api_key()
            self.check_login()
            self.check_user_data()
            flag = int(input('''1.Check Calendar\n2.Change Mode\n3.Change Default Location\n4.Change max time in mins between 2 events to go directly from one event to another\n5. Exit\n'''))
            if flag == 1:
                self.get_event()
                self.check_events()
            elif flag == 2:
                self.get_default_mode()
            elif flag == 3:
                self.get_default_location()
            elif flag == 4:
                self.get_default_time_bw_events()
            elif flag == 5:
                print("Thank You for Using MapThat")
                flag_loop = 0
            else:
                print("incorrect input")


if __name__ == '__main__':
    mapThat().driver()
