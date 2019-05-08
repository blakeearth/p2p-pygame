import pygame


class Bullet:
    color = (255, 0, 0)
    gravity = -9.8
    radius = 10

    def __init__(self, x, y, xVol, yVol):
        self.x = x
        self.y = y
        self.yStart = self.y
        self.xVelocity = xVol
        self.yVelocity = yVol
        self.yInitialVol = self.yVelocity
        self.time = 0

    def update(self):

        self.time += 0.1  # increment the time for calculations

        newX = self.x + (self.xVelocity / 10)  # calculate the new x cord
        newVol = self.yInitialVol + (self.gravity * self.time)  # calculate the new y velocity

        newY = self.yStart + (-((1/2) * (self.yInitialVol + newVol) * self.time))  # calculate new y cord

        self.x = int(newX)  # update x and y cords and yVelocity
        self.y = int(newY)
        self.yVelocity = newVol

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_radius(self):
        return self.radius

    def getx_vel(self):
        return self.xVelocity

    def gety_vel(self):
        return self.yVelocity

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, 0)
        return


