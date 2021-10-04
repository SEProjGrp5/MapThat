<h1 align="center">
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/MAPTHAT.gif.gif" width=800px height=300px>
</h1>

### *If you and time have a spat, use MapThat*

# Python Application to add travel time to google calendar

[![GitHub license](https://img.shields.io/github/license/SEProjGrp5/MapThat)](https://github.com/SEProjGrp5/MapThat/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/SEProjGrp5/MapThat)](https://github.com/SEProjGrp5/MapThat/issues)
[![DOI](https://zenodo.org/badge/408263207.svg)](https://zenodo.org/badge/latestdoi/408263207)

# DESCRIPTION

Double booking a time-slot is a common mistake that us humans make all the time! We also don't take into account that we are not FLASH and that we need some time to travel from point A to point B. While scheduling appointments on google calendar, while enrolling into two consecutive classes in two different buildings; the travel time between appointments is not taken into consideration.

We aim to develop a tool which will read the google calendar appointments to determe the location and calculate the average travel time to the appointment from either a predetermined location or the location of the previous appointment and block the time needed on google calendar.

We have implemented it as a python application which will be connected to the google calendar and google maps. 

We have used the google calendar and google maps APIs to read and write the calendar entries.

To maintan privacy of users, we will directly store the data in the users account.

# FEATURES
1. Get travel time to a location from the location of the previous event(within a preset timeframe) or a default location
2. Choose between various modes of transport
3. Block of the travel time on your calendar to make sure you take the it into account while setting up other appointments
4. Travel time gets updated if the previous appointment affects the current appointment.
5. Keep Track on total time spent on travel which will help plan your day better


# VISUAL REPRESENTATION

<a href="https://www.youtube.com/watch?v=EBHrUYNMrJs" target="_blank"><img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/screenshot.PNG" width="450" alt="Visual Representation for MapThat"/></a>

# USE CASES IN THE VIDEO

## Case 1: 
A boy hasn’t considered the travel time from his house to his lecture. He is assuming he would reach on time but misses his class.

If he had used MapThat, he would’ve known the exact bus timings and the time he needs to leave via his calendar.

## Case 2: 
Mr. Jacobs had scheduled two back-to-back meetings without considering the locations of the meetings.

In MapThat, there’ll be a functionality which would stop you from scheduling the meeting consecutively if they aren’t in the same building.


# BUILT WITH
1.Python \
2.json \
3.Google Calendar API \
4.Google Maps API

# INSTALLATIONS
Follow the instructuions given below and you are good to go!! 
## Prerequisites
1. You'll need python on your device. If you don't have it install it from [here](https://www.python.org/downloads/).
2. Install the packages needed for the project 
    ```sh 
    pip install -r requirements.txt
    ```
## Run Instructions
**1. Clone this GitHub project.**

**2. Following Steps to be done on Google Cloud console:**
  1. Create a Project 
  2. Setup Billing 
  3. Enable geocoding API and distancematrix API
  4. Generate API key-
      Refer to [this](https://developers.google.com/maps/documentation/geocoding/get-api-key) link for more information about the same.
  5. Store the API key in the following format-
      File name: key.json \
      File Content: {"key": "your api key here"}
  6. Key needs to be stored in the json folder.
  
**3. Run command- python MapThat.py**

# WORKING MODEL
  <summary>Working Model of the project </summary>
  1. Sample Event without location<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG1.jpeg"><br/>
    <br/>
  2. Sample Event with location<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG2.jpeg" ><br/>
    <br/>
  3. Screenshot of Calendar before running the program<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG3.jpeg" ><br/>
    <br/>
  4. Running the Python File<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG8.jpeg" ><br/>
    <br/>
  5. Google Account Login Funnel Step 1<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG4.jpeg" ><br/>
    <br/>
  6. Google Account Login Funnel Step 2<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG5.jpeg" ><br/>
    <br/>
  7. Google Account Login Funnel Step 3<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG6.jpeg" ><br/>
    <br/>
  8. Google Account Login Funnel Step 4<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG7.jpeg" ><br/>
    <br/>
  9.  Setting up default information and checking calndar events<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG12.jpeg" ><br/>
    <br/>
  10. Details of events traversed and events created<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG13.jpeg" ><br/>
    <br/>
  11. Details of events traversed and events created<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG16.jpeg" ><br/>
    <br/>
  12. Exiting the application<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG15.jpeg" ><br/>
    <br/>
  13. Calendar after running application<br/>
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/IMG14.jpeg" ><br/>
    <br/>

# HOW TO CONTRIBUTE?
The [CONTRIBUTING.md](https://github.com/SEProjGrp5/MapThat/blob/main/CONTRIBUTING.md) given in this repository has instructions on how to contribute to this repo. Kindly refer to this file and our [Code of Conduct guidelines](https://github.com/SEProjGrp5/MapThat/blob/main/CODE_OF_CONDUCT.md).

- Reporting Bugs
- Suggesting enhances
- Pull request


# FUTURE SCOPE
1. Create a chrome extension for extraction of important moodle dates and block the corresponding time for the events in google calendar.
2. Auto select the user's preferred mode of transportation i.e. the average time taken by the user to travel via bus/car/two-wheeler/train/walk based on the user's selection bhistory
3. Give Alerts when it is time to leave
4. Give alerts in case of conflict
5. Develop a UI
6. Set up cronjonb for Python automation
7. Update travel time when event is updated
8. Connect to other calendar apps
9. Extract location based on event title/description in cases where it is not explicitly defined
10. Set work location and use it as default during working hours

# TEAM MEMBERS
- [Anant Gadodia (agadodi@ncsu.edu)](https://github.com/antgad)
- [Anmolika Goyal (agoyal4@ncsu.edu)](https://github.com/AnmolikaGoyal)
- [Shreya Someswar Karra (sskarra@ncsu.edu)](https://github.com/sskarra1234)
- [Shubhangi Jain (sjain29@ncsu.edu)](https://github.com/shubhangij12)
- [Srujana Marne Shiva Rao (smarnes@ncsu.edu)](https://github.com/srujanarao)







