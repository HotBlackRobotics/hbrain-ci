from flask import Flask, current_app, g, jsonify, Response, request, redirect, url_for
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import JsonError, json_response, as_json
from flask_restful import Api, Resource, reqparse

from . import api
from datetime import datetime
import subprocess

from wifi import Cell, Scheme
from wifi.exceptions import ConnectionError
from compiler import Compiler

rest_api = Api(api)
comp = Compiler()

from ..utils import getRobotInfos, replace

class Robot(Resource):
    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"], methods=['GET', 'PUT'])]
    def get(self):
        return jsonify(getRobotInfos(current_app))

class RobotSketch(Resource):

    decorators = [cross_origin(origin='*')]

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()
        of = open(current_app.config['CATKIN_FOLDER'] + 'src/' + current_app.config['DOTBOT_PACKAGE_NAME'] + '/hbr_ros_skeleton/node.py', "w")
        of.write(args['code'])
        of.close()
        comp.run_dotbot_node()
        return jsonify({'response': 'ok'})

    def get(self):
        return jsonify({'response': 'ok'})

    def options(self):
        pass

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('node')
        args = parser.parse_args()
        env = comp.env()
        env["ROS_NAMESPACE"] = '';
        killproc = subprocess.Popen(['rosnode', 'kill', args.node], env=env)
        killproc.wait()
    	return jsonify({'response': 'ok'})

'''
class StreamNode(Resource):

    decorators = [cross_origin(origin='*')]

    def get(self, id):
        comp.run_dotbot_node()
        return jsonify({'response': 'running'})
        #return Response(comp.read_run_proc(id), mimetype='text/event-stream')
class WifiCells(Resource):
    def get(self):
        cells = Cell.all('wlan0')
        wifi_info = []
        for c in cells:
            if c.ssid not in [wc['name'] for wc in wifi_info] + ["\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"]:
                wifi_info.append({'name': c.ssid, 'encryption': c.encryption_type, 'encrypted': c.encrypted})
        return jsonify({'cells': wifi_info})

class WifiSchemes(Resource):
    def get(self):
        schemes = Scheme.all()
        return jsonify({'schemes': [s.__dict__ for s in schemes]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()

        schemes = [s for s in Scheme.all()]
        cells = Cell.all('wlan0')

        newscheme = None
        for cell in cells:
            if cell.ssid == args['name']:
                newscheme = Scheme.for_cell('wlan0', 'scheme-'+str(len(schemes)), cell, args['password'])
                break
        if newscheme is None:
            return jsonify({'response': "network non found"})
        else:
            newscheme.save()
            newscheme.activate()
            return jsonify({'response': "ok"})

class WifiScheme(Resource):
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('action')
        args = parser.parse_args()
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) == 0:
            return jsonify({'response': "non found"})
        scheme = s[0]
        return jsonify({'scheme': scheme.__dict__})

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('action')
        parser.add_argument('ssid')
        parser.add_argument('password')
        args = parser.parse_args()
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) == 0:
            return jsonify({'response': "non found"})
        scheme = s[0]
        if args["action"] == 'connect':
            try:
                scheme.activate()
            except ConnectionError:
                return  jsonify({"error": "Failed to connect to %s." % scheme.name})
            return jsonify({'scheme': scheme.__dict__, "connected": True})
        elif args["action"] == "configure":
            cells = [cell for cell in Cell.all("wlan0") if cell.ssid == args['ssid']]
            if len(cells) == 0:
                return jsonify({'error': 'wifi not found'})
            sname = scheme.name

            for s in Scheme.all():
                s.delete()
                if s.name == sname:
                    s = Scheme.for_cell('wlan0', sname, cells[0], args['password'])
                s.save()
            return jsonify({'scheme': scheme.__dict__})
        elif args["action"] == "clean":
            sname = scheme.name
            for s in Scheme.all():
                s.delete()
                if s.name == sname:
                    s = Scheme('wlan0', sname)
                s.save()

        else:
            return jsonify({'scheme': scheme.__dict__})

    def delete(self, name):
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) > 0:
            s[0].delete()
            return jsonify({'response': "ok"})
        else:
            return jsonify({'response': "non found"})
'''

class ConfHostname(Resource):
    decorators = [cross_origin(origin='*')]
    def get(self):
        return jsonify({'hostname': current_app.config["DOTBOT_NAME"]})

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hostname')
        args = parser.parse_args()
        if args["hostname"] is not None and args["hostname"] != "":
            hostname = '_'.join(args["hostname"].lower().split())
            replace(current_app.config["DOTBOT_VAR_ENVS"], '^export\sDOTBOT_NAME.*\W', 'export DOTBOT_NAME=%s\n'%hostname)
            return jsonify({'response': "ok"})
        return jsonify({'response': "error"})

class ManageRobot(Resource):
    decorators = [cross_origin(origin='*')]
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('command')
        args = parser.parse_args()
        print 'test'
        if args["command"] == 'poweroff':
            subprocess.Popen(['poweroff'])
            return jsonify({'response': "ok"})
        elif args["command"] == 'reboot':
            subprocess.Popen(['reboot'])
            return jsonify({'response': "ok"})
        else:
            return jsonify({'response': "command not found"})

rest_api.add_resource(Robot, '/discovery')
rest_api.add_resource(RobotSketch, '/run/sketch')

#rest_api.add_resource(StreamNode, '/stream/<int:id>', endpoint="stream")
#rest_api.add_resource(WifiCells, '/wifi/cells')
#rest_api.add_resource(WifiSchemes, '/wifi/schemes')
#rest_api.add_resource(WifiScheme, '/wifi/schemes/<name>')

rest_api.add_resource(ConfHostname, '/conf/hostname')
rest_api.add_resource(ManageRobot, '/manage/robot')
