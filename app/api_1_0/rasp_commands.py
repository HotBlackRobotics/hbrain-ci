from . import api
from flask import jsonify, request, flash, make_response, render_template, current_app
from flask_json import JsonError, json_response, as_json

from sqlalchemy.exc import IntegrityError
import subprocess


@api.route('/bin/poweroff')
def poweroff():
	proc = subprocess.Popen(['sudo', 'poweroff', 'now'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')

@api.route('/bin/reboot')
def reboot():
	proc = subprocess.Popen(['sudo', 'reboot'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')

@api.route('/bin/update')
def update():
	proc = subprocess.Popen(['update_robotoma'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')

@api.route('/bin/hostname/<hostname>')
def set_hostname(hostname):
	proc = subprocess.Popen(['/usr/local/bin/change_hostname', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	proc.wait()
	return json_response( response='ok')
