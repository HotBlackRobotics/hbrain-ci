#!/bin/bash

service nginx start
uwsgi ./uwsgi-hbr.ini &
roslaunch rosbridge_server rosbridge_websocket.launch
