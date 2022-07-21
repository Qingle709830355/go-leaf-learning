import os

import pygame
from pygame import freetype

from utils import settings


os.environ["SDL_IME_SHOW_UI"] = "1"


class Color:
    # 自定义颜色
    ACHIEVEMENT = (220, 160, 87)
    VERSION = (220, 160, 87)

    # 固定颜色
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GREY = (128, 128, 128)  # 中性灰
    TRANSPARENT = (255, 255, 255, 0)  # 白色的完全透明

    @staticmethod
    def create(r, g, b):
        return (r, g, b)


class Text:
    def __init__(self, text: str, text_color: Color, font_type: str, font_size: int,
                 rect_color: Color = None,
                 size=(0, 0)):
        """
        text: 文本内容，如'大学生模拟器'，注意是字符串形式
        text_color: 字体颜色，如Color.WHITE、COLOR.BLACK
        font_type: 字体文件(.ttc)，如'msyh.ttc'，注意是字符串形式
        font_size: 字体大小，如20、10
        """
        self.text = text
        self.text_color = text_color
        self.font_type = font_type
        self.font_size = font_size
        self.center_x, self.center_y = size

        font = pygame.font.Font(os.path.join(settings.ASSETS_PATH, self.font_type), self.font_size)
        self.text_image = font.render(self.text, True, self.text_color, rect_color).convert_alpha()
        self.text_width = self.text_image.get_width()
        self.text_height = self.text_image.get_height()

    def draw(self, surface: pygame.Surface):
        """
        surface: 文本放置的表面
        center_x, center_y: 文本放置在表面的<中心坐标>
        """
        upperleft_x = self.center_x - self.text_width / 2
        upperleft_y = self.center_y - self.text_height / 2
        surface.blit(self.text_image, (upperleft_x, upperleft_y))


class Image:
    def __init__(self, img_name: str, rect=pygame.Rect(0, 0, 1080, 1920), ratio=0.4):
        """
        img_name: 图片文件名，如'background.jpg'、'ink.png',注意为字符串
        ratio: 图片缩放比例，与主屏幕相适应，默认值为0.4
        """
        self.img_name = img_name
        self.ratio = ratio

        self.image_1080x1920 = pygame.image.load(self.img_name).convert()
        self.img_height, self.img_width = rect.height, rect.width

        self.size_scaled = self.img_width * self.ratio, self.img_height * self.ratio

        self.image_scaled = pygame.transform.smoothscale(self.image_1080x1920, self.size_scaled)
        self.img_width_scaled = self.image_scaled.get_width()
        self.img_height_scaled = self.image_scaled.get_height()
        self.center_x, self.center_y = rect.x, rect.y

    def draw(self, surface: pygame.Surface):
        """
        surface: 图片放置的表面
        center_x, center_y: 图片放置在表面的<中心坐标>
        """
        upperleft_x = self.center_x - self.img_width_scaled / 2
        upperleft_y = self.center_y - self.img_height_scaled / 2
        surface.blit(self.image_scaled, (upperleft_x, upperleft_y))


class ColorSurface:
    def __init__(self, color, width, height):
        self.color = color
        self.width = width
        self.height = height

        self.color_image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.color_image.fill(self.color)

    def draw(self, surface: pygame.Surface, center_x, center_y):
        upperleft_x = center_x - self.width / 2
        upperleft_y = center_y - self.height / 2
        surface.blit(self.color_image, (upperleft_x, upperleft_y))


