import os
import sys

import pygame

from app.app import APP
from game.basic.button import Image, ButtonText, Color
from utils import settings
from game.common.connect import ws_client


class Basic:
    # 基础窗口类
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = None
        self.screen = None
        self.running = True
        self.cache = None
        self.handle_events = []
        # 是否为刚进入页面
        self.is_start = True

    def create_map(self):
        self.size, self.screen = self.basic_bg()
        width, height = self.size
        result = []
        if self.cache:
            # 返回按钮
            b = ButtonText("返回", Color.create(255, 255, 255), 'HYHanHeiW.ttf', 16, rect_color=Color.create(55, 55, 55), size=(width - 50, 20))
            b.draw(self.screen)
            result.append({'class': b, 'args': [self.back]})
        return result

    def basic_bg(self):
        """
        设置基础背景
        :return:
        """
        # 设置开始界面
        show_ratio = settings.SHOW_RATIO
        size = width, height = settings.WIDTH * show_ratio, settings.HEIGHT * show_ratio
        # 设置视窗大小
        screen = pygame.display.set_mode(size)
        # 设置背景图
        Image(os.path.join(settings.ASSETS_PATH, 'background.jpeg'),
              rect=pygame.Rect(width/2, height/2, 1080, 1920),
              ratio=show_ratio).draw(screen)
        # 绘制背景
        return size, screen

    def back(self):
        APP.router.pop()

    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    ws_client.close()
                    sys.exit()
                # 重新刷整个页面
                self.create_map()
                for arg in self.handle_events:
                    class_ = arg['class']
                    params = arg['args']
                    class_.handle_event(event, *params)
                    class_.draw(self.screen)
                self.clock.tick(settings.FPS)
                if not self.running:
                    break
            pygame.display.update()

    def start(self):
        self.running = True
        self.is_start = True
        self.handle_events = self.create_map()
        self.run()

    def end(self):
        self.running = False



