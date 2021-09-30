from __future__ import print_function
import datetime
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
#import simplejson, urllib
#import googleapiclient
import requests
import json
#from geopy.geocoders import Nominatim

SCOPES = ['https://www.googleapis.com/auth/calendar']

class mapThat:
    def __init__(self):
        """
        Init class which initializes all variables 
        
        """
        self.creds=None
        self.events=None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.api_key_1="AIzaSyBGAQG3wYes4XkqxkDC_2uOzkgWIGCGsws" #apikey for maps distance matrix
        self.default_location=None
        self.mode=None
        self.mode_flag=0
        self.data={}
        self.user_data=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"json","user_data.json")

    def get_default_location(self):
        """
        Function returns default location       
        
        """
        address=input("Enter Default Location: ").replace(" ","+")
        self.default_location = self.get_lat_log(address)
        self.data['lat']=str(self.default_location[0])
        self.data['Lng']=str(self.default_location[1])
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)
        
        
    def get_lat_log(self, address):
        """
        Function returns latitude longitude values 
        
        """
        address2=address.replace(" ","+")

        url = "https://maps.googleapis.com/maps/api/geocode/json?key={0}&address={1}&language=en-EN".format(self.api_key_1,str(address2))
        r = requests.get(url)
        '''if location==None:
            return None'''
        return [r.json().get("results")[0].get("geometry").get("location").get('lat'), r.json().get("results")[0].get("geometry").get("location").get('lng')]

    def get_default_mode(self):
        """
        Function retrieves default mode of transports      
        
        """
        self.mode_flag=int(input("1. Select a default mode of transport\n2.Select mode of transport for each event\n"))
        if self.mode_flag==1:
            self.mode=input("Enter exact string out of following:[DRIVING, WALKING, BICYCLING, TRANSIT]\n")
        else:
            self.mode=None
        self.data['mode']=self.mode
        with open(self.user_data, 'w') as outfile:
            json.dump(self.data, outfile)
        

    def check_login(self):
        """
        Uses API keys to check login details of the users are available with us 
        
        """
        cred_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"json","credentials.json")
        token_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"json","token.json")
        
        ##If the user has already logged in, the details are extractecd from token.js 
        if os.path.exists(token_file):
            self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        #if the user has not logged in/ his credentials have expired, the user is prompted to login and the details are stored in token.json
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.cred_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
                print("Login Successfull")
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(self.creds.to_json())
        
        if  not os.path.exists(self.user_data):
            print("mode.json not exist")
            self.get_default_location()
            self.get_default_mode()    
            
            
        else:
            with open(self.user_data) as json_file:
                    data = json.load(json_file)
                    self.mode=data['mode']
                    print(data.keys())
                    self.default_location=[float(self.data.get('lat',0.0)),float(self.data.get('Lng',0.0))]
                    if self.default_location== [0.0,0.0]:
                        print("error reading default location")
                        self.get_default_location()
                    print("Defaultmode of transport:" , self.mode)
                    print("Default Location: ",self.default_location)

    def event_manager(self):
        """
        Checks whether the event is new or old
        
        """
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
                #self.events.remove(event)
                continue
            print(start,event['summary'])
            start=datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S%z")
            print(type(self.events))
            print(start, event['summary'])
            self.update_event(event,service)
            try:
                print("\nlocation: ", event['location'])
                if self.mode_flag==2:
                    self.mode=input("Enter exact string out of following:[DRIVING, WALKING, BICYCLING, TRANSIT]\n")
                travel_time=self.get_distance(event['location'])
                self.event_create(start,travel_time,service)
                
            except KeyError:
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
        print("\nTravel time:")
        print(travel_time)
        return travel_time

    def event_create(self,start,travel_time,service):
        end=start.isoformat()
        start=(start - datetime.timedelta(seconds=travel_time)).isoformat()
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
        self.check_login()
        

if __name__ == '__main__':
    mapThat().driver()
