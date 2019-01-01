import pygame
from bullet import Bullet


class SuperBullet(Bullet):
    """一个对飞船发射的超级子弹进行管理的类"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__(ai_settings, screen, ship)

        # 设置超级子弹宽高，颜色及速度
        self.rect.width = ai_settings.super_bullet_width
        self.rect.height = ai_settings.super_bullet_height
        self.color = ai_settings.super_bullet_color
        self.speed_factor = ai_settings.super_bullet_speed_factor
