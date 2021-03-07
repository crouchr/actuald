# append a weather record for consumption by Machine Learning
# Format is very similar to jena weather training set as per 'Deep Learning with Python' page 207

import definitions
import traceback
import pytz
from datetime import datetime


# https://stackabuse.com/how-to-get-the-current-date-and-time-in-python/
# 2021-03-07 20:55:08.94343+00.00
def get_jena_timestamp():

    utc_current_datetime = datetime.now(pytz.timezone("UTC")).__str__()
    print(utc_current_datetime)
    date_part = utc_current_datetime.split(' ')[0]
    time_part = utc_current_datetime.split(' ')[1].split('.')[0]
    date_parts = date_part.split('-')
    year = date_parts[0]
    month = date_parts[1]
    day = date_parts[2]

    jena_timestamp = day + '.' + month + '.' + year + ' ' + time_part

    return jena_timestamp


# Should be able to import this file direct into the Weather examples in Deep Learning with Python
def append_mlearning_info(weather_info):
    """
    Append a simple record to mlearning.csv

    :param weather_info:
    :return:
    """
    try:
        mlearning_log_filename = definitions.MLEARNING_DIR + 'mlearning.csv'

        mlearning_rec = get_jena_timestamp() + ',' + \
            weather_info['pressure'].__str__() + ',' + \
            weather_info['temp'].__str__() + ',' + \
            weather_info['dew_point'].__str__() + ',' + \
            weather_info['feels_like'].__str__() + ',' + \
            float(weather_info['humidity']).__str__() + ',' + \
            weather_info['wind_speed'].__str__() + ',' + \
            weather_info['wind_gust'].__str__() + ',' + \
            weather_info['wind_deg'].__str__() + '\n'

        print('mlearning_rec appended to ' + mlearning_log_filename + ' => ' + mlearning_rec.rstrip('\n'))

        fp_out = open(mlearning_log_filename, 'a')
        fp_out.write(mlearning_rec)
        fp_out.close()
        return True

    except Exception as e:
        traceback.print_exc()
        return False
