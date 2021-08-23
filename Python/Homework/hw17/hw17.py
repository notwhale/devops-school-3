#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать скрипт, который будет вытаскивать gps данные
из фотографии (jpg файл) и передавать их на вход программе
из hw16.txt
"""

import os
import csv
from GPSPhoto import gpsphoto

def get_files(ext):
    return [file for file in os.listdir('.') if os.path.isfile(file) and file.lower().endswith(ext)]

def gps_to_deg(coordinates):
    result = []
    for coord in coordinates:
        degrees = int(coord)
        minutes = int(abs(coord - degrees) * 60)
        result.append(f"{degrees},{minutes}'")
    return result


def extract_gps(filename):
    gps = gpsphoto.getGPSData(filename)
    if gps:
        return [gps['Latitude'], gps['Longitude']]

def save_gps(filename, row):
    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(row)

if __name__ == "__main__":
    out_file = '../hw16/hw17.csv'
    images = get_files('jpg')
    if images:
        gps_deg = []
        for image in images:
            gps_list = extract_gps(image)
            gps_deg.append(gps_to_deg(gps_list))
        save_gps(out_file, gps_deg)
        print(f'Geodata has been written in "{out_file}"')
    else:
        print('No jpg files found.')
