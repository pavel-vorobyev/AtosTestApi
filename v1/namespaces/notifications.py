import json

from socketio import Namespace, Server
from v1.util.worker import RedisQueue


class Notifications(Namespace):
    def __init__(self, endpoint, sio: Server):
        super().__init__(endpoint)
        self.redis_queue = RedisQueue("notifications")
        self.sio = sio
        self.sio.start_background_task(target=self.worker)

    def on_authorize(self, sid, user_id):
        self.enter_room(sid=sid, room=user_id)
        print("user_id " + str(user_id))

    def worker(self):
        while True:
            self.sio.sleep(0.1)
            item = self.redis_queue.get()

            if item is not None:
                item = item.decode("utf-8")
                item = item.replace("'", "\"")
                item = item.replace("None", "\"\"")
                item = item.replace("True", "true")
                item = item.replace("False", "false")
                item = json.loads(item)

                room = item["user"]["u_id"]
                print("room " + str(room))
                self.send(data=item, room=room)


