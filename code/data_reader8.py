#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2019-03-27 VKT Version 1.0
"""
"""
Description:
    Simple example python class for loading data from csv files and plotting data.
License: BSD 3-Clause
"""

### Import start
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pow
### Import end

### Class start
class data_loader():
    def __init__(self, inFileName, debug = False):
        self.fileName = inFileName;

        # Prepare containers for the data
        self.TimestampS = []
        self.TimestampSv = []
        self.AccelerometerXS = []
        self.AccelerometerYS = []
        self.AccelerometerZS = []
        self.GyroscopeXS = []
        self.GyroscopeYS= []
        self.GyroscopeZS = []
        self.ParaTimestampS = []
        self.ParaTriggerS = []
        self.velX = []
        self.velY = []
        self.velZ = []
	
        # remember to add class definitions for variables
		#self.BarometerXS
        # Print debug value
        self.debugText = debug
    def loadCSV_vel(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print ('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampSv.append(TimestampS)
                velcX = float(row['rollspeed'])
                self.velX.append(velcX)
                velcY = float(row['pitchspeed'])
                self.velY.append(velcY)
                velcZ = float(row['yawspeed'])
                self.velZ.append(velcZ)

            if self.debugText:
                print ('Data loaded')
    def loadCSV_para(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print ('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                ParaTimestampS = float(row['timestamp'])/1000000
                self.ParaTimestampS.append(ParaTimestampS)
                ParaTrigger = float(row['aux1']) * -20
                self.ParaTriggerS.append(ParaTrigger)

            if self.debugText:
                print ('Data loaded');

    def loadCSV_accel(self):
        with open(self.fileName) as csvfile:
            if self.debugText:
                print ('Data file opened, attempting data load')
            readCSV = csv.DictReader(csvfile, delimiter=',')

            for row in readCSV:
                TimestampS = float(row['timestamp'])/1000000
                self.TimestampS.append(TimestampS)
                AccelerometerX = float(row['accelerometer_m_s2[0]'])
                self.AccelerometerXS.append(AccelerometerX)
                AccelerometerY = float(row['accelerometer_m_s2[1]'])
                self.AccelerometerYS.append(AccelerometerY)
                AccelerometerZ = float(row['accelerometer_m_s2[2]'])
                self.AccelerometerZS.append(AccelerometerZ)
                GyroscopeX = float(row['gyro_rad[0]'])
                self.GyroscopeXS.append(GyroscopeX);
                GyroscopeY = float(row['gyro_rad[1]'])
                self.GyroscopeYS.append(GyroscopeY);
                GyroscopeZ = float(row['gyro_rad[2]'])
                self.GyroscopeZS.append(GyroscopeZ);

            if self.debugText:
                print ('Data loaded')

    # Extend class with more methods for loading different kind of csv files..
    # e.g loading 'TEST9_08-02-19_telemetry_status_0.csv':
    #
    # loadCSV_telemetry_status(self):
    #    with open(self.fileName) as csvfile:
    #       if self.debugText:
    #           print 'Data file opened, attempting data load'
    #       readCSV = csv.DictReader(csvfile, delimiter=',')
    #       for row in readCSV:
    #       TelemTimestampS = float(row['timestamp'])/1000000
    #       self.TelemTimestampS.append(ParaTimestampS)
    #       RXerrors = float(row['rxerrors'])
    #       self.RXerrorsS.append(RXerrors)
    #
    # (...)




### Class end - Main start

threshold = 20;
thresholdG = 5;

if __name__ == '__main__':

    SENSOR_COMBINED = 'files/TEST8_30-01-19/TEST8_30-01-19_sensor_combined_0.csv'
    MANUAL_CONTROLLED_SETPOINT = 'files/TEST8_30-01-19/TEST8_30-01-19_manual_control_setpoint_0.csv'
    vehicle_attitude = 'files/TEST8_30-01-19/TEST8_30-01-19_vehicle_attitude_0.csv'

    # Initialize and load data
    reader = data_loader(
        SENSOR_COMBINED,
        debug = True
    )
    reader.loadCSV_accel()
    reader1 = data_loader(
        vehicle_attitude,
        debug = True)   
 
    reader1.loadCSV_vel()
    
    trigger = data_loader(
        MANUAL_CONTROLLED_SETPOINT,
        debug = True
    )
    
    trigger.loadCSV_para()
    trigger_data = []
    k = 0
    SantasLittleHelper = False;
    # Add readers for the additional files you want to load...
    for i in range(len(reader.AccelerometerXS)):
        accX = reader.AccelerometerXS[i];
        accY = reader.AccelerometerYS[i];
        accZ = reader.AccelerometerZS[i];
        gX = reader.GyroscopeXS[i];
        gY = reader.GyroscopeYS[i];
        gZ = reader.GyroscopeZS[i];
        
        if(((-threshold > accX) or (accX > threshold)) or ((-threshold > accY) or (accY > threshold)) or ((-threshold > accZ) or (accZ > threshold))):
            if(((-thresholdG > gX) or (gX > thresholdG)) or ((-thresholdG > gY) or (gY > thresholdG)) or ((-thresholdG > gZ) or (gZ > thresholdG))):
                if(SantasLittleHelper == False):
                    trigger_data.append(20.0)
                    #print("hej")
                    SantasLittleHelper = True
                else:
                    trigger_data.append(20);
            else:
            	if(SantasLittleHelper == True):
            	    trigger_data.append(20.0)
            	else:
                   trigger_data.append(-20.0)
        else:
            if(SantasLittleHelper == True):
                trigger_data.append(20.0);
            else:
                trigger_data.append(-20.0)


    #print(trigger.ParaTriggerS)
#if(# You can likewise plot these failure detection parameters (with the same timestamp as the investigated dataset) together with the logged data.
    fig, ax = plt.subplots()

    # acceleration plot:
    #ax.plot(reader.TimestampS, reader.AccelerometerXS, linewidth=0.5, label='accel_x')
    #ax.plot(reader.TimestampS, reader.AccelerometerYS, linewidth=0.5, label='accel_y')
    #ax.plot(reader.TimestampS, reader.AccelerometerZS, linewidth=0.5, label='accel_z')
    # parachute trigger plot:
    ax.plot(trigger.ParaTimestampS, trigger.ParaTriggerS, linewidth=1, label='para_trigger')
    ax.plot(reader.TimestampS, trigger_data, linewidth=1, label='OurTrigger')
    # Add more plots or create new plots for additional data loaded...
    #ax.plot(reader.TimestampS, reader.GyroscopeXS, linewidth=0.5, label='ygro_x')
    #ax.plot(reader.TimestampS, reader.GyroscopeYS, linewidth=0.5, label='gyro_y')
    #ax.plot(reader.TimestampS, reader.GyroscopeZS, linewidth=0.5, label='gyro_z')
#    ax.plot(reader1.TimestampSv, reader1.velX, linewidth=0.5, label='vel_x')
#    ax.plot(reader1.TimestampSv, reader1.velY, linewidth=0.5, label='vel_y')
#    ax.plot(reader1.TimestampSv, reader1.velZ, linewidth=0.5, label='vel_z')
    # plot settings
    ax.set(xlabel='time (s)', ylabel='Trigger level',
       title='Failure detection for Test 8')
    legend = ax.legend(loc='best', shadow=True, fontsize='medium')
    ax.grid()
    
    plt.show()
### Main end
