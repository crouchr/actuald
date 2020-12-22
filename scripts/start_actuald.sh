#!/bin/bash
set -e

echo 'entered start_actuald.sh'
docker pull registry:5000/actuald:1.0.0
docker-compose --verbose --no-ansi -f /home/crouchr/actuald/dev-actuald-compose.yml kill
echo 'sleeping...'
sleep 10
docker-compose --verbose --no-ansi -f /home/crouchr/actuald/dev-actuald-compose.yml up &
echo 'exited start_actuald.sh'
