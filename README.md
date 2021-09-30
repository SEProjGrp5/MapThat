<h1 align="center">
  <img src="https://github.com/SEProjGrp5/MapThat/blob/main/Images/MapThat.gif" width=800px height=300px>
</h1>

# Python Application to add travel time to google calendar

[![GitHub license](https://img.shields.io/github/license/SEProjGrp5/MapThat)](https://github.com/SEProjGrp5/MapThat/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/SEProjGrp5/MapThat)](https://github.com/SEProjGrp5/MapThat/issues)
[![DOI](https://zenodo.org/badge/408263207.svg)](https://zenodo.org/badge/latestdoi/408263207)

Double booking a time-slot is a common mistake that us humans make all the time! We also don't take into account that we are not FLASH and that we need some time to travel from point A to point B. While scheduling appointments on google calendar, while enrolling into two consecutive classes in two different buildings; the travel time between appointments is not taken into consideration.

We aim to develop a tool which will read the google calendar appointments to determing the location and calculate the average travel time to the appointment from either a predetermined location or the location of the previous appointment and block the time needed on google calendar.

We have implemented it as a python application which will be connected to the google calendar and google maps. 

We have used the google calendar and google maps APIs to read and write the calendar entries.

To maintan privacy of users, we will directly store the data in the users account.

## Built with:
1.Python\
2.PHP\
3.javascript\
4.Google Calendar API\
5.Google Maps API

## Installations:

### Following Steps to be done on Google Cloud console:
1. Create a Project\
2. Setup Billing\
3. Enable geocoding API and distancematrix API\
4. generate API key-\
    Refer to the following link https://developers.google.com/maps/documentation/geocoding/get-api-key
6. Store the API key in the following format-\
    File name: key.json\
    File Content: {"key": "your api key here"}\
    **Key needs to be stored in the json folder.**


## How to Contribute?


## Future Scope:
1. Create a chrome extension for extraction of important moodle dates and block the corresponding time for the events in google calendar.\
2. Keep  track of the user's preferred mode of transportation i.e. the average time taken by the user to travel via bus/car/two-wheeler/train/walk.

## Team Members:








