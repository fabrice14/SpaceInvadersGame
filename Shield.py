from pgzero.builtins import keyboard
from pgzero.builtins import Actor
from pgzero.builtins import animate
import pygame.draw_py
from Creator import Creator


class Shield(Creator):

    def __init__(self):
        self.__shield = Actor("shield1")
        self.__shield.status = 0
        self.counter = 0

    def getActor(self):
        return self.__shield

    def getStatus(self):
        return self.__shield.status

    def update(self, x, y):
        if keyboard.K_LSHIFT and self.counter <= 3:
            self.__shield.x = x
            self.__shield.y = y
            self.__shield.status = 1
        else:
            self.__shield.status = 0


