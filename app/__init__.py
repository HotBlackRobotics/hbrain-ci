from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask_json import FlaskJSON
from config import config
from flask import g
from flask_cors import CORS

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
json = FlaskJSON()
cors = CORS(resources={r"/": {"origins": "*"}})


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    json.init_app(app)
    cors.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .ros import ros as ros_bp
    app.register_blueprint(ros_bp)

    from .api_1_0 import api as api_1_0_bp
    app.register_blueprint(api_1_0_bp, url_prefix='/api/v1.0')

    from .wifi_views import wifi_views as wifi_views_bp
    app.register_blueprint(wifi_views_bp, url_prefix='/wifi')



    def get_version():
        import subprocess, os
        path = os.path.realpath(__file__)
        p = subprocess.Popen('git describe --always', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.dirname(path))
        ver = ""
        for line in p.stdout.readlines():
            ver =  line.rstrip()
        retval = p.wait()
        return ver

    def get_ros():
        import json, subprocess
        import time
        time.sleep(5)
        source = 'source ' + app.config["ROS_ENVS"]
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
        env_info =  pipe.stdout.read()
        env = json.loads(env_info)
        return env["ROS_MASTER_URI"].split('//')[1].split(":")[0].rstrip() or 'localhost', env["DOTBOT_NAME"].rstrip() or 'dotbot', env["ROS_IP"].rstrip() or 'localhost'

    app.config["ROS_MASTER_URI"], app.config["DOTBOT_NAME"], app.config["ROS_IP"] = get_ros()

    @app.context_processor
    def utility_processor():
        g.MASTER_URL = app.config["ROS_MASTER_URI"]
        g.DOTBOT_NAME = app.config["DOTBOT_NAME"]
        g.ROS_IP = app.config["ROS_IP"]
    	return dict(version=get_version())


    def sendServerInfo():
        import requests
        from flask import current_app
        with app.app_context():
            app.config["ROS_MASTER_URI"], app.config["DOTBOT_NAME"], app.config["ROS_IP"] = get_ros()
            def getMAC(interface):
                try:
                    str = open('/sys/class/net/' + interface + '/address').read()
                except:
                    str = "00:00:00:00:00:00"
                return str[0:17]

            data = {
                'name': current_app.config["DOTBOT_NAME"],
                'master': current_app.config["ROS_MASTER_URI"],
                'ip': current_app.config["ROS_IP"],
                "macaddress":getMAC('wlan0'),
                "model":current_app.config["MODEL_HB"]
                }

            print data


            r = requests.put("http://www.hotblackrobotics.com/robot_api/v1.0/remote_robot", data=data)
            print r.status_code, r.reason
    import uwsgi
    if uwsgi.worker_id() == 1:
        import logging
        logging.basicConfig()

        print 'worker 1'
        from apscheduler.schedulers.background import BackgroundScheduler
        apsched = BackgroundScheduler()
        apsched.start()
        apsched.add_job(sendServerInfo, 'interval', seconds=3)

    return app
