import json

# Urls
# dev: http://localhost:8080/sg-1

# prod: https://sg-api.dss.husqvarnagroup.net/sg-1
#BASE_URL = 'http://localhost:8080/sg-1'
BASE_URL = 'https://sg-api.dss.husqvarnagroup.net/sg-1'

# Paths
SESSIONS_URL = BASE_URL + '/sessions'
LOCATIONS_URL = BASE_URL + '/locations'
DEVICES_URL = BASE_URL + '/devices'

# Commands
CMD_MOWER_PARK_UNTIL_NEXT_TIMER = {'name': 'park_until_next_timer'}
CMD_MOWER_PARK_UNTIL_FURTHER_NOTICE = {'name': 'park_until_further_notice'}
CMD_MOWER_START_RESUME_SCHEDULE = {'name': 'start_resume_schedule'}
CMD_MOWER_START_24HOURS = {
    'name': 'start_override_timer', 'parameters': {'duration': 1440}}
CMD_MOWER_START_3DAYS = {
    'name': 'start_override_timer', 'parameters': {'duration': 4320}}

CMD_SENSOR_REFRESH_TEMPERATURE = {'name': 'measure_ambient_temperature'}
CMD_SENSOR_REFRESH_LIGHT = {'name': 'measure_light'}
CMD_SENSOR_REFRESH_HUMIDITY = {'name': 'measure_humidity'}

CMD_WATERINGCOMPUTER_START_30MIN = {
    'name': 'manual_override', 'parameters': {'duration': 30}}
CMD_WATERINGCOMPUTER_STOP = {'name': 'cancel_override'}
