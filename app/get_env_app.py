# environment
import os


def get_db_hostname():
    if 'SQL_DB_HOSTNAME' in os.environ:
        hostname = os.environ['SQL_DB_HOSTNAME']
    else:
        hostname = '192.168.1.5'        # Use Test MySQL on Dev workstation
        hostname = '192.168.1.180'      # Use Test MySQL on Dev workstation

    return hostname


def get_open_weather_api_key():
    if 'OPEN_WEATHER_API_KEY' in os.environ:
        api_key = os.environ['OPEN_WEATHER_API_KEY']
    else:
        api_key = None
    return api_key
