import configparser
import os
import sys


def get_app_root_directory():
    fn = getattr(sys.modules['app'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    return root_path


def get_db_conf():
    config = configparser.ConfigParser()
    config.read("{}/v1/util/conf/db.ini".format(os.getcwd()))
    return config['DB']['host'], config['DB']['name'], config['DB']['user'], config['DB']['password']


def get_redis_conf():
    config = configparser.ConfigParser()
    config.read("{}/v1/util/conf/redis.ini".format(os.getcwd()))
    return config["REDIS"]["host"], config["REDIS"]["port"], config["REDIS"]["db"]
