#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os
from sys import platform

import requests
from huepy import *

filename = os.path.expanduser('~/.aerovane')
config = configparser.ConfigParser()


class Observation:
    def __init__(self, owm_key, location, units):
        self.owm_key = owm_key
        self.location = location
        self.units = units
        self.url = 'https://api.openweathermap.org/data/2.5/'
        self.query_params = {
            'appid': self.owm_key,
            'q': self.location,
            'units': self.units
        }

    def current_weather(self):
        response = requests.get(self.url + 'weather', params=self.query_params)
        return response.json()

    def get_conditions(self):
        pass

    def get_temp(self):
        pass

    def get_humidity(self):
        pass

    def get_wind(self):
        pass

    def forecast(self):
        params = self.query_params
        params['cnt'] = 3
        response = requests.get(self.url + 'forecast', params=params)
        return response.json()


def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def check_config():
    if os.path.isfile(filename):
        pass
    else:
        clear()
        print('It looks like you have not yet configured', bold(blue('AEROVANE')) + '.')

        owm_key = input('Please enter your OWM API key: ')
        config['OWM_API_KEY'] = {'owm_key': owm_key}

        ipstack_key = input('Please enter your ipstack API key: ')
        config['IPSTACK_API_KEY'] = {'ipstack_key': ipstack_key}

        units_pref = input('Which units would you prefer for your weather report '
                           '(metric (m), imperial(i), or kelvin(k)): ').lower()
        if units_pref == 'm':
            config['UNITS'] = {'units': 'metric'}
        elif units_pref == 'i':
            config['UNITS'] = {'units': 'imperial'}
        elif units_pref == 'k':
            config['UNITS'] = {'units': 'kelvin'}

        with open(filename, 'w') as configfile:
            config.write(configfile)


def parse_config(value):
    response = ''
    config.read(filename)
    if value == 'owm_key':
        response = config['OWM_API_KEY']['owm_key']
    elif value == 'ipstack_key':
        response = config['IPSTACK_API_KEY']['ipstack_key']
    elif value == 'units':
        response = config['UNITS']['units']

    return response


def ip_get_location():
    api_key = parse_config('ipstack_key')

    ipstack_url = 'http://api.ipstack.com/check'
    query_params = {
        'access_key': api_key,
        'format': 1
    }

    response = requests.put(ipstack_url, params=query_params)
    location = response.json()['city'] + ", " + response.json()['country_code']

    return location


def weather_report(observation, units):

    temperature = observation['main']['temp']
    humidity = str(observation['main']['humidity']) + '%'
    wind = observation['wind']['speed']
    status = str(observation['weather'][0]['description'])

    degree_marker = ('°' if platform == 'darwin' else '') + ('C' if units == 'metric' else 'F')
    location_name = observation['name'].upper()

    if temperature > (26.67 if units == 'metric' else 80.0):
        temp = (bold(red('HOT!')), red(str(temperature) + degree_marker))
    elif temperature > (20.0 if units == 'metric' else 68.0):
        temp = (bold(yellow('WARM.')), yellow(str(temperature) + degree_marker))
    elif temperature > (14.44 if units == 'metric' else 58.0):
        temp = (bold(green('COOL.')), green(str(temperature) + degree_marker))
    elif temperature > (8.89 if units == 'metric' else 48.0):
        temp = (bold(lightblue('CHILLY.')), lightblue(str(temperature) + degree_marker))
    else:
        temp = (bold(blue('COLD!')), blue(str(temperature) + degree_marker))

    header = (4 * ' ') + 'YOUR ' + bold(blue('AEROVANE')) + ' WEATHER REPORT FOR ' + \
             bold(blue(location_name.upper())) + (4 * ' ')
    line = '-' * (41 + len(location_name))

    clear()
    print(line)
    print(header)
    print(line)
    print(f'Current weather conditions: {bold(white(status.upper()))}')
    print(f'It\'s {temp[0]} The current temperature is {temp[1]}.')
    print(f'Relative humidity is {green(humidity)}.')
    print(f'The wind speed is {orange(str(round(wind, 2)))}' + (' m/s' if units == 'metric' else ' mph') + '.')
    print(line + '\n')
