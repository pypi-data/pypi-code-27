#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from .aerovane import Observation, check_config, parse_config, ip_get_location, weather_report


@click.command()
@click.option('--location', '-l', callback=check_config(), default=ip_get_location(),
              help='Overrides default location based on your IP. Takes a string of city name and two letter country '
                   'code (separated by a comma), for example: \'Los Angeles, US\'.')
@click.option('--units', '-u', callback=check_config(), default=parse_config('units'),
              type=click.Choice(['metric', 'imperial']),
              help='Overrides units preference stored in the config file. Takes either metric or imperial '
                   'as a value.')
def cli(location, units):
    """
    Aerovane is a simple CLI for generating a weather report in your terminal.
    """

    owm_key = parse_config('owm_key')
    aerovane = Observation(owm_key, location, units)
    observation = aerovane.current_weather()
    # forecast = aerovane.forecast()

    weather_report(observation, units)
    # print(observation)
    # print(forecast)

    pass
