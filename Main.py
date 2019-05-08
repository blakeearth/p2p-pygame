import pygame
import sys
import Tank
import Bullet

from pygame.locals import *

background_color = (0, 0, 255)

WINDOWIDTH = 1200
WINDOWHIGHT = 700
DISPLAYSURFACE = ""

fps = 30

player_1_score = 0
player_2_score = 0


def main():
    global DISPLAYSURFACE, FPSCLOCK

    pygame.init()  # initialize Pygame
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWIDTH, WINDOWHIGHT))
    pygame.display.set_caption('P2P Game')
    FPSCLOCK = pygame.time.Clock()

    draw_start_screen()
    while True:
        run_game()


def draw_start_screen():
    pass


def run_game():
    player_1 = Tank.Tank(True, 1200, 700)
    player_2 = Tank.Tank(False, 1200, 700)
    bullet_1 = None

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONDOWN:  # if the player clicks on the screen shoot a bullet
                bullet_1 = player_1.shoot(pygame.mouse.get_pos())

        DISPLAYSURFACE.fill(background_color)

        if not bullet_1 == None:  # if there is a bullet update its position and check collisions
            bullet_1.update()
            bullet_1.draw(DISPLAYSURFACE)

            if collision(player_2, bullet_1):
                return

            if bullet_1.get_x() < 0 or bullet_1.get_x() > WINDOWIDTH:
                bullet_1 = None  # if the bullet is off screen remove it

        print_score()  # draw players and score
        player_1.draw(DISPLAYSURFACE)
        player_2.draw(DISPLAYSURFACE)
        pygame.display.update()
        FPSCLOCK.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()


def print_score():
    pass


def collision(player, bullet):
    # create rectangles for collision comparison
    player_hitbox = pygame.Rect(player.get_x() - (player.get_width() / 2), player.get_y(), player.get_width(), player.get_height())
    bullet_hitbox = pygame.Rect(bullet.get_x() - bullet.get_radius(), bullet.get_y() - bullet.get_radius(), bullet.get_radius() * 2, bullet.get_radius() * 2)

    if player_hitbox.colliderect(bullet_hitbox):  # check collision ane return the answer
        return True
    else:
        return False


if __name__ == '__main__':
    main()