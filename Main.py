import pygame
import thorpy # GUI library designed for pygame http://www.thorpy.org/documentation/userguide/cheatsheet.html
import sys
import Tank
import Mastermind

from pygame.locals import *

background_color = (0, 0, 255)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700
DISPLAYSURFACE = ""

fps = 30

player_1_score = 0
player_2_score = 0

def main():
    global DISPLAYSURFACE, FPSCLOCK

    pygame.init()  # initialize Pygame
    pygame.font.init() # initialize Pygame fonts for GUI
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('P2P Demonstration')
    FPSCLOCK = pygame.time.Clock()

    # TODO mastermind server setup

    draw_start_screen()


def submit_ip(event):
    value = event.el.get_value()
    connect(value)


def connect(ip):
    # TODO: validate that it's either "localhost" or a valid IP address; state = "connect" and connect if it is
    #  mastermind client setup
    print(ip)
    run_game()
    return


def draw_start_screen():
    global DISPLAYSURFACE, WINDOWWIDTH, WINDOWHEIGHT

    ip_field = thorpy.Inserter(name="Peer's IP", value="localhost", size=(100, 12))
    
    # can't figure out how to make a submit button! currently handling this with the submit reaction below
    # needs user to press enter/return
    cancel_button = thorpy.make_button("Cancel", func=terminate)
    
    box = thorpy.Box(elements=[ip_field, cancel_button])

    submit_reaction = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func=submit_ip,
                              event_args={"id":thorpy.constants.EVENT_INSERT})
    
    box.add_reaction(submit_reaction)
    box.set_topleft((WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 25)) # position the box
    box.blit() # draw the box's pixels so we don't need to update them individually for them to draw properly
    box.update()

    menu = thorpy.Menu(box)
    menu.play()
    for element in menu.get_population():
        element.surface = DISPLAYSURFACE
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            # respond to thorpy reactions
            menu.react(event)
    return


def run_game():
    # TODO computers flip a coin to see who is going first and who si on the left side of the screen
    roll_win = True
    my_turn = roll_win
    while True: # game loop
        player_1 = Tank.Tank(roll_win, 1200, 700)
        player_2 = Tank.Tank(~roll_win, 1200, 700)
        bullet_1 = None
        # TODO send and receive x and y cords
        while True:  # runs for one "turn"
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    terminate()
                elif event.type == MOUSEBUTTONDOWN and my_turn and bullet_1 == None:  # if the player clicks on the screen shoot a bullet
                    bullet_1 = player_1.shoot(pygame.mouse.get_pos())
                    # TODO send message with bullet info

            # TODO message handling stuff

            DISPLAYSURFACE.fill(background_color)

            if not bullet_1 == None:  # if there is a bullet update its position and check collisions
                bullet_1.update()
                bullet_1.draw(DISPLAYSURFACE)

                if collision(player_2, bullet_1):
                    # TODO send message saying that you are hit
                    break

                if bullet_1.get_x() < 0 or bullet_1.get_x() > WINDOWWIDTH:
                    bullet_1 = None  # if the bullet is off screen remove it

            print_score()  # draw players and score
            player_1.draw(DISPLAYSURFACE)
            player_2.draw(DISPLAYSURFACE)
            pygame.display.update()
            FPSCLOCK.tick(fps)


def terminate():
    # TODO disconnect
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
