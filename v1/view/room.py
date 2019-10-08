from flask import request, g
from v1 import ApiView
from v1.util.values import Keys, Reasons, RoomTypes
from v1.util.checker import check_for_params
from v1.util.exceptions import ApiException
from v1.models.essence import Room as RoomModel
from v1.provider.room import put_room, get_all_rooms, get_available_rooms, get_my_rooms, edit_room, get_room
from v1.provider.reservation import get_room_reservations
from v1.util.response import get_response, get_list_response
from v1.util.auth import access_token_required


class Room(ApiView):

    def put(self):
        body = request.json
        missed_param = check_for_params([Keys.NAME, Keys.DESCRIPTION, Keys.WITH_PROJECTOR, Keys.WITH_BOARD,
                                         Keys.SEATS_COUNT], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        name = body[Keys.NAME]
        description = body[Keys.DESCRIPTION]
        with_projector = body[Keys.WITH_PROJECTOR]
        with_board = body[Keys.WITH_BOARD]
        places_count = body[Keys.SEATS_COUNT]

        room = RoomModel(None, name, description, with_projector, with_board, places_count)
        put_room(self.cursor, room)

        return get_response(room)

    @access_token_required
    def get(self):
        params = request.args

        if Keys.TYPE not in params:
            raise ApiException(pointer=Keys.TYPE, reason=Reasons.MISSED, code=400)

        allowed_types = [RoomTypes.ALL, RoomTypes.AVAILABLE, RoomTypes.MY]
        r_type = params[Keys.TYPE]

        if r_type not in allowed_types:
            raise ApiException(pointer=Keys.TYPE, reason=Reasons.INVALID, code=400)

        user_id = g.user_id

        if r_type == RoomTypes.AVAILABLE:
            rooms = get_available_rooms(self.cursor, user_id)
        elif r_type == RoomTypes.MY:
            rooms = get_my_rooms(self.cursor, user_id)
        else:
            rooms = get_all_rooms(self.cursor)

        for room in rooms:
            room.reservations = get_room_reservations(self.cursor, room.r_id)

        return get_list_response(rooms)

    def patch(self):
        body = request.json
        print(body)
        missed_param = check_for_params([Keys.R_ID, Keys.NAME, Keys.DESCRIPTION, Keys.WITH_PROJECTOR, Keys.WITH_BOARD,
                                         Keys.SEATS_COUNT], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        r_id = body[Keys.R_ID]
        name = body[Keys.NAME]
        description = body[Keys.DESCRIPTION]
        with_projector = body[Keys.WITH_PROJECTOR]
        with_board = body[Keys.WITH_BOARD]
        places_count = body[Keys.SEATS_COUNT]

        room = RoomModel(r_id, name, description, with_projector, with_board, places_count)
        edit_room(self.cursor, room)

        room = get_room(self.cursor, r_id)
        return get_response(room)
