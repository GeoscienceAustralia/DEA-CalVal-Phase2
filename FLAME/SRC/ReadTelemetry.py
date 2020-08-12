import pandas as pd
from dateutil import parser
from datetime import datetime, timedelta


def read_telemetry(TelemetryFile):

    # Read Telemetry data from csv file
    TeleDat = pd.read_csv(TelemetryFile)

    # These lines can be uncommented and used of more than one Telemetry file exists
    #
    #TeleDat1 = pd.read_csv(TelemetryFile1)
    #TeleDat2 = pd.read_csv(TelemetryFile2)
    #TeleDat = pd.concat([TeleDat1, TeleDat2])
    
    # Remove unwanted fields
    TeleDat.drop(['height_above_ground_at_drone_location(meters)', 
                  'ground_elevation_at_drone_location(meters)',
                  'satellites',
                  'gpslevel',
                  'voltage(v)',
                  'max_altitude(meters)',
                  'max_ascent(meters)',
                  'max_speed(m/s)',
                  'max_distance(meters)',
                  ' xSpeed(m/s)',
                  ' ySpeed(m/s)',
                  ' zSpeed(m/s)',
                  'isPhoto',
                  'isVideo',
                  'rc_elevator',
                  'rc_aileron',
                  'rc_throttle',
                  'rc_rudder',
                  'battery_percent',
                  'voltageCell1',
                  'voltageCell2',
                  'voltageCell3',
                  'voltageCell4',
                  'voltageCell5',
                  'voltageCell6',
                  'current(A)',
                  'battery_temperature(c)',
                  'altitude(meters)',
                  'ascent(meters)',
                  'flycStateRaw',
                  'flycState'], axis=1, inplace=True)
    
    # Rename columns for simplicity and consistency
    TeleDat.rename(columns={'time(millisecond)': 'time_ms',
                            'datetime(utc)': 'datetime',
                            'latitude': 'Latitude',
                            'longitude': 'Longitude',
                            'height_above_takeoff(meters)': 'height_local',
                            'altitude_above_seaLevel(meters)': 'height_sea',
                            'distance(meters)': 'distance(m)',
                            ' compass_heading(degrees)': 'compass_heading',
                            ' pitch(degrees)': 'pitch',
                            ' roll(degrees)': 'roll',
                            'gimbal_heading(degrees)': 'gimbal_heading',
                            'gimbal_pitch(degrees)': 'gimbal_pitch',
                            'message': 'comment'
                           }, inplace=True
                  )
    
    # Ensure datetime column is formatted with datetime objects, rather than strings
    TeleDat['datetime'] = [parser.parse(TeleDat.datetime[i]) for i in range(len(TeleDat.datetime))]

    # Make sure there are no silly times in the telemetry file like 01JAN70
    TeleDat = TeleDat[TeleDat['datetime'] > datetime(2020,1,1)]

    # Identify the line where the datetime entry first progresses by 1 second.
    # Then adjust the fractional seconds to match this timestamp.
    # Create a new column (date_saved) that holds the timestamp with fractional
    # seconds.
    for i in range(11):
        if (TeleDat.datetime[i]-TeleDat.datetime[0]).seconds == 1:
            TimeOffset = int(1000-TeleDat.time_ms[i])
            break
    
    TeleDat['date_saved'] = [TeleDat.datetime.iloc[0] + 
                            timedelta(milliseconds=int(TeleDat.time_ms.iloc[i])) + 
                            timedelta(milliseconds=TimeOffset) 
                            for i in range(len(TeleDat.datetime))]

    return TeleDat
