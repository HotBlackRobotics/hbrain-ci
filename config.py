import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MODEL_NAME = 'HBrain-CI'
    MODEL_VERSION = os.environ.get('HBRAIN_VERSION') or '0.0.0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    BOOTSTRAP_SERVE_LOCAL = True
    CATKIN_FOLDER = os.environ.get('CATKIN_FOLDER') or '/opt/hbrain-ros/'
    DOTBOT_PACKAGE_NAME = os.environ.get('DOTBOT_PACKAGE_NAME') or 'hbr_app'
    ROS_ENVS = os.environ.get('ROS_ENVS') or '/opt/ros/indigo/setup.bash'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HBR_SERVER = 'http://www.hotblackrobotics.com'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
