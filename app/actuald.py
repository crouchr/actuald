#!/usr/bin/python3
# Stockcross height is 129m
# https://getoutside.ordnancesurvey.co.uk/local/stockcross-west-berkshire
# 1000 api calls per day is limit of free account

import time
from pprint import pprint
import sys

import current_weather
import connect_db
import locations
import actuald_funcs



# fixme - add exception handling
def insert_rec_to_db(mydb, mycursor, weather_info):
    """
    Insert record into database
    :param weather_info:
    :return:
    """

    sql = "INSERT INTO actual (" \
          "ts_local, " \
          "ts_utc, " \
          "julian, " \
          "hour_utc, " \
          "location, " \
          "main, " \
          "description, " \
          "pressure, " \
          "wind_speed, " \
          "wind_deg, " \
          "wind_quadrant, " \
          "wind_strength, " \
          "wind_gust, " \
          "temp, " \
          "feels_like, " \
          "dew_point, " \
          "uvi, " \
          "humidity, " \
          "coverage, " \
          "visibility, " \
          "rain, " \
          "snow, " \
          "source," \
          "lat, " \
          "lon, " \
          "tz, " \
          "tz_offset, " \
          "ts_epoch, " \
          "sunrise_local, " \
          "sunset_local" \
          ") " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    val = (weather_info['ts_local'],
           weather_info['ts_utc'],
           weather_info['julian'],
           weather_info['hour_utc'],
           weather_info['location'],
           weather_info['main'],
           weather_info['description'],
           weather_info['pressure'],
           weather_info['wind_speed'],
           weather_info['wind_deg'],
           weather_info['wind_quadrant'],
           weather_info['wind_strength'],
           weather_info['wind_gust'],
           weather_info['temp'],
           weather_info['feels_like'],
           weather_info['dew_point'],
           weather_info['uvi'],
           weather_info['humidity'],
           weather_info['coverage'],
           weather_info['visibility'],
           weather_info['rain'],
           weather_info['snow'],
           weather_info['source'],
           weather_info['lat'],
           weather_info['lon'],
           weather_info['tz'],
           weather_info['tz_offset'],
           weather_info['ts_epoch'],
           weather_info['sunrise_local'],
           weather_info['sunset_local']
           )

    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted into MySQL database OK")


def main():
    api_calls = 0
    start_time = time.time()
    sleep_secs = 600        # normal poll every 10 minutes

    try:
        log_msg = "actuald started"
        print(log_msg)

        db_hostname = actuald_funcs.get_db_hostname()
        stage = actuald_funcs.get_stage()
        version = actuald_funcs.get_version()   # container version
        if stage == 'DEV' or stage == 'IDE':
            sleep_secs = 10
            print("stage=" + stage + " caused sleep_secs to be modified to " + sleep_secs.__str__() + " secs")


        mydb, mycursor = connect_db.connect_database(db_hostname, "metminidb")

        while True:
            print("---------------")
            print("Local time (not UTC) : " + time.ctime())
            print("SQL database hosted on : " + db_hostname)
            print("Stage : " + stage)
            print("version : " + version)

            for place in locations.locations:
                flag, weather_info = current_weather.get_current_weather_info(place['location'], place['lat'], place['lon'])
                api_calls += 1
                if flag:                            # API data read OK
                    pprint(weather_info)
                    insert_rec_to_db(mydb, mycursor, weather_info)
                    log_msg = "Read OpenWeatherAPI data OK for " + place['location'].__str__()
                    print(log_msg)
                    time.sleep(5)                   # crude rate-limit
                else:                               # API data not read OK
                    log_msg = "main() : error : failed to read API weather data for " + place['location'].__str__()
                    sleep_secs_short = 120         # wait to let flaky home network connectivity restore
                    print(log_msg)
                    print("short waiting...")
                    time.sleep(sleep_secs_short)

            # update stats
            now = time.time()
            running_time = int(now - start_time)
            api_calls_per_day = actuald_funcs.calc_api_calls(len(locations.locations), sleep_secs)
            print("stats => version=" + version + ", " + api_calls.__str__() + " API call(s) in " + running_time.__str__() +
                  " secs, estimated api_calls_per_day=" + api_calls_per_day.__str__())

            if (stage == 'DEV' or stage == 'IDE') and api_calls >= 10:
                print("stage=" + stage + ", container exiting to not abuse API limit")
                sys.exit(1)

            print("waiting...")
            time.sleep(sleep_secs)

    except Exception as e:
        log_msg = "main() : error : " + e.__str__()
        print(log_msg)


if __name__ == '__main__':
    main()
