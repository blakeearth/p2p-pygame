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
            
            self.has_bullet = False
            self.has_roll = False
            self.has_coord = False

            self.bullet = None
            self.coord = None
            self.roll = None


        def callback_client_handle(self, connection_object, data):
            message_type = self.reader.message_type(data)
            if message_type == "shoot":
                self.has_bullet = True
                self.bullet = self.reader.read_shoot(data)
            elif message_type == "cord":
                self.has_coord = True
                self.coord = self.reader.read_cord(data)
            elif message_type == "roll":
                self.has_roll = True
                self.roll = self.reader.read_roll(data)
            

        def callback_connect_client(self, connection_object):
            print("Got some kind of connection.")
            return super(MastermindServerTCP,self).callback_connect_client(connection_object)            


        def has_bullet(self):
            return self.has_bullet


        def has_roll(self):
            return self.has_roll


        def has_coord(self):
            return self.has_coord

        def get_bullet(self):
            return self.bullet


        def get_roll(self):
            return self.roll


        def get_coord(self):
            return self.coord
