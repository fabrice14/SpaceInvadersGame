from random import randint
from pgzero.loaders import sounds
from Alien import Alien
from LaserAlien import LaserAlien
from LaserPlayer import LaserPlayer
from Liste import Liste
from Player import Player
from Shield import Shield
from Game import Game


class Builder:

    aliensList = Liste()
    lasersList = Liste()
    game: Game

    def __init__(self):
        self.laserPlayer = LaserPlayer()
        self.shield = Shield()
        self.ship = Player(500, 650)
        self.move_sequence = 0
        self.score = 0

    @staticmethod
    def createGame():
        global game
        game = Game()
        return game

    def alien(self, i):
        self.aliensList.addElement(Alien(i))

    def laser(self, x, y):
        self.lasersList.addElement(LaserAlien(x, y))

    def removeAliens(self):
        self.aliensList.removeAllElement()

    def removeLasers(self):
        self.lasersList.removeAllElement()

    def updateLasers(self):
        self.laserPlayer.update(5)
        self.checkLaserHitAlien()
        if self.laserPlayer.getActor().y < 10 and self.ship.laserActive == 0:
            del self.laserPlayer
            self.laserPlayer = LaserPlayer()
            self.ship.laserActive = 1
        if self.lasersList.list:
            for element in self.lasersList.list:
                element.update(1 * game.level)
                self.checkLaserHitPlayer(element)
                self.checkLaserHitShield(element)
        self.aliensList.list = self.aliensList.clearListe()
        self.lasersList.list = self.lasersList.clearListe()

    def updateAliens(self):
        for element in self.aliensList.list:
            if randint(0, game.difficulty) == 0:
                if game.level > 1:
                    if element == self.aliensList.list[-1] or element == self.aliensList.list[randint(0, 18) % 6 == 0]:
                        element.getActor().type = 1
            element.update(self.move_sequence, game.level)
            if element.getActor().type == 0 and randint(0, game.difficulty) == 0:
                self.laser(element.getActor().x, element.getActor().y)
            if element.getActor().type == 1 and randint(0, game.difficulty) == 0:
                self.laser(element.getActor().x, element.getActor().y)
            if element.getActor().y > 620 and self.ship.getStatus() == 1 and element.getActor().type == 0:
                self.ship.getActor().status += 1
                sounds.shipexplosion.play()
            self.checkAlienHitPlayer(element)
        self.move_sequence += 1
        if self.move_sequence == 40:
            self.move_sequence = 0

    def checkAlienHitPlayer(self, alien):
        if self.ship.getActor().collidepoint(alien.getActor().x, alien.getActor().y):
            sounds.shipexplosion.play()
            self.ship.getActor().status += 1
            alien.getActor().image = alien.images[1]

    def checkLaserHitPlayer(self, laser):
        if self.shield.getStatus() == 0:
            if self.ship.getActor().collidepoint(laser.getActor().x, laser.getActor().y):
                sounds.shipexplosion.play()
                self.ship.getActor().status += 1

    def checkLaserHitShield(self, laser):
        if self.shield.getStatus() == 1:
            if self.shield.getActor().collidepoint(laser.getActor().x, laser.getActor().y):
                sounds.ufo_highpitch.play()
                laser.getActor().status = 0

    def checkLaserHitAlien(self):
        liste = self.aliensList.list
        for element in liste:
            if element.getActor().collidepoint((self.laserPlayer.getActor().x, self.laserPlayer.getActor().y)):
                sounds.invaderkilled.play()
                del self.laserPlayer
                self.laserPlayer = LaserPlayer()
                element.getActor().status = 0
                self.ship.laserActive = 1
                if element.getActor().type == 0:
                    game.score += 100
                else:
                    game.score += 200
                    game.drawscore = True
                    game.coord = [element.getActor().x, element.getActor().y]
