import os

import pygame

from app.app import APP
from game.basic.basic_background import Basic
from game.basic.button import Image, Text, Color, ButtonImage
from game.common.connect import ws_client
from game_data.hall_data import HallCacheData
from pb.pd_class import GameHall
from utils import settings, enums
from utils.utils import encode_msg_class


class Hall(Basic):
    def __init__(self):
        super().__init__()
        self.cache = HallCacheData()
        self.username = None
        self.is_start = True

    def create_map(self):
        if self.is_start:
            # 成功进入大厅时，获取当前路由
            current_router = APP.router.current_router()
            game_type = current_router.replace('hall', '').replace('/', '')
            if game_type == "":
                game_type = 'blank'
            self.submit(game_type, is_push=False)
            self.is_start = False
        self.size, self.screen = self.basic_bg()
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
        Text(f" {self.username} 欢迎您, 当前大厅在线人数：{self.cache.GAME_HALL.pb_class.players}", Color.BLACK, 'HYHanHeiW.ttf', 16, size=(260, 50)).draw(self.screen)

        x, y = 50, 150
        result = []
        # 游戏类型列表
        for game_info, image_file in enums.GAME_TYPES.items():
            button = ButtonImage(image_file, rect=pygame.Rect(x, y, 200, 200))
            button.draw(self.screen)
            game_type, cn_name = game_info.split("|")
            Text(cn_name, Color.BLACK,
                 'HYHanHeiW.ttf', 12, size=(x, y + 50)).draw(self.screen)
            result.append({'class': button, 'args': [self.submit, game_type]})
            x += 320
        return result

    def submit(self, game_type, is_push=True):
        g = GameHall()
        g.set_val(**{'gameType': game_type})
        ws_client.send_message(encode_msg_class('hall', g))
        if is_push:
            APP.router.push(f'/chat')

