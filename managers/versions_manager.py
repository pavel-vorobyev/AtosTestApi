from flask import Flask
from socketio import Server

from v1.namespaces.notifications import Notifications
from v1.view.user import User
from v1.view.room import Room
from v1.view.reservation import Reservation


class V1:

    @staticmethod
    def register(app: Flask):
        app.add_url_rule("/v1/user", view_func=User.as_view("user"))
        app.add_url_rule("/v1/room", view_func=Room.as_view("room"))
        app.add_url_rule("/v1/reservation", view_func=Reservation.as_view("reservation"))

    @staticmethod
    def register_sockets(app: Server):
        app.register_namespace(Notifications('/v1/notifications', app))
