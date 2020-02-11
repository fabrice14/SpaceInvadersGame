from Liste import Liste
from Alien import Alien
from LaserAlien import LaserAlien


class BuilderList:

    aliensList = Liste()
    lasersList = Liste()

    def alien(self, i):
        self.aliensList.addElement(Alien(i))

    def laser(self, x, y):
        self.lasersList.addElement(LaserAlien(x, y))

    def removeAliens(self):
        self.aliensList.removeAllElement()

    def removeLasers(self):
        self.lasersList.removeAllElement()

