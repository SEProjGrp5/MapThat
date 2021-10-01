get_api_key(self):
- This fucntion extracts the api key from the json file

get_default_location(self):
- This accepts the default locatin from the user and stores it into the json file

get_lat_log(self, address):
- This function converst a textual address to a set of coordinates

get_default_mode(self):
- This accepts the default mode of transport from the user and stores it ot the json file

get_default_time_bw_events(self):
- This accepts the maximum time between events wherein the user would go directly from one event to the other and stors it to the json file

check_login(self):
- This checks whether the login credentials are available locally

check_user_data(self):
- This checks if the user data is present locally

get_event(self):
- this extracts the events from the user's calendar

check_events(self):
- this checks each event from the calendar

get_distance(self, dest, src):
- this gets the distace matrix which includes the travel time to the event

event_create(self, start, travel_time):
- This creates the travel time event to the user's calendar

update_event(self, event):
- This updates the current event to add a string which prevents mapThat from processing the event again

driver(self):
- This is the driver function, it drives the whole application.
