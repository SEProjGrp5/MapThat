
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
    def __init__(self):
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
        key_data = os.path.join(os.path.dirname(os.path.dirname
                                                (os.path.abspath(__file__))), "json", "key.json")
        if not os.path.exists(key_data):
            print(
                '''Api Key file does not exist. Please refer to 
                  readme to add key and restart program''')
            sys.exit("Thank You for Using MapThat")
        with open(key_data) as json_file:
            data = json.load(json_file)
            self.api_key_1 = data["key"]
        

    def get_default_location(self):
        address = input("Enter Default Location: ").replace(" ", "+")
        if os.path.exists(self.user_data):
            with open(self.user_data) as infile:
                self.data = json.load(infile)
        self.data['add'] = str(address)
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)
        self.default_location = self.get_lat_log(address)
        self.prev_location = self.default_location
        
        
    def get_lat_log(self, address):
        address2 = address.replace(" ", "+")
        url = '''https://maps.googleapis.com/maps/api/geocode/json?key={0}
        &address={1}&language=en-EN'''.format(self.api_key_1, str(address2))
        r = requests.get(url)
        return [r.json().get("results")[0].
                get("geometry").
                get("location").
                get('lat'),
                r.json().get("results")[0].get("geometry").get("location").get('lng')]

    def get_default_mode(self):
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
        if not os.path.exists(self.user_data):
            print("User data does not exist")
            self.get_default_location()
            self.get_default_mode()
            self.get_default_time_bw_events()
        else:
            with open(self.user_data) as json_file:
                data = json.load(json_file)
                print(data.keys())
                print(data)
                self.mode = data['mode']
                self.time_bw_event = int(data['time_bw_event'])
                self.default_location = self.get_lat_log(data['add'])
                print("Default mode of transport:", self.mode)
                print("Default Location: ", data['add'].replace("+", " "))
                print("Max time in mins between 2 events to go directly from one event to another:",
                      str(self.time_bw_event))
                if self.default_location == "":
                    print("error reading default location")
                    self.get_default_location()


     def get_event(self):
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


    def event_manager(self):
        service = build('calendar', 'v3', credentials=self.creds)
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        self.events = events_result.get('items', [])
        if not self.events:
            print('No upcoming events found.')
        for event in self.events:
            if 'description' in event:
                if event['description']=='#Created by MapThat#':
                    continue
                if '#This event has been checked by MapThat#' in event['description']:
                    continue

            start = event['start'].get('dateTime', event['start'].get('date'))
            if len(start)<20:#ignore events which last all day(do not have a time)
                continue
            start=datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            print("\n\n\n\n", start, event['summary'])
            self.update_event(event,service)
            if 'location' in event:
                print("location: ", event['location'])
                if self.mode_flag==2:
                    self.mode=input("Enter exact string out of following:[DRIVING, WALKING, BICYCLING, TRANSIT]\n")
                travel_time=self.get_distance(event['location'])
                self.event_create(start,travel_time,service)
                
            else:
                print("no Location")

    def get_distance(self,dest):
        url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
        dest_lat_lon=self.get_lat_log(dest)
        if dest_lat_lon==None:
            print("Location not Found")
            return
        orig = str(self.default_location[0]) + " " + str(self.default_location[1])
        dest = str(dest_lat_lon[0]) + " " + str(dest_lat_lon[1])
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?key={0}&origins={1}&destinations={2}&mode={3}&language=en-EN&sensor=false".format(self.api_key_1,str(orig),str(dest),self.mode)
        
        r = requests.get(url) 
        travel_time=r.json().get('rows')[0].get("elements")[0].get("duration").get("value")
        print("Travel time:")
        print(travel_time)
        return travel_time

    def event_create(self,start,travel_time,service):
        end=start.isoformat()
        start=(start - datetime.timedelta(seconds=travel_time)).isoformat()
        print("travel event created starting:")
        print(start)
        event_result = service.events().insert(calendarId='primary',
           body={
               "summary": 'Travel Time',
               "description": '#Created by MapThat#',
               "start": {"dateTime": str(start)},
               "end": {"dateTime": str(end)},
           }
       ).execute()
        
    def update_event(self,event,service):
        if 'description' in event: 
            event['description']=event['description'] + "\n#This event has been checked by MapThat#"
        else:
            event['description']="#This event has been checked by MapThat#"
            
        updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        


    def driver(self):
        self.get_api_key()
        self.check_login()
        flag=int(input("1.Check Calendar\n2.Change Mode\n3.Change Default Location"))
        if flag==1:    
            self.event_manager()
        if flag == 2:
            self.get_default_mode()
        if flag == 3:
            self.get_default_location()



if __name__ == '__main__':
    mapThat().driver()
