# my-rides
This summer I've been training for a bike race and tracking all of training!  I wanted to make a dashboard showing my progress this summer, and to do that, I needed to convert all of my ride data to useable tables.  Garmin bike systems record activities and can be exported as a tcx file.  I used the lxml package to parse this tree into a usable dataframe.

# tcx_trackpoints.py

## packages
### lxml, pandas

## Inputs
Python script must be in the same directory as an assets folder with all of your tcx files.

## Outputs
The script outputs three tables
### rides.csv
Includes summary data for each ride.  Primary Key: Ride_Id
### laps.csv
Includes summary data for each lap of a ride.  Primary Key: Lap.  Maps to rides.csv by Ride_Id
### trackpoints.csv
Includes the trackpoints for each ride.  Can be used to make maps, or get a closer look at certain metrics throughout a ride.  Primary Key: Time.  Maps to Rides and Laps
