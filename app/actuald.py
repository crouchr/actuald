#!/usr/bin/python3
# Stockcross height is 129m
# https://getoutside.ordnancesurvey.co.uk/local/stockcross-west-berkshire
# 1000 api calls per day is limit of free account

import time
import os
from pprint import pprint
import uuid
import traceback
import sys

# artifacts (metminifuncs)
import sync_start_time
import jena_data
import append_mlearning_rec

import get_env
import get_env_app
import open_weather_map
import connect_db
import locations
import actuald_funcs
import db_funcs
import append_actual_rec
import append_mlearning_rec
import definitions


def main():
    api_calls = 0
    start_time = time.time()
    mins_between_updates = 10        # normal poll every 10 minutes

    try:
        print("actuald started, version=" + get_env.get_version())
        stage = get_env.get_stage()
        container_version = get_env.get_version()  # container version
        db_hostname = get_env_app.get_db_hostname()
        actual_log_filename = definitions.WEATHER_INFO_DIR + 'actuald.tsv'
        mlearning_log_filename = definitions.MLEARNING_DIR + 'mlearning.csv'

        mydb, mycursor = connect_db.connect_database(db_hostname, "metminidb")
        if mydb is None:
            print('Failed to connect to database so aborting...')
            sys.exit(-1)
        print("SQL database hosted on : " + db_hostname)
        print("Stage : " + stage)
        print("container_version : " + container_version)
        print('actual_log_filename=' + actual_log_filename)
        print('mlearning_log_filename=' + mlearning_log_filename)

        while True:
            try:
                print('waiting to sync main loop...')
                sync_start_time.wait_until_minute_flip(10)      # comment out when debugging
                print('---------------------------------')
                start_secs = time.time()
                mlearning_record_timestamp = jena_data.get_jena_timestamp()
                actual_record_timestamp = time.ctime()      # FIXME :need to make this UTC

                for place in locations.locations:
                    this_uuid = uuid.uuid4().__str__()
                    flag, weather_info = open_weather_map.get_current_weather_info(place['location'], place['lat'], place['lon'], this_uuid.__str__())
                    api_calls += 1
                    if flag:
                        print("Read OpenWeatherMap API data OK for " + place['location'].__str__() + ', uuid=' + this_uuid.__str__())  # API data read OK
                        pprint(weather_info)
                        db_funcs.insert_rec_to_db(mydb, mycursor, weather_info, container_version)
                        if place['location'] == 'Stockcross, UK':
                            append_actual_rec.append_weather_info(actual_log_filename, weather_info, actual_record_timestamp, container_version)      # add to continuous file
                            append_mlearning_rec.append_mlearning_info(mlearning_log_filename, weather_info, mlearning_record_timestamp)                    # data for Machine learning
                        time.sleep(5)                   # crude rate-limit
                    else:                               # API data not read OK
                        log_msg = 'main() : uuid=' + this_uuid.__str__() + ', error : failed to read API weather data for ' + place['location'].__str__()
                        sleep_secs_short = 120          # wait to let flaky home network connectivity restore
                        print(log_msg)
                        print("short waiting...")
                        time.sleep(sleep_secs_short)

                # update stats
                now = time.time()
                running_time = int(now - start_time)
                api_calls_per_day = actuald_funcs.calc_api_calls(len(locations.locations), mins_between_updates * 60)
                print("stats => version=" + container_version + ", " + api_calls.__str__() + " API call(s) in " + running_time.__str__() +
                      " secs, estimated api_calls_per_day=" + api_calls_per_day.__str__())

                stop_secs = time.time()
                sleep_secs = (mins_between_updates * 60) - (stop_secs - start_secs) - 10
                # processing_secs = loop_end_secs - loop_start_secs
                # poll_wait_secs = sleep_secs - processing_secs
                # print('waiting for ' + int(poll_wait_secs).__str__() + ' secs...')
                time.sleep(sleep_secs)

            except Exception as e:
                print('main() inner loop : error : ' + e.__str__())
                print("short waiting...")
                time.sleep(10)
                continue        # go back around the loop again

    except Exception as e:
        log_msg = 'main() 2 : error : ' + e.__str__()
        print(log_msg)
        traceback.print_exc()


if __name__ == '__main__':
    os.environ['PYTHONUNBUFFERED'] = "1"  # does this help with log buffering ?
    main()
