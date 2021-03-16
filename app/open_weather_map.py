#!/usr/bin/python3
# Use Open Weather API to get current weather

import requests
import json
from datetime import datetime

# my modules from web.ermin
import metfuncs

# my modules
import julian
import time
from pprint import pprint
import ts_funcs
import call_rest_api
import map_location_to_code
import get_env

# Stockcross height is 129m
# https://getoutside.ordnancesurvey.co.uk/local/stockcross-west-berkshire
# https://stackabuse.com/how-to-get-the-current-date-and-time-in-python/


# Leave out daily forecast for now
# need to call this a couple of times in order to determine if pressure is rising, falling etc
def get_current_weather_info(location, lat, lon, uuid):
    """

    :return:
    """
    # Free version - FIXME : read from an ENV var

    #api_key = get_env.get_open_weather_api_key()
    api_key = 'ab4b5be3e0bf875659c638ded9decd79'
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric&exclude=minutely,hourly,daily" % (lat, lon, api_key)

    light_service_endpoint = 'http://192.168.1.180:9503'

    try:
        weather_info = {}
        flag = True
        weather_info['met_source'] = "OpenWeatherMap"       # allows for multiple APIs to be used plus Vantage or other logging weather station

        # query for Light Level
        query = {}
        query['app_name'] = 'actuald'
        query['uuid'] = uuid.__str__()

        weather_info['uuid'] = uuid.__str__()

        utc_now = datetime.utcnow()
        hour_utc = utc_now.hour
        weather_info['hour_utc'] = hour_utc
        #print("hour_utc : " + hour_utc.__str__())

        response = requests.get(url)

        data = json.loads(response.text)

        print("status_code=" + response.status_code.__str__() + ", REST API response from OpenWeatherAPI : " + data.__str__())
        time.sleep(2)                   # crude rate limit

        weather_info['lat']           = data['lat']
        weather_info['lon']           = data['lon']
        weather_info['tz']            = data['timezone']
        weather_info['tz_offset']     = data['timezone_offset']

        weather_info['ts_epoch']      = data['current']['dt']            # api = timestamp from the API in UNIX UTC
        weather_info['ts_local']      = ts_funcs.epoch_to_local(data['current']['dt'])
        weather_info['ts_utc']        = ts_funcs.epoch_to_utc(data['current']['dt'])

        weather_info['julian']        = julian.get_julian_date(weather_info['ts_utc'] )

        weather_info['sunrise_local'] = ts_funcs.epoch_to_local(data['current']['sunrise'])     # api = timestamp from the API in UNIX UTC
        weather_info['sunset_local']  = ts_funcs.epoch_to_local(data['current']['sunset'])      # api = timestamp from the API in UNIX UTC

        weather_info['pressure']      = round(float(data['current']['pressure']), 1)            # api = sea-level hPa
        weather_info['wind_speed']    = round(metfuncs.m_per_sec_to_knots(data['current']['wind_speed']), 1)   # api = metres/s

        # call to light-service to get light levels - if Stockcross
        if location == 'Stockcross, UK':
            status_code, response_dict = call_rest_api.call_rest_api(light_service_endpoint + '/get_lux', query)
            weather_info['light'] = response_dict['lux']
            weather_info['light_condition'] = response_dict['sky_condition']
        else:
            weather_info['light'] = -1.0
            weather_info['light_condition'] = 'not applicable'

        # api returns m/s
        weather_info['wind_strength'] = metfuncs.kph_to_beaufort(metfuncs.metres_per_sec_to_kph(data['current']['wind_speed'])) # metres/s

        weather_info['wind_deg']      = data['current']['wind_deg']
        weather_info['wind_quadrant'] = metfuncs.wind_deg_to_quadrant(weather_info['wind_deg'])
        weather_info['wind_rose']     = '---'   # fixme - not yet implemented
        weather_info['temp']          = round(data['current']['temp'], 1)
        weather_info['feels_like']    = round(data['current']['feels_like'], 1)
        weather_info['dew_point']     = round(data['current']['dew_point'], 1)
        weather_info['humidity']      = data['current']['humidity']     # percent
        weather_info['coverage']      = data['current']['clouds']       # percent
        weather_info['visibility']    = data['current']['visibility']   # average (metres)

        weather_info['location']      = location            # how close ?
        weather_info['location_code'] = map_location_to_code.map_location_to_code(location)

        # optional fields ?
        if 'wind_gust' in data['current']:
            weather_info['wind_gust'] = round(metfuncs.m_per_sec_to_knots(data['current']['wind_gust']) ,1)
        else:
            weather_info['wind_gust'] = 0.0

        # if 'rain.1h' in data['current']:
        #     weather_info['rain']  = round(data['current']['rain.1h'], 1)      # rain volume for last hour (mm)
        # else:
        #     weather_info['rain'] = 0.0
        # FIXME : 'rain' and 'snow' parsing yet to be checked
        if 'rain' in data['current']:
            weather_info['rain'] = round(data['current']['rain']['1h'], 1)      # rain volume for last hour (mm)
        else:
            weather_info['rain'] = 0.0

        if 'snow' in data['current']:
            weather_info['snow'] = round(data['current']['snow']['1h'], 1)      # snow volume for last hour (mm)
        else:
            weather_info['snow'] = 0.0

        if 'uvi' in data['current']:
            weather_info['uvi'] = data['current']['uvi']    # UV index
        else:
            weather_info['uvi'] = 0.0

        weather_info['synopsis']   = 'reserved'     # New function to go into forecast-service - i.e. how is current weather summarised from known conditions
        weather_info['synopsis_code'] = -999        # New function to go into forecast-service

        weather_info['image_name'] = 'reserved'     # taken from webcam-service when implemented
        weather_info['video_name'] = 'reserved'     # taken from webcam-service when implemented

        # fixme - this is a list - so need to store it as a list ? - store a assume a single item list for now until understand the API response more
        weather_info['main']          = data['current']['weather'][0]['main']
        weather_info['description']   = data['current']['weather'][0]['description']
        weather_info['condition_code'] = data['current']['weather'][0]['id'] # use OpenWeather IDs for all

        if 'alerts' in data:
            alert_sender = data['alerts'][0]['sender_name']
            if alert_sender == 'Go to UK Met Office':           # what a shit name !
                alert_sender = 'UK Met Office'
            weather_info['alert_sender'] = alert_sender
            weather_info['alert_event']  = data['alerts'][0]['event']
            #weather_info['alert_description'] = data['alerts'][0]['description']
        else:
            weather_info['alert_sender'] = 'none'
            weather_info['alert_event']  = 'none'

        return flag, weather_info

    except Exception as e:
        print('get_current_weather_info() : uuid=' + uuid.__str__() + ', error : ' + e.__str__())
        return False, None
