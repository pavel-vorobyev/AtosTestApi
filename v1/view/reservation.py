from flask import request, g
from v1 import ApiView
from v1.util.values import Keys, Reasons, ReservationStatuses
from v1.util.checker import check_for_params
from v1.util.exceptions import ApiException
from v1.provider.reservation import put_reservation, if_reservation_created, set_reservation_status, get_reservation, \
    get_requested_reservations
from v1.models.essence import Reservation as ReservationModel, User, Room
from v1.util.response import get_response
from v1.util.auth import access_token_required
from v1.util.worker import RedisQueue


class Reservation(ApiView):

    @access_token_required
    def get(self):
        reservations = get_requested_reservations(self.cursor)
        return get_response(reservations)

    @access_token_required
    def put(self):
        body = request.json
        missed_param = check_for_params([Keys.ROOM_ID, Keys.START_TIME, Keys.END_TINE], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        user_id = g.user_id
        room_id = body[Keys.ROOM_ID]
        start_time = body[Keys.START_TIME]
        end_time = body[Keys.END_TINE]

        if end_time <= start_time:
            raise ApiException(pointer=Keys.END_TINE, reason=Reasons.INVALID, code=400)

        if if_reservation_created(self.cursor, room_id, user_id, start_time):
            raise ApiException(pointer=Keys.REQUEST, reason=Reasons.CREATED, code=409)

        user = User(user_id, None, None)
        room = Room(room_id, None, None, None, None, None)
        reservation = ReservationModel(None, room, user, start_time, end_time)
        result = put_reservation(self.cursor, reservation)

        if result:
            return get_response(reservation)
        else:
            raise ApiException(pointer=Keys.START_TIME, reason=Reasons.TAKEN, code=409)

    @access_token_required
    def patch(self):
        body = request.json
        missed_param = check_for_params([Keys.RESERVATION_ID, Keys.STATUS], body)

        if missed_param is not None:
            raise ApiException(pointer=missed_param, reason=Reasons.MISSED, code=400)

        reservation_id = body[Keys.RESERVATION_ID]
        status = body[Keys.STATUS]

        allowed_statuses = [ReservationStatuses.CONFIRMED, ReservationStatuses.DECLINED]

        if status not in allowed_statuses:
            raise ApiException(pointer=Keys.STATUS, reason=Reasons.INVALID, code=400)

        set_reservation_status(self.cursor, reservation_id, status)
        reservation = get_reservation(self.cursor, reservation_id)

        redis_queue = RedisQueue("notifications")
        redis_queue.put(str(reservation.to_json()))

        return get_response(reservation)


