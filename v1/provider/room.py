from psycopg2.extras import RealDictCursor
from v1.util.values import Keys, ReservationStatuses
from v1.models.essence import Room


def get_room(cursor: RealDictCursor, r_id):
    cursor.execute("SELECT * FROM rooms WHERE {}=%s"
                   .format(Keys.ID),
                   [str(r_id)])

    db_response = cursor.fetchone()

    r_id = db_response[Keys.ID]
    name = db_response[Keys.NAME]
    description = db_response[Keys.DESCRIPTION]
    with_projector = db_response[Keys.WITH_PROJECTOR]
    with_board = db_response[Keys.WITH_BOARD]
    places_count = db_response[Keys.SEATS_COUNT]

    room = Room(r_id, name, description, with_projector, with_board, places_count)
    return room


def get_all_rooms(cursor: RealDictCursor) -> []:
    cursor.execute("SELECT * FROM rooms ORDER BY id DESC ")

    db_response = cursor.fetchall()
    rooms = []

    for db_room in db_response:
        r_id = db_room[Keys.ID]
        room = get_room(cursor, r_id)
        rooms.append(room)

    return rooms


def get_available_rooms(cursor: RealDictCursor, user_id) -> []:
    cursor.execute("SELECT * FROM rooms AS room WHERE "
                   "NOT EXISTS "
                   "(SELECT 1 FROM reservations AS res "
                   "WHERE res.room_id = room.id AND res.user_id = %s AND res.status = %s) "
                   "ORDER BY room.id DESC",
                   [str(user_id), str(ReservationStatuses.CONFIRMED)])

    db_response = cursor.fetchall()
    rooms = []

    for db_room in db_response:
        r_id = db_room[Keys.ID]
        room = get_room(cursor, r_id)
        rooms.append(room)

    return rooms


def get_my_rooms(cursor: RealDictCursor, user_id) -> []:
    cursor.execute("SELECT * FROM rooms AS room WHERE "
                   "EXISTS "
                   "(SELECT 1 FROM reservations AS res "
                   "WHERE res.room_id = room.id AND res.user_id = %s AND res.status = %s) "
                   "ORDER BY room.id DESC",
                   [str(user_id), str(ReservationStatuses.CONFIRMED)])

    db_response = cursor.fetchall()
    rooms = []

    for db_room in db_response:
        r_id = db_room[Keys.ID]
        room = get_room(cursor, r_id)
        rooms.append(room)

    return rooms


def put_room(cursor: RealDictCursor, room: Room):
    cursor.execute("INSERT INTO rooms({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s)"
                   .format(Keys.NAME, Keys.DESCRIPTION, Keys.WITH_PROJECTOR, Keys.WITH_BOARD, Keys.SEATS_COUNT),
                   [str(room.name), str(room.description), bool(room.with_projector), bool(room.with_board),
                    int(room.seats_count)])


def edit_room(cursor: RealDictCursor, room: Room):
    cursor.execute("UPDATE rooms SET {}=%s, {}=%s, {}=%s, {}=%s, {}=%s WHERE {}=%s"
                   .format(Keys.NAME, Keys.DESCRIPTION, Keys.WITH_PROJECTOR, Keys.WITH_BOARD, Keys.SEATS_COUNT,
                           Keys.ID),
                   [str(room.name), str(room.description), bool(room.with_projector), bool(room.with_board),
                    int(room.seats_count), int(room.r_id)])
