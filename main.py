import math
import pgzrun
from pygame import font

from Builder import Builder
from Player import Player

WIDTH = 1000
HEIGHT = 700
move_delay = 30
move_counter = counterTime = counter = 0
game = Builder.createGame()
playername = ""
game.readhighscores("")
game.writehighscores()


def initCommon():
    global builder
    builder = Builder()
    builder.removeAliens()
    builder.removeLasers()
    for i in range(18):
        builder.alien(i)


def startGame():
    global game
    Player.life = 3
    game.level += 1
    if 5 < game.difficulty:
        game.difficulty -= 3
    initCommon()


def continueGame():
    initCommon()


def endGame(text):
    global game
    displayMessage(text)
    if keyboard.ESCAPE:
        game.readhighscores(playername)
        game.writehighscores()
        game.gamestate = 0
        game.level = 0
        game.difficulty = 30
        game.score = 0


def newLevel(text):
    displayMessage(text)


def scoreUpdate():
    screen.draw.text(str(game.score), topright=(980, 10),
                     owidth=0.5, ocolor=(255, 255, 255),
                     color=(0, 64, 255),
                     fontsize=60)


def displayMessage(text, x=500, y=300, f=50, color=(255, 64, 0)):
    screen.draw.text(text,
                     center=(x, y), owidth=0.5,
                     ocolor=(255, 255, 255),
                     color=color, fontsize=f)


def drawScore():
    game.drawscore = True
    screen.draw.text("+200", center=(game.coord[0], game.coord[1]), owidth=0.5,
                     ocolor=(255, 255, 255),
                     color=(255, 64, 0), fontsize=30)


def drawLife():
    for i in range(Player.lives()):
        screen.blit('life', (10 + i*40, 10))


def drawShieldRemaining():
    counter = builder.shield.counter
    if counter == -1:
        counter = 0
    text = "shield: " + str(counter)
    screen.draw.text(text, center=(950, 680), owidth=0.5,
                     ocolor=(0, 0, 0),
                     color=(255, 255, 255), fontsize=20)


def drawHighScores():
    ord = 0
    counterline = 0
    displayMessage("the five Highest Scores: \n", 500, 400, 40, (0, 0, 255))
    for line in game.scoreList:
        if counterline <= 5:
            displayMessage(line, 500, 430 + ord, 30, (0, 0, 255))
            ord += 30
            counterline += 1
    displayMessage("Press Return to play \n", 500, 650, 50, (0, 0, 0))

#  pygame thread ###############################################
#
#


def draw():
    global counterTime
    screen.blit('background', (0, 0))
    screen.clear()
    checkDrawScore()
    drawLife()
    drawShieldRemaining()
    if game.gamestate == 0:
        #music.play('spaceinvader')
        displayMessage("SPACE INVADERS\nkeys: \nPress SPACE to fire\nPress Shift Left "
                       "\n for the Shield (3 times per level)\n"
                       "Press Arrow <- and -> to move\nPress Enter to play\n"
                       "Enter your name: ", 500, 150, 40)
        displayMessage(playername, 500, 300, 40)
        drawHighScores()
        if keyboard.RETURN:
            game.gamestate = 1
    else:
        builder.ship.getActor().image = builder.ship.images[math.floor(builder.ship.getStatus() / 6)]
        builder.ship.getActor().draw()
        draw_aliens()
        draw_lasers()
        if keyboard.K_LSHIFT and builder.shield.getStatus() == 1 and builder.shield.counterTime < 100:
            builder.shield.counterTime += 1
            builder.shield.getActor().draw()
        scoreUpdate()
        if builder.ship.getStatus() >= 30:
            if Player.lives() >= 0:
                Player.lifeupdate()
            if Player.lives() < 1:
                screen.clear()
                #drawHighScores()
                endGame("GAME OVER\n Nice Play ! \n Press Escape to play again \n")
            else:
                continueGame()
        if not builder.aliensList.list:
            newLevel("YOU WON!,\n press Enter for the next level: "+str(game.level+1))


def update():
    global move_counter, move_delay
    if game.gamestate == 1:
        if builder.ship.getStatus() < 30 and builder.aliensList.list:  # 30 iteration pour avoir un delai d'affichage lent
            verifyKeys()
            builder.updateLasers()
            move_counter += 1
            if move_counter == move_delay:
                move_counter = 0
                builder.updateAliens()
            if builder.ship.getStatus() > 1:
                builder.ship.getActor().status += 1
        else:
            if keyboard.RETURN:
                startGame()


#
#
#  end of pygame thread ##########################################


def verifyKeys():
    builder.ship.update()
    builder.shield.update(builder.ship.getActor().x, builder.ship.getActor().y)
    if keyboard.space and builder.ship.laserActive == 1:
        sounds.shoot.play()
        builder.ship.laserActive = 0
        builder.laserPlayer.coordInit(builder.ship.getActor().x, (builder.ship.getActor().y - 32))
        builder.laserPlayer.getActor().status = 1


def on_key_down(key):
    global playername
    if game.gamestate == 0:
        if key != keys.RETURN:
            playername += key.name
            print("name = " + playername)
            if key == keys.BACKSPACE:
                playername = ""
    else:
        if key == keys.LSHIFT:
            builder.shield.counter -= 1
            builder.shield.counterTime = 0


def on_key_up(key):
    if key == keys.LSHIFT:
        builder.shield.getActor().status = 0
        builder.shield.counterTime = 0


def checkDrawScore():
    global counter
    if game.drawscore and counter < 10:
        drawScore()
        counter += 1
    if counter == 10:
        game.drawscore = False
        counter = 0
        game.coord = []


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
    if builder.laserPlayer.getStatus() == 1:
        builder.laserPlayer.getActor().draw()


startGame()

pgzrun.go()

