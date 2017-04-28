from . import api
from flask import jsonify, request, flash, render_template
from flask_json import JsonError, json_response, as_json
from datetime import datetime
import subprocess
import json
from sqlalchemy.exc import IntegrityError
from compile import comp


#@api.route('/roscore/start')
#    if not roscore_is_running():
#@api.route('/roscore/stop')


@api.route('/roscore/check')
@as_json
def roscore_check():
    return jsonify(running=roscore_is_running())

def roscore_is_running():
    return True


@api.route("/ros/rosconfig", methods=["PUT"])
def post_rosconfig():
    print request.json
    of = open("/opt/virtualenvs/ros/project/config.bash", "w")
    of.write(render_template("code/config.bash", namespace = request.json["namespace"], master=request.json["master"], ip=request.json["ip"]))
    of.close()
    return "ok"



def get_rostopic():
    system_topics = ['/rosout', '/rosout_agg']
    p = subprocess.Popen('rostopic list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=comp.env())
    topics = []
    info = []
    for line in p.stdout.readlines():
        t = line.rstrip()
        if t not in system_topics:
            topics.append([t])
    print topics, len(topics)
    for i in range(0, len(topics)):
        pt = subprocess.Popen('rostopic info '  + topics[i][0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=comp.env())
        for line in pt.stdout.readlines():
            topics[i].append(line.split(': ')[1].rstrip())
            break
    return topics

@api.route('/rostopics/')
@as_json
def rostopic():
    if roscore_is_running():
        return jsonify(topics=get_rostopic())
    raise JsonError(description='roscore not running')

@api.route('/rosnodes/')
@as_json
def rosnode():
    if roscore_is_running():
        p = subprocess.Popen('rosnode list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=comp.env())
        nodes = []
        for line in p.stdout.readlines():
            nodes.append([line[1:-1] ])
        return jsonify(nodes=nodes)
    raise JsonError(description='roscore not running')

@api.route('/rosnode/<path:node>/', methods=['DELETE'])
@as_json
def rostopic_kill(node):
    env = comp.env()
    env["ROS_NAMESPACE"] = '';
    subprocess.Popen(['rosnode', 'kill', node], env=env)
    return json_response( response='ok')
