import pygame

from app.app import APP
from game.basic.basic_background import Basic
from game.basic.button import Text, ButtonText, InputBox, Color
from game.common.connect import ws_client
from utils.utils import encode_msg


class Login(Basic):

    def create_map(self):
        self.size, self.screen = self.basic_bg()

        width, height = self.size
        Text("欢迎使用MY Leaf客户端", Color.BLACK, 'msyh.ttc', 32, size=(width / 2, height / 2 - 250)).draw(self.screen)
        # 用户信息输入
        Text("请输入用户名称：", Color.BLACK, 'HYHanHeiW.ttf', 16, size=(width/2 - 120, height/2 - 100)).draw(self.screen)
        # 输入框
        input_name = InputBox(pygame.Rect(width/2 - 60, height/2 - 115, 100, 32))
        Text("请输入用户名称：", Color.BLACK, 'HYHanHeiW.ttf', 16, size=(width/2 - 120, height/2)).draw(self.screen)
        input_pwd = InputBox(pygame.Rect(width / 2 - 60, height / 2 - 15, 100, 32))
        # 确定登录按钮
        submit = ButtonText("确认登录", Color.create(255, 255, 255), 'HYHanHeiW.ttf', 24, rect_color=Color.create(40, 112, 21), size=(width / 2 + 92, height / 2 + 70))
        submit.draw(self.screen)
        return [{'class': input_name, 'args': []},
                {'class': input_pwd, 'args': []},
                {'class': submit, 'args': [self.login, input_name, input_pwd]}]

    def login(self, input_name, input_pwd):
        """
        确认登录
        :param input_name:
        :param input_pwd:
        :return:
        """
        name = input_name._ime_text
        pwd = input_pwd._ime_text
        if not all([name, pwd]):
            return
        user = {'username': name, 'password': pwd}
        ws_client.send_message(encode_msg('login', user))
        APP.router.push('/chat')