class Settings():
    """储存《外星人入侵》所有设置的类"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # 外星人设置
        self.fleet_drop_speed = 10

        # 游戏加快节奏参数
        self.speedup_scale = 1.1

        # 击中外星人得分点数的提高速度
        self.score_scale = 1.5

        # 初始化游戏动态设置
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """初始化动态参数"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

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
