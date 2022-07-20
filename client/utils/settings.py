import os


BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSETS_PATH = os.path.join(BASEDIR, 'asset')

WIDTH = 1080
HEIGHT = 1920

SHOW_RATIO = 0.4

FONT_TYPE = os.path.join(ASSETS_PATH, 'msyh.ttc')


FPS = 30