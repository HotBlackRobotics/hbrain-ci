from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask_json import FlaskJSON
from config import config
from flask import g
from flask_cors import CORS

bootstrap = Bootstrap()
json = FlaskJSON()
cors = CORS()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    json.init_app(app)
    cors.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .api_1_0 import api as api_1_0_bp
    app.register_blueprint(api_1_0_bp, url_prefix='/api/v1.0')

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

    def sendServerInfo():
        import requests
        from flask import current_app
        with app.app_context():
            app.config["ROS_MASTER_URI"], app.config["DOTBOT_NAME"], app.config["ROS_IP"] = get_ros()
            from .utils import getRobotInfos
            data = getRobotInfos(app)
            r = requests.put(app.config['HBR_SERVER'] + '/robot_api/v1.0/remote_robot', data=data)
            print r.status_code, r.reason

    return app
