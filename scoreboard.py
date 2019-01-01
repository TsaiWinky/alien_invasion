import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化相关参数"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 字体设置
        self.text_color = (230, 230, 230)
        self.font = pygame.font.Font('C:\Windows\Fonts\Calibri.ttf', 28)

        # 准备得分图像、等级及剩余飞船图像
        self.prep_images()


    def show_score(self):
        """在屏幕上显示得分、历史记录、等级、大招数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.power_image, self.power_rect)


    def prep_images(self):
        """准备各个图像(得分,历史记录,等级,剩余飞船)"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_power()


    def prep_score(self):
        """将得分渲染为图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 20
        self.score_rect.right = self.screen_rect.right - 20


    def prep_high_score(self):
        """将历史记录渲染为图像"""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = "Record: " + "{:,}".format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 将历史记录放在屏幕左下角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.bottom = self.screen_rect.bottom - 10
        self.high_score_rect.left = self.screen_rect.left + 10


    def prep_level(self):
        """将等级渲染为图像"""
        level_str = "Level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom
        self.level_rect.right = self.screen_rect.right - 20


    def prep_ships(self):
        """显示剩余飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = pygame.transform.scale(ship.image,(25, 27))
            ship.rect = ship.image.get_rect()
            ship.rect.x = ship.rect.width * ship_number + 10
            ship.rect.y = 10
            self.ships.add(ship)


    def prep_power(self):
        """将大招渲染为图像"""
        power_num = int(self.stats.power / self.ai_settings.points_of_power)
        power_str = "Power: " + str(power_num)
        self.power_image = self.font.render(power_str, True, self.text_color, self.ai_settings.bg_color)

        # 将大招数放在屏幕右下
        self.power_rect = self.power_image.get_rect()
        self.power_rect.bottom = self.screen_rect.bottom - 10
        self.power_rect.right = self.screen_rect.right - 10
