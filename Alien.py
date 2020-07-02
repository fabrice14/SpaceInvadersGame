
from pgzero.builtins import Actor
from Creator import Creator
from pgzero.builtins import animate
from random import randint
from pgzero.loaders import sounds


class Alien(Creator):

    def __init__(self, i):
        self.__x = 200+(i % 8)*90
        self.__y = 80+(int(i/8)*80)
        self.__images = ["alien1", "explosion5"]
        self.__alien = Actor(self.__images[0], (self.__x, self.__y))
        self.__alien.status = 1  # draw => visible
        self.__alien.type = 0

    def __del__(self):
        return

    def getActor(self):
        return self.__alien

    def getStatus(self):
        return self.__alien.status

    def update(self, move_sequence, level):
        movex = movey = 0
        if self.__alien.type == 0:
            if move_sequence < 10 or move_sequence > 30:
                movex = -15
            if move_sequence == 10 or move_sequence == 30:
                movey = 50 + (3 * level)
            if 10 < move_sequence < 30:
                movex = 15
            animate(self.__alien, pos=(self.__alien.x + movex, self.__alien.y + movey), duration=0.5, tween='linear')
            if randint(0, 1) == 0:
                self.__alien.image = "alien1"
            else:
                self.__alien.image = "alien1b"
        else:
            movey = 10 * level
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
            elif self.__alien.y > 670:
                self.__alien.y = 10
            animate(self.__alien, pos=(self.__alien.x + movex, self.__alien.y + movey), duration=0.5, tween='linear')
            if randint(0, 1) == 0:
                self.__alien.image = "alien1"
            else:
                self.__alien.image = "alien1b"

    @property
    def images(self):
        return self.__images

    # def updateAliens(self):
    #     global builder, ship, move_sequence, LEVEL, DIFFICULTY
    #     for element in builder.aliensList:
    #         if randint(0, DIFFICULTY) == 0:
    #             if element == builder.aliensList[-1]:
    #                 element.getActor().type = 1
    #         element.update(move_sequence, LEVEL)
    #         if element.getActor().type == 0 and randint(0, DIFFICULTY) == 0:
    #             builder.laser(element.getActor().x, element.getActor().y)
    #         if element.getActor().type == 1 and randint(0, 2) == 0:
    #             builder.laser(element.getActor().x, element.getActor().y)
    #         if element.getActor().y > 620 and ship.getStatus() == 1 and element.getActor().type == 0:
    #             ship.getActor().status += 1
    #             sounds.shipexplosion.play()
    #         self.checkAlienHitPlayer(element)
    #     move_sequence += 1
    #     if move_sequence == 40:
    #         move_sequence = 0
    #
    # def checkAlienHitPlayer(self, alien):
    #     if ship.getActor().collidepoint(alien.getActor().x, alien.getActor().y):
    #         sounds.shipexplosion.play()
    #         ship.getActor().status += 1
    #         alien.getActor().image = alien.images[1]
