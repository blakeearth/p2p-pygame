import pygame
from pygame.locals import *
import thorpy # GUI library designed for pygame http://www.thorpy.org/documentation/userguide/cheatsheet.html
import Mastermind

import random
import sys

import Tank
import Server

background_color = (0, 0, 255)

WINDOWWIDTH = 1200
WINDOWHEIGHT = 700
DISPLAYSURFACE = ""

fps = 30

server_port = 0
client_port = 0

server = None
client = None

player_1_score = 0
player_2_score = 0


def main():
    global DISPLAYSURFACE, FPSCLOCK

    pygame.init()  # initialize Pygame
    pygame.font.init() # initialize Pygame fonts for GUI
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('P2P Demonstration')
    FPSCLOCK = pygame.time.Clock()

    draw_start_screen()


def submit_ip(event):
    value = event.el.get_value()
    connect(value)


def submit_server(port_field):
    global server_port, server

    port = port_field.get_value()
    
    print("Starting a server on localhost with port " + port)
    server_port = int(float(port))

    server = Server.Server()
    server.connect("localhost", server_port)
    try:
        server.accepting_allow()
    except:
        # From example: only way to break is with an exception
        pass


def submit_peer(ip_field, port_field):
    global client_port

    client_port = int(float(port_field.get_value()))
    client_ip = ip_field.get_value()
    
    ip = client_ip
    port = client_port
    connect(ip, port)


def connect(ip, port):
    # TODO: validate that it's either "localhost" or a valid IP address; state = "connect" and connect if it is
    #  mastermind client setup

    global client_port, client
    
    print(ip)
    client = Mastermind.MastermindClientTCP(5.0, 10.0)
    client.connect(ip, client_port)
    
    run_game()
    return


def draw_start_screen():
    global DISPLAYSURFACE, WINDOWWIDTH, WINDOWHEIGHT, server_port

    server_port_field = thorpy.Inserter(name="My Host Port", value="23865", size=(100, 12))

    submit_server_button = thorpy.make_button("Submit", func=submit_server,
                                                   params={"port_field":server_port_field})
    
    server_box = thorpy.Box(elements=[server_port_field, submit_server_button])
    
    server_box.set_topleft((WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 25)) # position the box
    server_box.blit() # draw the box's pixels so we don't need to update them individually for them to draw properly
    server_box.update()

    # peer information box

    peer_ip_field = thorpy.Inserter(name="Peer's IP", value="localhost", size=(150, 12))

    peer_port_field = thorpy.Inserter(name="Peer's Host Port", value="23867", size=(100, 12))

    submit_peer_button = thorpy.make_button("Submit", func=submit_peer,
                                                   params={"ip_field": peer_ip_field,
                                                           "port_field": peer_port_field})

    peer_box = thorpy.Box(elements=[peer_ip_field, peer_port_field, submit_peer_button])
    peer_box.set_topleft((WINDOWWIDTH / 2 - 100, WINDOWHEIGHT / 2 - 50)) # position the box

    thorpy.set_launcher(submit_server_button, peer_box)

    menu = thorpy.Menu(server_box)
    menu.play()
    return


def run_game():
    global player_2_score, player_1_score
    # computers flip a coin to see who is going first and who is on the left side of the screen
    our_roll = random.randrange(1, 6)
    their_roll = our_roll
    roll_message = {"type": "roll", "number": our_roll}
    client.send(roll_message)
    while True:
        if server.has_roll():
            their_roll = server.get_roll()
            if our_roll == their_roll:
                our_roll = random.randrange(1, 6)
                roll_message["number"] = our_roll
                client.send(roll_message)
            else:
                break
    
    roll_win = our_roll > their_roll
    my_turn = roll_win
    while True: # game loop
        player_1 = Tank.Tank(roll_win, 1200, 700)
        player_2 = Tank.Tank(~roll_win, 1200, 700)
        bullet_1 = None
        # TODO send and receive x and y cords
        cord_message = {"type": "cord", "x": player_1.get_x(), "y": player_1.get_y()}
        client.send(cord_message)
        their_cords = 0

        while True:
            if server.has_coords() == True:
                their_cords = server.get_coords()
                break

        player_2.set_location(their_cords[0], their_cords[1])

        while True:  # runs for one "turn"
            for event in pygame.event.get():  # event handling loop
                if event.type == QUIT:
                    terminate()
                elif event.type == MOUSEBUTTONDOWN and my_turn and bullet_1 == None:  # if the player clicks on the screen shoot a bullet
                    bullet_1 = player_1.shoot(pygame.mouse.get_pos())
                    my_turn = False
                    # send message with bullet info
                    shoot_message = {"type": "shoot", "x": bullet_1.get_x(), "y": bullet_1.get_y(), "x_vol": bullet_1.getx_vel(), "y_vol": bullet_1.gety_vel()}
                    client.send(shoot_message)

            # TODO message handling stuff
            if server.has_bullet() == True:
                bullet_1 = server.get_bullet()
                my_turn = True

            if server.has_coords() == True:
                player_1_score += 1
                break

            DISPLAYSURFACE.fill(background_color)

            if not bullet_1 == None:  # if there is a bullet update its position and check collisions
                bullet_1.update()
                bullet_1.draw(DISPLAYSURFACE)

                if collision(player_1, bullet_1) and my_turn == True:
                    # send message saying that you are hit
                    player_2_score += 1
                    break

                if bullet_1.get_x() < 0 or bullet_1.get_x() > WINDOWWIDTH:
                    bullet_1 = None  # if the bullet is off screen remove it

            print_score(player_1.left_or_right())  # draw players and score
            player_1.draw(DISPLAYSURFACE)
            player_2.draw(DISPLAYSURFACE)
            pygame.display.update()
            FPSCLOCK.tick(fps)


def terminate():
    # TODO disconnect
    client.disconnect()
    server.disconnect_clients()
    server.disconnect()

    pygame.quit()
    sys.exit()


def print_score(player_1_side):
    global player_1_score, player_2_score
    font_obj = pygame.font.Font('freesansbold.ttf', 16)

    if player_1_side == True:
        text_surface_obj = font_obj.render("player 1 score: " + str(player_1_score) + "| player 2 score" + str(player_2_score), True, (255, 255, 255))
    else:
        text_surface_obj = font_obj.render("player 2 score: " + str(player_2_score) + "| player 1 score" + str(player_1_score), True, (255, 255, 255))

    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (WINDOWWIDTH / 2, 30)

    DISPLAYSURFACE.blit(text_surface_obj, text_rect_obj)
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
