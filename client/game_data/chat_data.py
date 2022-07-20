from game_data.user_data import UserDataCache
from pb.pd_class import MsgInfo


class ChatDataCache(UserDataCache):
    """
    聊天数据缓存
    """

    def __init__(self):
        super().__init__()
        self.CHAT_LIST = []

    def save(self, msg):
        super(ChatDataCache, self).save(msg)
        if isinstance(msg, MsgInfo):
            self.CHAT_LIST.append(msg)
