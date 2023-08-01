#!/usr/bin/env python
# coding: utf-8



import os
from datetime import datetime, date
from lxml import etree as ET
import pandas as pd
import folium
from geopy.distance import geodesic


def m_to_miles(m):
    miles = (m/1000) * 0.621371
    return miles


def get_file_names_in_directory(directory):
    file_names = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):  # Check if it's a file
            file_names.append(f'assets/{item}')
    return file_names


directory_path = 'assets/'
file_names = get_file_names_in_directory(directory_path)

rides_master = pd.DataFrame(columns=['Ride_Id','Ride_Dist', 'Ride_Max_Speed', 'Ride_Cals', 'Ride_Avg_Cad', 'Ride_Time', 'Ride_Avg_Speed', 'Ride_avg_watts', 'Ride_max_watts', 'ride_ascent', 'ride_descent'])
laps_master = pd.DataFrame(columns=['Ride_Id', 'Lap', 'Lap_Dist', 'Lap_Time', 'Lap_Max_Speed', 'Lap_cals', 'Lap_cad', 'Lap_avg_watts', 'Lap_max_watts', 'ascent', 'descent', 'Lap_Avg_Speed'])
trackpoints_master = pd.DataFrame(columns=['Ride_Id', 'Lap', 'Time', 'Lat', 'Long', 'Alt', 'Speed', 'Watts', 'Alt_Change', 'ascent/descent'])

