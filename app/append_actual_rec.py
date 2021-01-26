# append a weather record for consumption by 3rd parties e.g. wunderground
import time
import definitions
import traceback


# main + description will be replaced with synopsis in future
def append_weather_info(weather_info, container_version):
    """
    Append a simple record to actuald.tsv

    :param weather_info:
    :return:
    """
    try:
        actual_log_filename = definitions.WEATHER_INFO_DIR + 'actuald.tsv'

        actual_rec = time.ctime() + '\t' +\
            weather_info['met_source'] + '\t' + \
            weather_info['location'] + '\t' + \
            weather_info['location_code'].__str__() + '\t' + \
            weather_info['lat'].__str__() + '\t' + \
            weather_info['lon'].__str__() + '\t' + \
            weather_info['ts_utc'].__str__() + '\t' + \
            container_version.__str__() + '\t' + \
            weather_info['pressure'].__str__() + '\t' + \
            weather_info['temp'].__str__() + '\t' +\
            weather_info['humidity'].__str__() + '\t' +\
            weather_info['wind_deg'].__str__() + '\t' +\
            weather_info['wind_speed'].__str__() + '\t' + \
            weather_info['wind_gust'].__str__() + '\t' + \
            weather_info['rain'].__str__() + '\t' +\
            weather_info['snow'].__str__() + '\t' +\
            weather_info['dew_point'].__str__() + '\t' +\
            weather_info['feels_like'].__str__() + '\t' + \
            weather_info['light'].__str__() + '\t' + \
            weather_info['uvi'].__str__() + '\t' + \
            weather_info['main'] + '(' + weather_info['description'] + ')' + '\t' + \
            weather_info['synopsis_code'].__str__() + '\n'

        print('actual_rec appended to ' + actual_log_filename + ' => ' + actual_rec)

        fp_out = open(actual_log_filename, 'a')
        fp_out.write(actual_rec)
        fp_out.close()
        return True

    except Exception as e:
        traceback.print_exc()
        return False
