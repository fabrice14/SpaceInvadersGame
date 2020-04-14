import pgzrun
import math
import time
import pygame.draw_py
import random
from pgzero.builtins import music
from random import randint
from Alien import Alien
from Player import Player
from LaserPlayer import LaserPlayer
from Shield import Shield
from LaserAlien import LaserAlien
from BuilderList import BuilderList
from Liste import Liste


WIDTH = 1000
HEIGHT = 700
LEVEL = 0
DIFFICULTY = 20
SCORE = 0
GameState = 0
DrawScore = False
Coord = []
Life = 2


def initCommon():
    global builder, ship, shield, laserPlayer
    builder = BuilderList()
    ship = Player(500, 650)
    shield = Shield()
    laserPlayer = LaserPlayer()
    builder.removeAliens()
    builder.removeLasers()
    for i in range(18):
        builder.alien(i)


def startGame():
    global move_delay, move_counter, move_sequence, counterTime, counter, LEVEL, DIFFICULTY
    move_counter = move_sequence = counterTime = counter = 0
    move_delay = 30
    LEVEL += 1
    if 5 != DIFFICULTY:
        DIFFICULTY -= 5
    initCommon()


def continueGame():
    global Life, ship, builder, shield, laserPlayer
    Life -= 1
    initCommon()


def endGame(text):
    global SCORE, DIFFICULTY, LEVEL, GameState
    LEVEL = 0
    DIFFICULTY = 20
    SCORE = 0
    displayMessage(text)
    if keyboard.RETURN:
        GameState = 0


def newLevel(text):
    displayMessage(text)


def scoreUpdate():
    screen.draw.text(str(SCORE), topright=(980, 10),
                     owidth=0.5, ocolor=(255, 255, 255),
                     color=(0, 64, 255),
                     fontsize=60)


def displayMessage(text):
    screen.draw.text(text,
                     center=(400, 300), owidth=0.5,
                     ocolor=(255, 255, 255),
                     color=(255, 64, 0), fontsize=60)


def drawScore():
    global DrawScore, Coord
    DrawScore = True
    screen.draw.text("+200", center=(Coord[0], Coord[1]), owidth=0.5,
                     ocolor=(255, 255, 255),
                     color=(255, 64, 0), fontsize=30)


def drawLife():
    global Life
    screen.draw.text(str(Life), center=(980, 680), owidth=0.5,
                     ocolor=(255, 255, 255),
                     color=(255, 64, 0), fontsize=30)

#  pygame thread ###############################################
#
#


def draw():
    global LEVEL, counterTime, GameState, DrawScore, counter, Coord, Life, ship
    screen.blit('background', (0, 0))
    screen.clear()
    checkDrawScore()
    drawLife()
    if GameState == 0:
        music.play('spaceinvader')
        displayMessage("SPACE INVADERS\nkeys: \nPress SPACE to fire\nPress Shift Left \n for the Shield (3 times per level)\n"
                   "Press Arrow <- and -> to move\nPress Enter to play\n")
        if keyboard.RETURN:
            GameState = 1
    else:
        ship.getActor().image = ship.images[math.floor(ship.getStatus() / 6)]
        ship.getActor().draw()
        draw_aliens()
        draw_lasers()
        if keyboard.K_LSHIFT and shield.getStatus() == 1 and counterTime < 100:
            counterTime += 1
            shield.getActor().draw()
        scoreUpdate()
        if ship.getStatus() >= 30:
            if Life < 1:
                endGame("GAME OVER\nPress Enter to play again\n")
            else:
                continueGame()
        if len(builder.aliensList.list) == 0:
            newLevel("YOU WON!,\npress return for the next level: "+str(LEVEL+1))


def update():
    global builder, move_counter, move_delay, LEVEL, DIFFICULTY, Life
    if GameState == 1:
        if ship.getStatus() < 30 and len(builder.aliensList.list) > 0:  # 30 iteration pour avoir un delai d'affichage lent
            verifyKeys()
            updateLasers()
            move_counter += 1
            if move_counter == move_delay:
                move_counter = 0
                updateAliens()
            if ship.getStatus() > 1:
                ship.getActor().status += 1
        else:
            if keyboard.RETURN:
                startGame()

