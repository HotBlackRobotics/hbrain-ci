import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    MODEL_HB = 'HBrain vb0.5.0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BOOTSTRAP_SERVE_LOCAL = True
    CATKIN_FOLDER = os.environ.get('CATKIN_FOLDER') or '/Users/ludus/develop/dotbot_ws/ros/'
    DOTBOT_PACKAGE_NAME = os.environ.get('DOTBOT_PACKAGE_NAME') or 'dotbot_app'
    ROS_ENVS = os.environ.get('ROS_ENVS') or '/opt/ros/indigo/setup.bash'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