class ButtonText(Text):
    def __init__(self, text: str, text_color: Color, font_type: str, font_size: int, rect_color: Color, size):
        super().__init__(text, text_color, font_type, font_size, rect_color, size)
        self.rect = self.text_image.get_rect()

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        self.rect.center = self.center_x, self.center_y

    def handle_event(self, event, command, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                command(*args)
                return True
        return False


class ButtonImage(Image):
    def __init__(self, img_name: str, rect=pygame.Rect(0, 0, 1080, 1920), ratio=0.4):
        super().__init__(img_name, rect, ratio)
        self.rect = self.image_scaled.get_rect()

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        self.rect.center = self.center_x, self.center_y

    def handle_event(self, event, command, *args):
        # 监听到操作 返回True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                command(*args)
                return True
        return False


class ButtonColorSurface(ColorSurface):
    def __init__(self, color, width, height):
        super().__init__(color, width, height)
        self.rect = self.color_image.get_rect()

    def draw(self, surface: pygame.Surface, center_x, center_y):
        super().draw(surface, center_x, center_y)
        self.rect.center = center_x, center_y

    def handle_event(self, event, command, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.hovered = self.rect.collidepoint(event.pos)
            if self.hovered:
                command(*args)
            return True
        return False


class InputBox:
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32),
                 color_inactive=Color.create(0, 0, 0),
                 coloc_active=pygame.Color("dodgerblue2"),
                 prompt='|',
                 max_width=200,
                 font_size=24, font_small_size=16) -> None:
        """
        rect，传入矩形实体，传达输入框的位置和大小
        """
        self.boxBody: pygame.Rect = rect
        self.color_inactive = color_inactive  # 未被选中的颜色
        self.color_active = coloc_active  # 被选中的颜色
        self.text_color = self.color_inactive  # 当前颜色，初始为未激活颜色
        self.active = False
        self.done = False
        self.prompt = prompt
        self._ime_text = ''
        self._ime_editing = False
        self._ime_editing_text = ''
        self._ime_text_pos = 0
        self._ime_editing_pos = 0
        self.FONT_NAMES = '华文宋体'
        self.chat_list = []
        self.CHAT_BOX_POS = rect
        self.CHAT_LIST_MAXSIZE = 20
        self.font = freetype.SysFont(self.FONT_NAMES, font_size)
        self.font_small = freetype.SysFont(self.FONT_NAMES, font_small_size)
        self.max_width = max_width
        self.font_size = font_size
        self.font_small_size = font_small_size

    def draw(self, screen: pygame.surface.Surface):
        # Chat List updates
        # Chat box updates
        start_pos = self.CHAT_BOX_POS.copy()
        ime_text_l = self.prompt + self._ime_text[0: self._ime_text_pos]
        ime_text_m = (
                self._ime_editing_text[0: self._ime_editing_pos]
                + "|"
                + self._ime_editing_text[self._ime_editing_pos:]
        )
        ime_text_r = self._ime_text[self._ime_text_pos:]
        rect_text_l = self.font.render_to(
            screen, start_pos, ime_text_l, self.text_color
        )
        start_pos.x += rect_text_l.width
        #
        # # Editing texts should be underlined
        rect_text_m = self.font.render_to(
            screen,
            start_pos,
            ime_text_m,
            self.text_color,
            None,
            freetype.STYLE_UNDERLINE,
        )
        start_pos.x += rect_text_m.width
        self.font.render_to(screen, start_pos, ime_text_r, self.text_color)
        self.boxBody.w = self.max_width
        pygame.draw.rect(screen, self.text_color, self.boxBody, 2)

    def handle_event(self, event: pygame.event.Event, command=None, *args):
        have_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            have_run = True
            if self.boxBody.collidepoint(event.pos):  # 若按下鼠标且位置在文本框
                self.active = not self.active
            else:
                self.active = False
            self.text_color = self.color_active if (
                self.active) else self.color_inactive
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            have_run = True
            if self._ime_editing:
                if len(self._ime_editing_text) == 0:
                    self._ime_editing = False
                return

            if self._ime_editing:
                if len(self._ime_editing_text) == 0:
                    self._ime_editing = False
                return

            if event.key == pygame.K_BACKSPACE:
                have_run = True
                if len(self._ime_text) > 0 and self._ime_text_pos > 0:
                    self._ime_text = (
                            self._ime_text[0: self._ime_text_pos - 1]
                            + self._ime_text[self._ime_text_pos:]
                    )
                    self._ime_text_pos = max(0, self._ime_text_pos - 1)

            elif event.key == pygame.K_DELETE:
                have_run = True
                self._ime_text = (
                        self._ime_text[0: self._ime_text_pos]
                        + self._ime_text[self._ime_text_pos + 1:]
                )
            elif event.key == pygame.K_LEFT:
                have_run = True
                self._ime_text_pos = max(0, self._ime_text_pos - 1)
            elif event.key == pygame.K_RIGHT:
                self._ime_text_pos = min(
                    len(self._ime_text), self._ime_text_pos + 1
                )

        elif event.type == pygame.TEXTEDITING:
            have_run = True
            self._ime_editing = True
            self._ime_editing_text = event.text
            self._ime_editing_pos = event.start

        elif event.type == pygame.TEXTINPUT:
            have_run = True
            self._ime_editing = False
            self._ime_editing_text = ""
            self._ime_text = (
                    self._ime_text[0: self._ime_text_pos]
                    + event.text
                    + self._ime_text[self._ime_text_pos:]
            )
            self._ime_text_pos += len(event.text)
        return have_run


class ShowBox(InputBox):
    def __init__(self, rect: pygame.Rect = pygame.Rect(100, 100, 140, 32), color_inactive=Color.create(91, 91, 91),
                 coloc_active=pygame.Color("dodgerblue2"), prompt='|', max_width=200,
                 font_size=24, font_small_size=16) -> None:
        super().__init__(rect, color_inactive, coloc_active, prompt, max_width, font_size, font_small_size)
        self.chat_list = []

    def draw(self, screen: pygame.surface.Surface):
        # 从最后开始展示
        super(ShowBox, self).draw(screen)
        for index in range(len(self.chat_list)-1, -1, -1):
            msg, username, position = self.chat_list[index]
            x1 = x2 = position[0]
            if x1 is None:
                x1 = settings.WIDTH * settings.SHOW_RATIO - (len(msg) * self.font_size + 12)
                x2 = settings.WIDTH * settings.SHOW_RATIO - (len(username) * self.font_small_size + 12)
            self.font.render_to(screen, (x1, position[1]), msg, self.text_color)
            self.font_small.render_to(screen, (x2, position[1] - self.font_small_size - 4), f'{username}:',
                                      self.text_color)

    def handle_event(self, event: pygame.event.Event, command=None, *args):
        result = command(self, *args)
        if len(result) == len(self.chat_list):
            return False
        self.chat_list = result
        return True

