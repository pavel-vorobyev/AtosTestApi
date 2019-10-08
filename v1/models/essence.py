from v1.models import Model, JsonableModel


class User(Model):

    def __init__(self, u_id, name, email):
        super().__init__()
        self.u_id = u_id
        self.email = email
        self.name = name


class Room(Model):

    def __init__(self, r_id, name, description, with_projector, with_board, seats_count, reservations=None):
        super().__init__()
        self.r_id = r_id
        self.name = name
        self.description = description
        self.with_projector = with_projector
        self.with_board = with_board
        self.seats_count = seats_count
        self.reservations = reservations


class Reservation(Model, JsonableModel):

    def __init__(self, r_id, room: Room, user: User, start_time, end_time, status=None):
        super().__init__()
        self.r_id = r_id
        self.room = room
        self.user = user
        self.start_time = start_time
        self.end_time = end_time
        self.status = status


class Auth(Model):

    def __init__(self, token, user: User):
        super().__init__()
        self.token = token
        self.user = user


class Error(Model):

    def __init__(self, pointer, reason):
        super().__init__()
        self.pointer = pointer
        self.reason = reason
