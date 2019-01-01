import sys
import pygame
import random
from bullet import Bullet
from super_bullet import SuperBullet
from alien import Alien
from alien_bullet import AlienBullet
from time import sleep
from threading import Timer



"""
用户操作响应
"""

def check_events(ai_settings, screen, ship, bullets, aliens, stats, play_button, scoreboard, alien_bullets, super_bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, scoreboard, super_bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, bullets, aliens, stats, play_button, mouse_x, mouse_y, scoreboard, alien_bullets)


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, scoreboard, super_bullets):
    """响应按键按下"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_UP:
        activate_super_mode(ai_settings, ship, stats, scoreboard)
    elif event.key == pygame.K_LSHIFT:
        fire_super_bullet(ai_settings, screen, ship, stats, super_bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应按键松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, ship, bullets, aliens, stats, play_button, mouse_x, mouse_y, scoreboard, alien_bullets):
    """检查开始游戏按钮是否被按下，并响应"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏参数
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        # 重置记分牌
        scoreboard.prep_images()
        # 设置状态为激活
        stats.game_active = True
        # 清屏并创建新的一群外星人
        clear_and_create_fleet(ai_settings, screen, ship, bullets, aliens, alien_bullets)


def fire_super_bullet(ai_settings, screen, ship, stats, super_bullets):
    if stats.power >= ai_settings.points_of_power:
        new_super_bullet = SuperBullet(ai_settings, screen, ship)
        super_bullets.add(new_super_bullet)
        stats.power -= ai_settings.points_of_power


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def activate_super_mode(ai_settings, ship, stats, scoreboard):
    """响应进入无敌模式"""
    if stats.power >= ai_settings.points_of_power:
        ship.super_mode = True
        stats.power -= ai_settings.points_of_power
        scoreboard.prep_power()
        Timer(5, quit_super_mode, args=[ship]).start()

def quit_super_mode(ship):
    ship.super_mode = False


"""
子弹参数更新（包括超级子弹）
"""

def update_bullets(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, super_bullets):
    """更新子弹位置并检查碰撞"""
    # 更新子弹位置
    bullets.update()
    super_bullets.update()
    # 删除已超出范围的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    for super_bullet in super_bullets.copy():
        if super_bullet.rect.bottom <= 0:
            super_bullets.remove(super_bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, super_bullets)


def check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, super_bullets):
    """响应子弹击中外星人"""
    # 检查是否有子弹击中外星人，若有，删除对应的子弹与外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    super_collisions = pygame.sprite.groupcollide(super_bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            stats.power += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
            scoreboard.prep_power()
        # 检查是否打破历史记录
        check_high_score(stats, scoreboard)

    if super_collisions:
        for aliens in super_collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            stats.power += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
            scoreboard.prep_power()
        # 检查是否打破历史记录
        check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # 外星人被消灭干净，开启新等级
        start_new_level(ai_settings, screen, ship, bullets, aliens, stats, scoreboard)


def start_new_level(ai_settings, screen, ship, bullets, aliens, stats, scoreboard):
    """响应外星人被消灭干净"""
    bullets.empty()
    ai_settings.increase_speed()
    create_fleet(ai_settings, screen, ship, aliens)
    stats.level += 1
    scoreboard.prep_level()


def check_high_score(stats, scoreboard):
    """响应打破历史记录"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


"""
外星人参数更新
"""

def update_aliens(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets):
    """更新所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets)

    check_aliens_bottom(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达屏幕边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将外星人整体下移一行并改变移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets):
    """检查是否有外星人撞到屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船与外星人相撞一样处理
            ship_hit(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets)
            break

def ship_hit(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets):
    """响应飞船与外星人碰撞"""
    if stats.ships_left > 0:
        # 将剩余飞船数减一
        stats.ships_left -= 1
        # 清空外星人和子弹列表并创建一批新外星人
        clear_and_create_fleet(ai_settings, screen, ship, bullets, aliens, alien_bullets)
        # 更新剩余飞船数
        scoreboard.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    sleep(0.5)

def clear_and_create_fleet(ai_settings, screen, ship, bullets, aliens, alien_bullets):
    """清空外星人和子弹列表并创建一批新外星人"""
    # 清空外星人和子弹列表
    bullets.empty()
    aliens.empty()
    alien_bullets.empty()

    # 创建一批新的外星人，并将飞船放到屏幕底部中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    """计算一行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, alien_height, ship_height):
    """计算可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 6 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并把它加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


"""
外星人子弹更新
"""

def update_aliens_fire_bullet(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets):
    """更新外星人发射的子弹"""
    for alien in aliens.sprites():
        flag_is_last_line = True
        for alien_next in aliens.sprites():
            if (alien.rect.y + alien.rect.height * 2 == alien_next.rect.y
            and alien.rect.x == alien_next.rect.x):
                flag_is_last_line = False
                break
        if flag_is_last_line:
            """外星人有一定的概率发射子弹"""
            if random.randint(0,3000) < 1:
                new_alien_bullet = AlienBullet(ai_settings, screen, alien)
                alien_bullets.add(new_alien_bullet)

    check_alien_bullet_ship_collision(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets)
    alien_bullets.update()



def check_alien_bullet_ship_collision(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets):
    """响应外星人子弹击中飞船"""
    for alien_bullet in alien_bullets.sprites():
        if alien_bullet.rect.colliderect(ship.rect) and not ship.super_mode:
            ship_hit(ai_settings, screen, ship, bullets, aliens, stats, scoreboard, alien_bullets)
            break


"""
屏幕更新
"""

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, scoreboard, alien_bullets, super_bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 绘制全部子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien_bullet in alien_bullets.sprites():
        alien_bullet.draw_alien_bullet()
    for super_bullet in super_bullets.sprites():
        super_bullet.draw_bullet()
    # 绘制玩家飞船
    ship.blitme()
    # 绘制全部外星人
    aliens.draw(screen)
    scoreboard.ships.draw(screen)
    # 显示得分
    scoreboard.show_score()

    # 如果游戏处于非活动状态，就显示Play按钮
    if stats.game_active == False:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
