from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
import subprocess
import json

def get_config():
    env_var_source = '/opt/hbrain/configurations/vars.bash'
    source = 'source ' + env_var_source
    dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
    pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
    env_info =  pipe.stdout.read()
    env = json.loads(env_info)

    name = env['DOTBOT_NAME'] or 'dotbot'
    os_version = env['ROBOT_VERSION'] or '0.0.0'
    os_name = env['ROBOT_OS'] or 'hbrain'
    conf =  {'name':name, 'os':os_name + ' v'+ os_version, 'model':'O|Robot101'}
    return conf

@main.route('/')
def index():
	return render_template('main/cover.html', robot = get_config())
