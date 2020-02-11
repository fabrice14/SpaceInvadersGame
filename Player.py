from pgzero.builtins import keyboard
from pgzero.builtins import Actor
from Creator import Creator


class Player(Creator):

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__images = ["player", "explosion1", "explosion2", "explosion3", "explosion4", "explosion5"]
        self.__player = Actor(self.__images[0], (self.__x, self.__y))
        self.__player.status = 1
        self.__laserActive = 1

    def getActor(self):
        return self.__player

    def getStatus(self):
        return self.__player.status

    def update(self, a=0, b=0):
        if keyboard.right and self.__player.x < 950:
            self.__player.x += 3
        if keyboard.left and self.__player.x > 50:
            self.__player.x -= 3

    @property
    def images(self):
        return self.__images

    @property
    def laserActive(self):
        return self.__laserActive

    @laserActive.setter
    def laserActive(self, a):
        self.__laserActive = a
