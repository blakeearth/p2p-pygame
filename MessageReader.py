import Bullet

class MessageReader:

    def __init__(self):
        return

    def message_type(self, message):
        return message["type"]

    def read_shoot(self, message):
        return Bullet.Bullet(message["x"], message["y"], message["x_vol"], message["y_vol"])

    def read_cord(self, message, tank):
        tank.set_location(message["x"], message["y"])

    def read_roll(self, message):
        return message["number"]
