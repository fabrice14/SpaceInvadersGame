from pgzero.builtins import sounds
from pgzero.builtins import Actor
from Creator import Creator


class LaserAlien(Creator):

    def __init__(self, x, y):
        self.__laserAlien = Actor("laser2", (x, y))
        self.__laserAlien.status = 1  # draw => visible
        sounds.ufo_highpitch.play()

    def getActor(self):
        return self.__laserAlien

    def getStatus(self):
        return self.__laserAlien.status

    def update(self, y):
        self.__laserAlien.y += y
        if self.__laserAlien.y > 680:
            self.__laserAlien.status = 0



