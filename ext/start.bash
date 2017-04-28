#!/bin/bash

service nginx start
uwsgi /hbrain/hbrain_server/uwsgi-hbr.ini &
roslaunch rosbridge_server rosbridge_websocket.launch
