from psycopg2.extras import RealDictCursor
from v1.util.values import Keys, ReservationStatuses
from v1.models.essence import Reservation
from v1.provider.user import get_user_by_id
from v1.provider.room import get_room


def if_reservation_time_available(cursor: RealDictCursor, room_id, start_time):
    cursor.execute("SELECT * FROM reservations WHERE {}=%s AND {}=%s AND {} >= %s"
                   .format(Keys.ROOM_ID, Keys.STATUS, Keys.END_TINE),
                   [int(room_id), ReservationStatuses.CONFIRMED, int(start_time)])

    return cursor.rowcount == 0


def if_reservation_created(cursor: RealDictCursor, room_id, user_id, start_time):
    cursor.execute("SELECT * FROM reservations WHERE {}=%s AND {}=%s AND {} >= %s AND {}=%s"
                   .format(Keys.ROOM_ID, Keys.USER_ID, Keys.END_TINE, Keys.STATUS),
                   [int(room_id), int(user_id), int(start_time), str(ReservationStatuses.REQUESTED)])

    return cursor.rowcount != 0


def put_reservation(cursor: RealDictCursor, reservation: Reservation) -> bool:
    if not if_reservation_time_available(cursor, reservation.room.r_id, reservation.start_time):
        return False

    cursor.execute("INSERT INTO reservations({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)"
                   .format(Keys.ROOM_ID, Keys.USER_ID, Keys.START_TIME, Keys.END_TINE, Keys.STATUS),
                   [int(reservation.room.r_id), int(reservation.user.u_id), int(reservation.start_time),
                    int(reservation.end_time), str(ReservationStatuses.REQUESTED)])

    return True


def get_reservation(cursor: RealDictCursor, id):
    cursor.execute("SELECT * FROM reservations WHERE {}=%s"
                   .format(Keys.ID),
                   [int(id)])

    db_response = cursor.fetchone()

    r_id = db_response[Keys.ID]
    room_id = db_response[Keys.ROOM_ID]
    user_id = db_response[Keys.USER_ID]
    start_time = db_response[Keys.START_TIME]
    end_time = db_response[Keys.END_TINE]
    status = db_response[Keys.STATUS]

    user = get_user_by_id(cursor, user_id)
    room = get_room(cursor, room_id)
    room.reservations = get_room_reservations(cursor, room.r_id)

    reservation = Reservation(r_id, room, user, start_time, end_time, status)
    return reservation


def get_requested_reservations(cursor: RealDictCursor):
    cursor.execute("SELECT * FROM reservations WHERE {}=%s ORDER BY id DESC "
                   .format(Keys.STATUS),
                   [str(ReservationStatuses.REQUESTED)])

    db_response = cursor.fetchall()
    reservations = []

    for db_reservation in db_response:
        r_id = db_reservation[Keys.ID]
        reservation = get_reservation(cursor, r_id)
        reservations.append(reservation)

    return reservations


def get_room_reservations(cursor: RealDictCursor, room_id) -> []:
    cursor.execute("SELECT * FROM reservations WHERE {}=%s AND {}=%s"
                   .format(Keys.ROOM_ID, Keys.STATUS),
                   [int(room_id), str(ReservationStatuses.CONFIRMED)])

    db_response = cursor.fetchall()
    reservations = []

    for db_reservation in db_response:
        r_id = db_reservation[Keys.ID]
        room_id = db_reservation[Keys.ROOM_ID]
        user_id = db_reservation[Keys.USER_ID]
        start_time = db_reservation[Keys.START_TIME]
        end_time = db_reservation[Keys.END_TINE]
        status = db_reservation[Keys.STATUS]

        user = get_user_by_id(cursor, user_id)
        room = get_room(cursor, room_id)
        room.reservations = []

        reservation = Reservation(r_id, room, user, start_time, end_time, status)
        reservations.append(reservation)

    return reservations


def set_reservation_status(cursor: RealDictCursor, r_id, status):
    cursor.execute("UPDATE reservations SET {}=%s WHERE {}=%s"
                   .format(Keys.STATUS, Keys.ID),
                   [str(status), int(r_id)])
