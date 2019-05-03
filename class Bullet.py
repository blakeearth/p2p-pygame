class Bullet:
    gravity = 9.8

    def __init__(self, x, y, xVol, yVol):
        self.x = x
        self.y = y
        self.xVolocity = xVol
        self.yVolocity = yVol

    def update(self):
        pass

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getxVol(self):
        return self.xVolocity

    def getyVol(self):
        return self.yVelocity


