import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from playername_inputbox import PlayernameInputbox


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建一艘飞船, 一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    alien_bullets = Group()
    super_bullets = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建一个用于游戏统计信息的示例，并创建记分牌
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # 创建开始游戏按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建玩家名字文本输入框
    playername_inputbox = PlayernameInputbox(screen)

    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, aliens, stats, play_button, scoreboard, alien_bullets, super_bullets, playername_inputbox)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, super_bullets)
            gf.update_aliens(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets, super_bullets)
            gf.update_aliens_fire_bullet(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets, super_bullets)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, scoreboard, alien_bullets, super_bullets, playername_inputbox)


run_game()