#
#
#  end of pygame thread ##########################################


def updateAliens():
    global builder, move_sequence, LEVEL
    liste = builder.aliensList.list
    for element in liste:
        if randint(0, DIFFICULTY) == 0:
            if element == liste[-1]:
                element.getActor().type = 1
        element.update(move_sequence, LEVEL)
        if element.getActor().type == 0 and randint(0, DIFFICULTY) == 0:
            builder.laser(element.getActor().x, element.getActor().y)
        if element.getActor().type == 1 and randint(0, 2) == 0:
            builder.laser(element.getActor().x, element.getActor().y)
        if element.getActor().y > 620 and ship.getStatus() == 1 and element.getActor().type == 0:
            ship.getActor().status += 1
            sounds.shipexplosion.play()
        checkAlienHitPlayer(element)
    move_sequence += 1
    if move_sequence == 40:
        move_sequence = 0


def updateLasers():
    global builder, laserPlayer
    laserPlayer.update(5)
    checkLaserHitAlien()
    if laserPlayer.getActor().y < 10 and ship.laserActive == 0:
        del laserPlayer
        laserPlayer = LaserPlayer()
        ship.laserActive = 1
    for element in builder.lasersList.list:
        element.update(1 * LEVEL)
        checkLaserHitPlayer(element.getActor())
        checkLaserHitShield(element)
    builder.aliensList.list = builder.aliensList.clearListe()
    builder.lasersList.list = builder.lasersList.clearListe()


def verifyKeys():
    global laserPlayer
    ship.update()
    shield.update(ship.getActor().x, ship.getActor().y)
    if keyboard.space and ship.laserActive == 1:
        sounds.shoot.play()
        ship.laserActive = 0
        laserPlayer.coordInit(ship.getActor().x, (ship.getActor().y - 32))
        laserPlayer.getActor().status = 1


def on_key_down(key):
    if key == keys.LSHIFT:
        shield.counter += 1


def on_key_up(key):
    global counterTime
    if key == keys.LSHIFT:
        counterTime = 0


def checkDrawScore():
    global DrawScore, counter, Coord
    if DrawScore and counter < 10:
        drawScore()
        counter += 1
    if counter == 10:
        DrawScore = False
        counter = 0
        Coord = []


def draw_aliens():
    global builder
    liste = builder.aliensList.list
    for element in liste:
        if element.getStatus() == 1:
            element.getActor().draw()


def draw_lasers():
    global builder, laserPlayer
    liste = builder.lasersList.list
    for element in liste:
        element.getActor().draw()
    if laserPlayer.getStatus() == 1:
        laserPlayer.getActor().draw()


def checkLaserHitAlien():
    global builder, SCORE, laserPlayer, DrawScore, Coord
    liste = builder.aliensList.list
    for element in liste:
        if element.getActor().collidepoint((laserPlayer.getActor().x, laserPlayer.getActor().y)):
            sounds.invaderkilled.play()
            del laserPlayer
            laserPlayer = LaserPlayer()
            element.getActor().status = 0
            ship.laserActive = 1
            if element.getActor().type == 0:
                SCORE += 100
            else:
                SCORE += 200
                DrawScore = True
                Coord = [element.getActor().x, element.getActor().y]


def checkLaserHitPlayer(laser):
    if shield.getStatus() == 0:
        if ship.getActor().collidepoint(laser.x, laser.y):
            sounds.shipexplosion.play()
            ship.getActor().status += 1


def checkAlienHitPlayer(alien):
    if ship.getActor().collidepoint(alien.getActor().x, alien.getActor().y):
        sounds.shipexplosion.play()
        ship.getActor().status += 1
        alien.getActor().image = alien.images[1]


def checkLaserHitShield(laser):
    if shield.getStatus() == 1:
        if shield.getActor().collidepoint(laser.getActor().x, laser.getActor().y):
            sounds.ufo_highpitch.play()
            laser.getActor().status = 0


startGame()

pgzrun.go()

