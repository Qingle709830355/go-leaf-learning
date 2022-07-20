import os

import pygame

from app.app import APP
from game.basic.basic_background import Basic
from game.basic.button import InputBox, ButtonText, Color, Image, Text, ShowBox
from game.common.connect import ws_client
from game_data.chat_data import ChatDataCache
from utils import settings
from pb.pd_class import MsgInfo
from utils.utils import encode_msg_class


class Chat(Basic):

    def __init__(self):
        super().__init__()
        self.cache = ChatDataCache()
        self.username = None

    def create_map(self):
        self.size, self.screen = self.basic_bg()
        width, height = self.size
        # 头像
        Image(os.path.join(settings.ASSETS_PATH, 'touxiang.jpeg'), rect=pygame.Rect(50, 50, 200, 200),
              ratio=settings.SHOW_RATIO).draw(self.screen)
        # 没有cookie， 跳到登录页面
        if self.cache.COOKIE is None:
            self.username = 'TEST'
            pass
            # APP.router.push('/')
        else:
            self.username = self.cache.COOKIE.pb_class.username
        # 用户名称
        Text(f" {self.username} 欢迎您使用leaf客户端！", Color.BLACK, 'HYHanHeiW.ttf', 16, size=(260, 50)).draw(self.screen)
        # 展示框
        show_ = ShowBox(pygame.Rect(10, 100, width - 20, height - 200), max_width=width - 20, prompt='',
                        font_size=16, font_small_size=10)
        show_.draw(self.screen)
        # 输入框
        input_ = InputBox(pygame.Rect(10, height - 90, width - 20, 60), max_width=width - 20)
        input_.draw(self.screen)
        # 发送按钮
        submit = ButtonText("发送", Color.create(255, 255, 255), 'HYHanHeiW.ttf', 24, rect_color=Color.create(40, 112, 21), size=(width / 2, height - 15))
        submit.draw(self.screen)
        return [{'class': show_, 'args': [self.add_msg]},
                {'class': input_, 'args': []},
                {'class': submit, 'args': [self.send_, input_]}]

    def add_msg(self, showBox: ShowBox):
        chat_list = self.cache.CHAT_LIST
        result = []
        y = showBox.boxBody.y + 20
        for index, chat in enumerate(chat_list):
            msg = chat.pb_class.msg
            username = chat.pb_class.userInfo.username
            if index > 0:
                y += 32
            if username == self.username:
                x = None
            else:
                x = 15
            positions = (x, y)
            result.append([msg, username, positions])
        return result

    def send_(self, input_):
        text = input_._ime_text
        msg_info = MsgInfo()
        msg_info.set_val(msg=text, user_info=self.cache.COOKIE)
        ws_client.send_message(encode_msg_class('msg', msg_info))
        input_._ime_text = ''
