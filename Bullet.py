class Bullet:
    gravity = -9.8

    def __init__(self, x, y, xVol, yVol):
        self.x = x
        self.y = y
        self.yStart = self.y
        self.xVolocity = xVol
        self.yVolocity = yVol
        self.yInitialVol = self.yVolocity
        self.time = 0

    def update(self):
        global gravity

        self.time += 1

        newX = self.x + self.xVolocity
        newVol = self.yInitialVol + (gravity * self.time)

        newY = self.yStart + ((1/2) * (self.yInitialVol + newVol) * self.time)

        self.x = newX
        self.y = newY

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getxVol(self):
        return self.xVolocity

    def getyVol(self):
        return self.yVelocity


