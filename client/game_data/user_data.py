from pb.pd_class import LoginResponse


class UserDataCache:

    def __init__(self):
        # 登录情况
        self.COOKIE = None

    def save(self, msg):
        if isinstance(msg, LoginResponse):
            self.COOKIE = msg
