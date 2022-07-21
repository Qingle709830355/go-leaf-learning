import os

import pygame

from app.app import APP
from game.basic.basic_background import Basic
from game.basic.button import Image, Text, Color, ButtonImage, ButtonText
from game.common.connect import ws_client
from game_data.hall_data import HallCacheData
from pb.pd_class import GameHall, Room
from utils import settings, enums
from utils.utils import encode_msg_class


class Hall(Basic):
    def __init__(self):
        super().__init__()
        self.cache = HallCacheData()
        self.username = None

    def create_map(self):
        result = super().create_map()
        current_router = APP.router.current_router()
        game_type = current_router.replace('hall', '').replace('/', '')
        if game_type == "":
            game_type = 'blank'
        if self.is_start:
            # 成功进入大厅时，获取当前路由
            self.submit(game_type, is_push=False)
            self.is_start = False
            if game_type != "blank":
                self.create_rooms(game_type, action='no')

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

        # 增加一个创建房间的按钮
        if game_type != 'blank':
            create_ = ButtonText("创建房间", Color.create(255, 255, 255), 'HYHanHeiW.ttf', 24, rect_color=Color.create(55, 55, 55), size=(50, 150))
            result.append({'class': create_, 'args': [self.create_rooms, game_type]})
            data_map = {}
            for num, room in enumerate(self.cache.GAME_HALL.pb_class.rooms):
                gt = room.gameType
                room_id = room.roomId
                cn = f'房间{num + 1}'
                image = os.path.join(settings.ASSETS_PATH, 'chat.jpg')
                data_map[f'{gt}|{cn}|{room_id}'] = image
        else:
            # 大厅地图数据
            data_map = enums.GAME_TYPES

        x, y = 50, 220
        num = 0
        # 游戏类型列表
        for game_info, image_file in data_map.items():
            num += 1
            button = ButtonImage(image_file, rect=pygame.Rect(x, y, 200, 200))
            button.draw(self.screen)
            game_t, cn_name, *room_id = game_info.split("|")
            room_id = ''.join(room_id)
            Text(cn_name, Color.BLACK,
                 'HYHanHeiW.ttf', 12, size=(x, y + 50)).draw(self.screen)
            # 存在roomid代表进入房间
            if room_id:
                result.append({'class': button, 'args': [self.in_room, game_t, room_id]})
            else:
                result.append({'class': button, 'args': [self.submit, game_t]})
            x += 150
            if num == 3:
                num = 0
                y += 100
                x = 50
        return result

    def submit(self, game_type, is_push=True):
        # 提交游戏类型
        g = GameHall()
        g.set_val(**{'gameType': game_type})
        ws_client.send_message(encode_msg_class('hall', g))
        if is_push:
            APP.router.push(f'/{game_type}hall')

    def create_rooms(self, game_type, action=""):
        room = Room()
        room.set_val(self.cache.COOKIE, **{'gameType': game_type, 'maxPlayerNum': 10, 'roomId': action})
        ws_client.send_message(encode_msg_class('room', room))
        self.handle_events = self.create_map()

    def in_room(self, game_type, room_id):
        # 进入房间
        room = Room()
        room.set_val(self.cache.COOKIE, **{'gameType': game_type, 'maxPlayerNum': 10, 'roomId': room_id})
        ws_client.send_message(encode_msg_class('room', room))
        APP.router.push(f'/{game_type}')
