import pygame

class Settings():
    """储存《外星人入侵》所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.lb_bg_color = (10, 10, 10)
        self.lb_text_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (180, 180, 180)
        self.bullets_allowed = 5

        # 超级子弹设置
        self.super_bullet_color = (0, 255, 0)
        self.super_bullet_width = 6
        self.super_bullet_height = 150
        self.points_of_power = 1000

        # 外星人设置
        self.fleet_drop_speed = 10
        self.alien_bullet_color = (220, 220, 0)

        # 游戏加快节奏参数
        self.speedup_scale = 1.1

        # 击中外星人得分点数的提高速度
        self.score_scale = 1.2

        # 音效设置
        self.bullet_sound = pygame.mixer.Sound("sounds/bullet.wav")
        self.super_bullet_sound = pygame.mixer.Sound("sounds/super_bullet.wav")
        self.ship_hit_sound = pygame.mixer.Sound("sounds/ship_hit.wav")
        self.start_new_level_sound = pygame.mixer.Sound("sounds/start_new_level.wav")
        self.super_mode_sound = pygame.mixer.Sound("sounds/super_mode.wav")
        self.gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
        self.recordbroken_sound = pygame.mixer.Sound("sounds/recordbroken.wav")

        # 初始化游戏动态设置
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化动态参数"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.super_bullet_speed_factor = 30

        # 1表示右移，-1表示左移
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50


    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