id_element = 0
for file in file_names:
    ride_df = pd.DataFrame(columns=['Ride_Id'])
    lap_df = pd.DataFrame(columns=['Ride_Id', 'Lap', 'Lap_Dist', 'Lap_Time', 'Lap_Max_Speed', 'Lap_cals', 'Lap_cad', 'Lap_avg_watts', 'Lap_max_watts'])
    trackpoints_df = pd.DataFrame(columns=['Ride_Id', 'Lap', 'Time', 'Lat', 'Long', 'Alt', 'Speed', 'Watts'])
    tree = ET.parse(file)
    root = tree.getroot()
    id_element = id_element + 1
    activities = root.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity')
    for activity in activities:
        data = {'Ride_Id': id_element}
        tmp_ride = pd.DataFrame(data, index=[0])
        ride_df = pd.concat([ride_df, tmp_ride])
        laps = activity.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap')
        for lap in laps:
            lap_start_time = lap.attrib['StartTime']
            lap_dist_element = lap.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}DistanceMeters')
            lap_dist = lap_dist_element.text if lap_dist_element is not None else '0'
            lap_time_element = lap.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}TotalTimeSeconds')
            lap_time = lap_time_element.text if lap_time_element is not None else '0'
            lap_speed_element = lap.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}MaximumSpeed')
            lap_speed = lap_speed_element.text if lap_speed_element is not None else '0'
            lap_cal_element = lap.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Calories')
            lap_cal = lap_cal_element.text if lap_cal_element is not None else '0'
            lap_cad_element = lap.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Cadence')
            lap_cad = lap_cad_element.text if lap_cad_element is not None else '0'
            lap_avg_watts_element = lap.find('.//{http://www.garmin.com/xmlschemas/ActivityExtension/v2}AvgWatts')
            lap_avg_watts = lap_avg_watts_element.text if lap_avg_watts_element is not None else '0'
            lap_max_watts_element = lap.find('.//{http://www.garmin.com/xmlschemas/ActivityExtension/v2}MaxWatts')
            lap_max_watts = lap_max_watts_element.text if lap_max_watts_element is not None else '0'
            data = {
                    'Ride_Id': id_element,
                    'Lap': lap_start_time,
                    'Lap_Dist': lap_dist,
                    'Lap_Time': lap_time,
                    'Lap_Max_Speed': lap_speed,
                    'Lap_cals': lap_cal,
                    'Lap_cad': lap_cad,
                    'Lap_avg_watts': lap_avg_watts,
                    'Lap_max_watts': lap_max_watts
            }
            tmp_lap = pd.DataFrame(data, index=[0])
            lap_df = pd.concat([lap_df, tmp_lap])

            points = lap.findall('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint')
            for trackpoint in points:
                time_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time')
                time = time_element.text if time_element is not None else '0'
                latitude_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees')
                latitude = latitude_element.text if latitude_element is not None else '0'
                longitude_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees')
                longitude = longitude_element.text if longitude_element is not None else '0'
                altitude_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}AltitudeMeters')
                altitude = altitude_element.text if altitude_element is not None else '0'
                speed_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Speed')
                speed = speed_element.text if speed_element is not None else '0'
                watts_element = trackpoint.find('.//{http://www.garmin.com/xmlschemas/ActivityExtension/v2}Watts')
                watts = watts_element.text if watts_element is not None else '0'
                # print(f"Time: {time}, Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}, Distance: {distance}, Speed: {speed}, Watts: {watts}")
                data = {
                    'Ride_Id': id_element,
                    'Lap': lap_start_time,
                    'Time': time,
                    'Lat': latitude,
                    'Long': longitude,
                    'Alt': altitude,
                    # 'Dist': distance,
                    'Speed': speed,
                    'Watts': watts
                }
                tmp = pd.DataFrame(data, index=[0])
                trackpoints_df = pd.concat([trackpoints_df, tmp])
    laps = lap_df['Lap'].unique()
    laps = laps.tolist()
    laps_dict = {f'{value}': index for index, value in enumerate(laps)}
    trackpoints_df['Lap'].replace(laps_dict, inplace=True)
    lap_df['Lap'].replace(laps_dict, inplace=True)
    if trackpoints_df['Lap'].min() == 0:
        trackpoints_df['Lap'] = trackpoints_df['Lap'] + 1
    if lap_df['Lap'].min() == 0:
        lap_df['Lap'] = lap_df['Lap'] + 1

    # trackpoints
    trackpoints_df['Ride_Id'] = trackpoints_df['Ride_Id'].astype(float)
    trackpoints_df['Lap'] = trackpoints_df['Lap'].astype(float)
    trackpoints_df['Time'] = pd.to_datetime(trackpoints_df['Time'])
    trackpoints_df['Lat'] = trackpoints_df['Lat'].astype(float)
    trackpoints_df['Long'] = trackpoints_df['Long'].astype(float)   # does this truncate a whole bunch of decimals??
    trackpoints_df['Alt'] = trackpoints_df['Alt'].astype(float)
    trackpoints_df['Speed'] = trackpoints_df['Speed'].astype(float)     # This is in meters per second
    trackpoints_df['Watts'] = trackpoints_df['Watts'].astype(float)
    trackpoints_df['Alt_Change'] = trackpoints_df['Alt'].diff()
    trackpoints_df['ascent/descent'] = trackpoints_df['Alt_Change'].apply(lambda x: 'ascent' if x > 0 else 'descent' if x < 0 else '')

    # Lap_df
    lap_df['Ride_Id'] = lap_df['Ride_Id'].astype(float)
    lap_df['Lap'] = lap_df['Lap'].astype(float)
    lap_df['Lap_Dist'] = m_to_miles(lap_df['Lap_Dist'].astype(float))
    lap_df['Lap_Dist'] = lap_df['Lap_Dist'].astype(float)
    lap_df['Lap_Time'] = lap_df['Lap_Time'].astype(float) / 60
    lap_df['Lap_Max_Speed'] = lap_df['Lap_Max_Speed'].astype(float) * 3600 / 1609.34
    lap_df['Lap_cals'] = lap_df['Lap_cals'].astype(float)
    lap_df['Lap_cad'] = lap_df['Lap_cad'].astype(float)
    lap_df['Lap_avg_watts'] = lap_df['Lap_avg_watts'].astype(float)
    lap_df['Lap_max_watts'] = lap_df['Lap_max_watts'].astype(float)

    elevation = trackpoints_df[['Ride_Id', 'Lap', 'Alt_Change', 'ascent/descent']].groupby(['Ride_Id', 'Lap', 'ascent/descent'], as_index=False).sum('Alt_Change')
    elevation = pd.pivot(elevation, index=['Ride_Id', 'Lap'], columns='ascent/descent', values='Alt_Change').reset_index()
    elevation = elevation[['Ride_Id', 'Lap', 'ascent', 'descent']].reset_index()

    lap_df = pd.merge(lap_df, elevation, how='left', on=['Ride_Id', 'Lap'])
    lap_df = lap_df.drop(columns='index')

    laps_tmp = lap_df.drop_duplicates(subset='Lap', keep='first')
    laps_tmp['lap_avg_speed'] = (laps_tmp['Lap_Dist'] / (laps_tmp['Lap_Time'] / 60)).astype(float)
    lap_df['Lap_Avg_Speed'] = lap_df['Lap'].map(laps_tmp.set_index('Lap')['lap_avg_speed'])

    # ride_df
    ride_dist = laps_tmp['Lap_Dist'].sum()
    ride_max_speed = laps_tmp['Lap_Max_Speed'].max()
    ride_cals = laps_tmp['Lap_cals'].sum()
    ride_cad = laps_tmp['Lap_cad'].mean()
    ride_time = laps_tmp['Lap_Time'].sum()
    ride_avg_watts = trackpoints_df['Watts'].mean()
    ride_max_watts = laps_tmp['Lap_max_watts'].max()
    ride_ascent = laps_tmp['ascent'].astype(float).sum()
    ride_descent = laps_tmp['descent'].astype(float).sum()
    ride_df['Ride_Dist'] = ride_dist.astype(float)
    ride_df['Ride_Max_Speed'] = ride_max_speed.astype(float)
    ride_df['Ride_Cals'] = ride_cals.astype(float)
    ride_df['Ride_Avg_Cad'] = ride_cad.astype(float)
    ride_df['Ride_Time'] = ride_time.astype(float)
    ride_df['Ride_Avg_Speed'] = ride_dist.astype(float) / (ride_time.astype(float) / 60)
    ride_df['Ride_avg_watts'] = ride_avg_watts.astype(float)
    ride_df['Ride_max_watts'] = ride_max_watts.astype(float)
    ride_df['ride_ascent'] = ride_ascent.astype(float)
    ride_df['ride_descent'] = ride_descent.astype(float)

    trackpoints_master = pd.concat([trackpoints_master, trackpoints_df])
    laps_master = pd.concat([laps_master, lap_df])
    rides_master = pd.concat([rides_master, ride_df])

ride_dates = trackpoints_master.drop_duplicates(subset='Ride_Id', keep='first')[['Ride_Id', 'Time']]
ride_dates['Time'] = ride_dates['Time'].apply(lambda x: x.strftime('%Y-%m-%d'))
rides_master = pd.merge(rides_master, ride_dates, how='left', on='Ride_Id')
rides_master = rides_master.rename(columns={'Time': 'Ride_Date'})

rides_master.to_csv('output/rides.csv', index=False)
laps_master.to_csv('output/laps.csv', index=False)
trackpoints_master.to_csv('output/trackpoints.csv', index=False)
print('complete')

# merged = pd.merge(trackpoints_master, laps_master, on=['Ride_Id', 'Lap'], how='left')
# merged = pd.merge(merged, rides_master, on='Ride_Id', how='left')
# merged.to_csv('output/merged.csv')

