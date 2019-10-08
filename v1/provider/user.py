from psycopg2.extras import RealDictCursor
from v1 import Keys
from v1.models.essence import User


def if_user_exists(cursor: RealDictCursor, email):
    cursor.execute("SELECT * FROM users WHERE {}=%s"
                   .format(Keys.EMAIL),
                   [str(email)])

    return cursor.rowcount != 0


def get_user(cursor: RealDictCursor, email, password):
    cursor.execute("SELECT * FROM users WHERE {}=%s AND {}=%s"
                   .format(Keys.EMAIL, Keys.PASSWORD),
                   [str(email), str(password)])

    db_response = cursor.fetchone()

    if db_response is None:
        return None

    return User(db_response[Keys.ID], db_response[Keys.NAME], db_response[Keys.EMAIL])


def get_user_by_id(cursor: RealDictCursor, user_id):
    cursor.execute("SELECT * FROM users WHERE {}=%s"
                   .format(Keys.ID),
                   [str(user_id)])

    db_response = cursor.fetchone()

    if db_response is None:
        return None

    return User(db_response[Keys.ID], db_response[Keys.NAME], db_response[Keys.EMAIL])


def put_user(cursor: RealDictCursor, name, email, password):
    cursor.execute("INSERT INTO users({}, {}, {}) VALUES(%s, %s, %s)"
                   .format(Keys.NAME, Keys.EMAIL, Keys.PASSWORD),
                   [str(name), str(email), str(password)])
