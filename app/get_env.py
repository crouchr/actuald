# environment
import os


def get_version():
    if 'VERSION' in os.environ:
        version = os.environ['VERSION']
    else:
        version = 'IDE'  # i.e. running in PyCharm

    return version


def get_stage():
    if 'STAGE' in os.environ:
        stage = os.environ['STAGE']
    else:
        stage = 'IDE'  # i.e. running in PyCharm

    return stage


def get_db_hostname():
    if 'SQL_DB_HOSTNAME' in os.environ:
        hostname = os.environ['SQL_DB_HOSTNAME']
    else:
        hostname = '192.168.1.15'  # xw6600 - dev machine

    return hostname


def get_open_weather_api_key():
    if 'OPEN_WEATHER_API_KEY' in os.environ:
        api_key = os.environ['OPEN_WEATHER_API_KEY']
    else:
        api_key = None
    return api_key