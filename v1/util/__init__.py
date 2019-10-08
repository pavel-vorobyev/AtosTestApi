import psycopg2
import redis

from v1.util.conf.config import get_db_conf, get_redis_conf


def get_db():
    host, db_name, user, password = get_db_conf()
    user_db = psycopg2.connect(
        "dbname='{}' user='{}' host='{}' password='{}'".format(db_name, user, host, password))
    user_db.autocommit = True
    return user_db


def get_redis():
    host, port, db = get_redis_conf()
    return redis.Redis(host=host, port=port, db=db)
