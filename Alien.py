from pgzero.builtins import Actor
from Creator import Creator
from pgzero.builtins import animate
from random import randint
import random


class Alien(Creator):

    def __init__(self, i):
        self.__x = 250+(i % 6)*100
        self.__y = 100+(int(i/6)*80)
        self.__images = ["alien1", "explosion5"]
        self.__alien = Actor(self.__images[0], (self.__x, self.__y))
        self.__alien.status = 1  # draw => visible
        self.__alien.type = 0

    def getActor(self):
        return self.__alien

    def getStatus(self):
        return self.__alien.status

    def update(self, move_sequence, level):
        movex = movey = 0
        if self.__alien.type == 0:
            if move_sequence < 10 or move_sequence > 30:
                movex = -20
            if move_sequence == 10 or move_sequence == 30:
                movey = 50 + (5 * level)
            if 10 < move_sequence < 30:
                movex = 20
            animate(self.__alien, pos=(self.__alien.x + movex, self.__alien.y + movey), duration=0.5, tween='linear')
            if randint(0, 1) == 0:
                self.__alien.image = "alien1"
            else:
                self.__alien.image = "alien1b"
        else:
            movey = 10
            if move_sequence < 10 or move_sequence > 30:
                movex = -40
            if move_sequence == 10 or move_sequence == 30:
                movex = -40
            if 10 < move_sequence < 30:
                movex = 40
            if self.__alien.x > 1000:
                self.__alien.x = 0
            elif self.__alien.x < 0:
                self.__alien.x = 1000
            animate(self.__alien, pos=(self.__alien.x + movex, self.__alien.y + movey), duration=0.5, tween='linear')
            if randint(0, 1) == 0:
                self.__alien.image = "alien1"
            else:
                self.__alien.image = "alien1b"
            if self.__alien.y > 670:
                self.__alien.status = 0

    @property
    def images(self):
        return self.__images
