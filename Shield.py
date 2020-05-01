from pgzero.builtins import keyboard
from pgzero.builtins import Actor
from pgzero.builtins import animate
import pygame.draw_py
from Creator import Creator


class Shield(Creator):

    def __init__(self):
        self.__shield = Actor("shield1")
        self.__shield.status = 0
        self.__counter = 3
        self.__counterTime = 0

    def getActor(self):
        return self.__shield

    def getStatus(self):
        return self.__shield.status

    @property
    def counter(self):
        return self.__counter

    @property
    def counterTime(self):
        return self.__counterTime

    @counter.setter
    def counter(self, i):
        self.__counter = i

    @counterTime.setter
    def counterTime(self, i):
        self.__counterTime = i

    def update(self, x, y):
        if keyboard.K_LSHIFT and self.__counter >= 0 and self.__counterTime < 100:
            self.__shield.status = 1
            self.__shield.x = x
            self.__shield.y = y
        else:
            self.__shield.status = 0
