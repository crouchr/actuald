#!/usr/bin/python3
# Stockcross height is 129m
# https://getoutside.ordnancesurvey.co.uk/local/stockcross-west-berkshire

import time
from pprint import pprint
import syslog
import os

import current_weather
import connect_db
import locations


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
    print(mycursor.rowcount, "record inserted in MySQL OK")


def main():
    try:
        log_msg = "metmini-backend started"
        syslog.syslog(log_msg)

        hostname = os.environ['SQL_DB_HOSTNAME']
        print('SQL database hostname : ' + hostname.__str__())
        mydb, mycursor = connect_db.connect_database(hostname, "metminidb")

        while True:
            print("-----------------")
            print("Local time (not UTC) : " + time.ctime())
            for place in locations.locations:
                flag, weather_info = current_weather.get_current_weather_info(place['location'], place['lat'], place['lon'])

                if flag:                # API data read OK
                    pprint(weather_info)
                    insert_rec_to_db(mydb, mycursor, weather_info)
                    log_msg = "Read API weather data OK for " + place['location'].__str__()
                    #syslog.syslog(log_msg)
                    print(log_msg)
                    time.sleep(5)       # crude rate-limit
                else:                   # API data not read OK
                    log_msg = "ERROR : failed to read API weather data for " + place['location'].__str__()
                    sleep_secs = 60         # wait a minute to let network fault restore
                    #syslog.syslog(log_msg)
                    print(log_msg)
                    print("short waiting...")
                    time.sleep(sleep_secs)

            sleep_secs = 600    # normal poll every 10 minutes
            print("waiting...")
            time.sleep(sleep_secs)

    except Exception as e:
        log_msg = "metmini-backed : exception : " + e.__str__()
        #syslog.syslog(log_msg)
        print(log_msg)


if __name__ == '__main__':
    main()
