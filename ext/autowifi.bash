#!/bin/bash
source /opt/hbrain/bin/activate
wifi autoconnect
sleep 2
service nginx restart
