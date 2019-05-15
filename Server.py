from Mastermind import *

import threading
from time import gmtime, strftime

from MessageReader import MessageReader
from Bullet import Bullet

class Server(MastermindServerCallbacksDebug, MastermindServerTCP):
        def __init__(self):
            MastermindServerTCP.__init__(self, 0.5,0.5,60.0)
            #self.mutex = threading.Lock()
            
            self.reader = MessageReader()
            
            self.new_bullet = False
            self.new_roll = False
            self.new_coord = False

            self.bullet = None
            self.coord = None
            self.roll = None


        def callback_client_handle(self, connection_object, data):
            message_type = self.reader.message_type(data)
            if message_type == "shoot":
                self.new_bullet = True
                self.bullet = self.reader.read_shoot(data)
            elif message_type == "cord":
                self.new_coord = True
                self.coord = self.reader.read_cord(data)
            elif message_type == "roll":
                self.new_roll = True
                self.roll = self.reader.read_roll(data)
            

        def callback_connect_client(self, connection_object):
            print("Got some kind of connection.")
            return super(MastermindServerTCP,self).callback_connect_client(connection_object)            


        def has_bullet(self):
            self.new_bullet = False
            return self.new_bullet


        def has_roll(self):
            self.new_roll = False
            return self.new_roll


        def has_coord(self):
            self.new_coord = False
            return self.new_coord

        def get_bullet(self):
            return self.bullet


        def get_roll(self):
            return self.roll


        def get_coord(self):
            return self.coord
