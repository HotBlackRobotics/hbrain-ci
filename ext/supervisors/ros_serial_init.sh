#!/bin/bash
source /opt/hbrain/hbrain-ci/ext/ros.bash
rosrun rosserial_python serial_node.py _port:=/dev/ttyACM0
