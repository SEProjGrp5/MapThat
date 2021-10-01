get_api_key(self):
- This function extracts the api key from the json file
- Input Args : None
- Output: API Keys appended to the json file 

get_default_location(self):
- This accepts the default locatin from the user and stores it into the json file
- Input Args : None
- Output : User data appended to the json file using input default location

get_lat_log(self, address):
- This function converst a textual address to a set of coordinates
- Input Args : Address
- Output :  list of the latitude and longitude of the given address using google maps

get_default_mode(self):
- This accepts the default mode of transport from the user and stores it ot the json file
- Input Args : None
- Output: Users preferred mode of transport appended to the json file 

get_default_time_bw_events(self):
- This accepts the maximum time between events wherein the user would go directly from one event to the other and stors it to the json file
- Input Args : None
- Output : This function performs json dump for the maximum time. No output 

check_login(self):
- This checks whether the login credentials are available locally
- Input Args : None
- Output : Login credentials pushed to token.json

check_user_data(self):
- This checks if the user data is present locally
- Input Args : None
- Output : This function retrieves user information from the json file and stores it in variables 

get_event(self):
- this extracts the events from the user's calendar
- Input Args : None
- Output : Creates a list of all the events in the calendar 

check_events(self):
- this checks each event from the calendar
- Input Args : None
- Output : Traverses through all the events in the calendar and checks for the following parameters :
           - Events that last all day are ignored 
           - Checks that no changes in the previous event which can affect the travel time to the current event 
           - Checks if the event has a location. If it doesnt have a loction, it is flagged and we check the next event

get_distance(self, dest, src):
- this gets the distace matrix which includes the travel time to the event
- Input Args : Dest, src
- Output : Returns the calculated travel time

event_create(self, start, travel_time):
- This creates the travel time event to the user's calendar
- Input Args : Start and Travel time 
- Output : Creates a google calendar event for the travel time calculated dynamically 

update_event(self, event):
- This updates the current event to add a string which prevents mapThat from processing the event again
- Input Args : Event 
- output: Creates a flag like string to avoid processing same event twice 

driver(self):
- This is the driver function, it drives the whole application.
