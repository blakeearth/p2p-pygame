import pygame.draw
import random
import math
import Bullet


class Tank:
    """The class used to represent both players' tanks in-game"""
    appx_frames_to_dest = 30

    def __init__(self, left, surface_width, max_y=100):
        self.left = left
        self.max_y = max_y
        self.surface_width = surface_width
        self.y = random.randint(0, max_y)

        if left:  # gives the tank a random staring x position on its side of the screen
            self.angle = -math.pi / 4
            self.x = random.randint(0, self.surface_width / 4)
        else:
            self.angle = (-math.pi * 3) / 4
            self.x = random.randint(3 * (self.surface_width / 4), self.surface_width)

        self.color = 81, 122, 81
        self.width = 100
        self.height = 50

    def change_location(self):
        self.y = random.randint(0, self.max_y)

        if self.left:  # gives the tank a random staring x position on its side of the screen
            self.angle = -math.pi / 4
            self.x = random.randint(0, self.surface_width / 4)
        else:
            self.angle = (-math.pi * 3) / 4
            self.x = random.randint(3 * (self.surface_width / 4), self.surface_width)

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def get_y(self):
        # to be used to send new ys to peers (or after new tank)
        return self.y

    def get_x(self):  # used for checking collision and sending new xs to peers
        return self.x

    def get_width(self):  # used for checking collision
        return self.width

    def get_height(self):  # used for checking collision
        return self.height

    def shoot(self, mouse):
        # x is used to construct x-velocity of bullet
        # y is used to construct y-velocity of bullet
        # both are used to generate a new angle for the gun/arm (using arctan)
        angle_x = mouse[0] - self.x
        angle_y = mouse[1] - self.y
        self.angle = math.atan2(angle_y, angle_x)

        x_vel = mouse[0] - self.x
        y_vel = self.y - mouse[1]

        # note: this will likely *not* come out of the arm yet
        return Bullet.Bullet(self.x, self.y, x_vel, y_vel)

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def rotate_point(self, origin, point, angle):
        point_at_origin = (point[0] - origin[0], point[1] - origin[1])

        rotated_point = (point_at_origin[0] * math.cos(angle) - point_at_origin[1] * math.sin(angle), point_at_origin[0] * math.sin(angle) + point_at_origin[1] * math.cos(angle))

        new_point = (rotated_point[0] + origin[0], rotated_point[1] + origin[1])
        return new_point

    def draw(self, surface):
        # draw the tank arm - rectangles are aligned with axes, so must be a polygon]
        # vertices of the arm:
        v1 = (self.x, self.y)
        v2 = (self.x, self.y + (1 / 4) * self.height)
        v3 = (self.x + self.width, self.y)
        v4 = (self.x + self.width, self.y + (1 / 4) * self.height)

        arm_origin = (self.x, self.y)

        # rotated vertices of the arm:
        r1 = self.rotate_point(arm_origin, v1, self.angle)
        r2 = self.rotate_point(arm_origin, v2, self.angle)
        r3 = self.rotate_point(arm_origin, v3, self.angle)
        r4 = self.rotate_point(arm_origin, v4, self.angle)
        
        pygame.draw.polygon(surface, self.color, [r1, r2, r3, r4])

        # draw the tank body
        body = pygame.Rect(self.x - (self.width / 2), self.y, self.width, self.height)
        pygame.draw.rect(surface, self.color, body)
