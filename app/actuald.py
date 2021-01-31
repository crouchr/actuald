#!/usr/bin/python3
# Stockcross height is 129m
# https://getoutside.ordnancesurvey.co.uk/local/stockcross-west-berkshire
# 1000 api calls per day is limit of free account

import time
import os
from pprint import pprint
import uuid

import get_env
import open_weather_map
import connect_db
import locations
import actuald_funcs
import db_funcs
import append_actual_rec


def main():
    api_calls = 0
    start_time = time.time()
    sleep_secs = 600        # normal poll every 10 minutes

    try:
        print("actuald started, version=" + get_env.get_version())

        db_hostname = get_env.get_db_hostname()
        stage = get_env.get_stage()
        container_version = get_env.get_version()   # container version

        # if stage == 'DEV' or stage == 'IDE':
        #     sleep_secs = 10
        #     print("stage=" + stage + " caused sleep_secs to be modified to " + sleep_secs.__str__() + " secs")

        mydb, mycursor = connect_db.connect_database(db_hostname, "metminidb")

        while True:
            print("---------------")
            print("Local time (not UTC) : " + time.ctime())
            print("SQL database hosted on : " + db_hostname)
            print("Stage : " + stage)
            print("container_version : " + container_version)

            for place in locations.locations:
                uuid = uuid.uuid1()           # make a UUID based on the host ID and current time
                flag, weather_info = open_weather_map.get_current_weather_info(place['location'], place['lat'], place['lon'], uuid)
                api_calls += 1
                if flag:
                    print("Read OpenWeatherMap API data OK for " + place['location'].__str__() + ', uuid=' + uuid)  # API data read OK
                    pprint(weather_info)
                    db_funcs.insert_rec_to_db(mydb, mycursor, weather_info, container_version)
                    if place['location'] == 'Stockcross, UK':
                        append_actual_rec.append_weather_info(weather_info, container_version)     # add to continuous file
                    print(log_msg)
                    time.sleep(5)                   # crude rate-limit
                else:                               # API data not read OK
                    log_msg = 'main() : uuid=' + uuid + ', error : failed to read API weather data for ' + place['location'].__str__()
                    sleep_secs_short = 120         # wait to let flaky home network connectivity restore
                    print(log_msg)
                    print("short waiting...")
                    time.sleep(sleep_secs_short)

            # update stats
            now = time.time()
            running_time = int(now - start_time)
            api_calls_per_day = actuald_funcs.calc_api_calls(len(locations.locations), sleep_secs)
            print("stats => version=" + container_version + ", " + api_calls.__str__() + " API call(s) in " + running_time.__str__() +
                  " secs, estimated api_calls_per_day=" + api_calls_per_day.__str__())

            print("waiting...")
            time.sleep(sleep_secs)

    except Exception as e:
        log_msg = 'main() : uuid=' + uuid + ', error : ' + e.__str__()
        print(log_msg)


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"  # does this help with log buffering ?
    main()
