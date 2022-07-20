from game_data.user_data import UserDataCache
from pb.pd_class import GameHall


class HallCacheData(UserDataCache):

    def __init__(self):
        super().__init__()
        self.GAME_HALL = GameHall()

    def save(self, msg):
        super().save(msg)
        if isinstance(msg, GameHall):
            self.GAME_HALL = msg