#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать программу, которая будет считывать из файла gps координаты,
и формировать текстовое описание объекта и ссылку на google maps.
Пример:

Input data: 60,01';30,19'
Output data:
Location: Теремок, Енотаевская улица, Удельная, округ Светлановское, Выборгский район, Санкт-Петербург, Северо-Западный федеральный округ, 194017, РФ
Goggle Maps URL: https://www.google.com/maps/search/?api=1&query=60.016666666666666,30.322
"""

import os
import csv
import re
from geopy.geocoders import Nominatim

def get_gps(latitude, longitude):
    geo = Nominatim(user_agent="python")
    address = geo.reverse(f"{latitude}, {longitude}")
    google_api = "https://www.google.com/maps/search/?api=1&query="
    result = {'Location': f"{address}", 'Google Maps URL': f"{google_api}{latitude},{longitude}\n"}
    return result

def gps_to_dec(coordinates):
    result = []
    for coord in coordinates:
        gps_input = re.search(r"(?P<degrees>\-?[0-9]+),(?P<minutes>[0-9]+)\'((?P<seconds>([0-9]+[.])?[0-9]+)\'\')?", coord)
        degrees = gps_input.group('degrees')
        minutes = gps_input.group('minutes')
        seconds = gps_input.group('seconds')
        if not seconds:
            seconds = 0
        coord = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
        result.append(coord)
    return result

def gps_from_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f, delimiter=";")
        result = [get_gps(*gps_to_dec(line)) for line in reader]
    return result

def get_files(ext):
    return [file for file in os.listdir('.') if os.path.isfile(file) and file.lower().endswith(ext)]


if __name__ == "__main__":
    csv_files = get_files('csv')
    if csv_files:
        for csv_file in csv_files:
            print(f"\n# {csv_file}")
            geodata = gps_from_csv(csv_file)
            print('\n'.join(
                [f"{key}: {value}"
                    for geo in geodata
                    for key, value in geo.items()]
                ))
    else:
        print('No csv files found.')
