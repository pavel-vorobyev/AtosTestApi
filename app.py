import socketio
import eventlet

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from managers.versions_manager import V1
from managers.errors_managers import handle_error

sio = socketio.Server(async_mode='eventlet')
flask_app = Flask(__name__)
app = socketio.WSGIApp(sio, flask_app)

CORS(flask_app)
V1.register(flask_app)
V1.register_sockets(sio)


@flask_app.errorhandler(HTTPException)
def error_handler(e):
    return handle_error(e)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 80)), app)
