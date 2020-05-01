from pgzero.builtins import Actor
from pgzero.builtins import sounds
from Creator import Creator


class LaserPlayer(Creator):

    def __init__(self):
        self.__laserPlayer = Actor("laser1")
        self.__laserPlayer.status = 0

    def __del__(self):
        self.__laserPlayer.status = 0

    def getActor(self):
        return self.__laserPlayer

    def getStatus(self):
        return self.__laserPlayer.status

    def coordInit(self, x, y):
        self.__laserPlayer.x = x
        self.__laserPlayer.y = y

    def update(self, y):
        if self.__laserPlayer.status == 1:
            self.__laserPlayer.y -= y

    def GetLaserPlayer(self):
        return self
