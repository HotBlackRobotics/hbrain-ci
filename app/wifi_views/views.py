from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import wifi_views

@wifi_views.route("/scan")
def wifi_scan():
    return render_template('wifi/scan.html')

@wifi_views.route("/schemes")
def schemes():
    import subprocess
    wifi_name = subprocess.check_output(["iwconfig", "wlan0"])
    wifi_name = wifi_name.split()[3].split(":")[1][1:-1]
    return render_template('wifi/schemes.html', wifi_name=wifi_name)

@wifi_views.route("/schemes/<name>/configure")
def schemes_config(name):
    return render_template('wifi/configure_scheme.html', scheme=name)
