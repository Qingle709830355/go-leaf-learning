from typing import List

from . import my_pb2


class BasePb:

    def __init__(self, pb_class):
        self.pb_class = pb_class

    def set_val(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self.pb_class, key, value)

    def properties(self):
        return [filed.name for filed in self.pb_class.DESCRIPTOR.fields]

    def encode(self):
        return self.pb_class.SerializeToString()

    def decode(self, code):
        self.pb_class.ParseFromString(code)

    def to_dict(self):
        result = {}
        for filed in self.pb_class.DESCRIPTOR.fields:
            filed_name = filed.name
            result[filed_name] = getattr(self.pb_class, filed_name)
        return result


class LoginRequest(BasePb):

    def __init__(self, pb_class=None):
        self.pb_class = pb_class if pb_class else my_pb2.LoginRequest()
        super().__init__(self.pb_class)


class LoginResponse(BasePb):
    def __init__(self, pb_class=None):
        self.pb_class = pb_class if pb_class else my_pb2.LoginResponse()
        super().__init__(self.pb_class)


class MsgInfo(BasePb):

    def __init__(self, pb_class=None):
        self.pb_class = pb_class if pb_class else my_pb2.MyMessage()
        super().__init__(self.pb_class)

    def set_val(self, msg, user_info: LoginResponse):
        user_class = LoginResponse(self.pb_class.userInfo)
        user_class.set_val(**user_info.to_dict())
        self.pb_class.msg = msg


class Room(BasePb):
    def __init__(self, pb_class=None):
        self.pb_class = pb_class if pb_class else my_pb2.Room()
        super().__init__(self.pb_class)

    def set_val(self, user_info: LoginResponse, **kwargs):
        super().set_val(**kwargs)
        self.pb_class.users.append(user_info.pb_class)


class GameHall(BasePb):
    def __init__(self, pb_class=None):
        self.pb_class = pb_class if pb_class else my_pb2.GameHall()
        super().__init__(self.pb_class)


msg_types = {
    'login': LoginRequest,
    'msg': MsgInfo,
    'hello': None,
    'loginResp': LoginResponse,
    'hall': GameHall,
    'room': Room
}