import pygame

class PlayernameInputbox:
    def __init__(self, screen):
        """初始化文本框的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width = 200
        self.height = 50
        self.box_color = (255, 255, 255)
        self.text_color = (20, 20, 20)
        self.font = pygame.font.SysFont("Calibri, Arial", 38)

        # 创建按钮的rect对象，并使其在屏幕上居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += 40

        self.text = "Your Name"
        self.login = False


    def draw_inputbox(self):
        """将输入文本渲染为图像，并显示"""
        self.text_image = self.font.render(self.text, True, self.text_color, self.box_color)
        self.text_image_rect = self.text_image.get_rect()
        self.text_image_rect.center = self.rect.center

        self.screen.fill(self.box_color, self.rect)
        self.screen.blit(self.text_image, self.text_image_rect)


    def key_down(self, event):
        """输入新文本"""
        unicode = event.unicode
        key = event.key

        if key == 8:
            # 退位键
            self.text = self.text[:-1]
            return
        if key == 301:
            # 切换大小写键
            return
        if key == 13:
            # 回车键
            return

        if unicode != "":
            char = unicode
        else:
            char = chr(key)

        self.text += char
