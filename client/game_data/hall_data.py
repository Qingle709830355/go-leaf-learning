from game_data.user_data import UserDataCache
from pb.pd_class import GameHall, Room


class HallCacheData(UserDataCache):

    def __init__(self):
        super().__init__()
        self.GAME_HALL = GameHall()
        self.ROOMS = []

    def save(self, msg):
        super().save(msg)
        if isinstance(msg, GameHall):
            self.GAME_HALL = msg
        if isinstance(msg, Room):
            self.ROOMS.append(msg)