import os
import sys

import pygame

from game.basic.button import Image
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

    def create_map(self):
        self.size, self.screen = self.basic_bg()
        return [{'class': None, 'args': []}]

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

    def run(self, *args):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    ws_client.close()
                    sys.exit()
                # 重新刷整个页面
                self.create_map()
                for arg in args:
                    class_ = arg['class']
                    params = arg['args']
                    class_.handle_event(event, *params)
                    class_.draw(self.screen)
                self.clock.tick(settings.FPS)
            pygame.display.update()

    def start(self):
        params = self.create_map()
        self.run(*params)

    def end(self):
        self.running = False



