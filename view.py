import sys, math, time
from function import *
import menu
import player
import blinky
import pygame as pg


class View:

    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((600,680))

        pg.display.set_caption("PAC MAN")
        self.surface = pg.display.get_surface()
        pg.display.set_icon(pg.image.load("./sprite/PAC-MAN-logo.webp"))

        self.m1 = menu.Menu1(self.surface)
        self.m2 = menu.Menu2(self.surface)
        self.map = creerMap()
        self.p = player.Player()
        self.blinky = blinky.Blinky()
        self.timer = 0
        self.timeSprite = 0
        self.cptSprite = 0
        self.nbGame = 1

        self.start = False

        self.run = True
        self.win = False

        self.font = pg.font.SysFont(None, 24)
        self.score = 0


    def updateSprite(self):
        if time.time() - self.timeSprite >= 0.2:
            if self.cptSprite == 1:
                self.cptSprite = 0
            else:
                self.cptSprite += 1
            self.timeSprite = time.time()

    def draw(self):
        t = 20
        self.window.fill("black")

        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "d":
                    pg.draw.line(self.surface, "white", (j * t, i * t + t//2), (j * t + t, i * t + t//2), 3)
                elif self.map[i][j] == "w":

                    # V
                    if self.map[i+1][j] == "w" and self.map[i-1][j] == "w":
                        pg.draw.line(self.surface, "blue", (j*t+t//2, i*t),(j*t+t//2, i*t+t-1),3)


                    # H
                    elif (self.map[i][j+1] == "w" and self.map[i][j-1] == "w") or (self.map[i][j+1] == "d" and self.map[i][j-1] == "w") or (self.map[i][j+1] == "w" and self.map[i][j-1] == "d"):
                        pg.draw.line(self.surface, "blue", (j * t, i * t + t // 2), (j * t + t, i * t + t // 2), 3)

                    # LD =====
                    # inter
                    if self.map[i][j-1] == "w" and self.map[i+1][j] == "w" and self.map[i+1][j-1] != "w":
                        pg.draw.rect(self.surface, "black", (j*t,i*t,t,t))
                        pg.draw.arc(self.surface, "blue", (j*t-t//2,i*t+t//2,t,t),0,math.pi/2,3)

                    # exter
                    elif self.map[i][j-1] == "w" and self.map[i+1][j] == "w" and self.map[i-1][j+1] != "w" and self.map[i][j+1] != "w" and self.map[i-1][j] != "w":
                        pg.draw.rect(self.surface, "black", (j*t,i*t,t,t))
                        pg.draw.arc(self.surface, "blue", (j*t-t//2,i*t+t//2,t,t),0,math.pi/2,3)

                    # LU =====
                    # inter
                    elif self.map[i][j - 1] == "w" and self.map[i - 1][j] == "w" and self.map[i-1][j - 1] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j*t-t//2,i*t-t//2,t,t),3*math.pi/2,0,3)

                    # exter
                    elif self.map[i][j - 1] == "w" and self.map[i - 1][j] == "w" and self.map[i+1][j+1] != "w" and self.map[i][j+1] != "w" and self.map[i+1][j] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j * t - t // 2, i * t - t // 2, t, t), 3 * math.pi / 2, 0, 3)

                    # RD =====
                    # inter
                    elif self.map[i][j + 1] == "w" and self.map[i + 1][j] == "w" and self.map[i+1][j+1] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j*t+t//2,i*t+t//2,t,t),math.pi/2,math.pi,3)

                    # exter
                    elif self.map[i][j + 1] == "w" and self.map[i + 1][j] == "w" and self.map[i-1][j-1] != "w" and self.map[i][j-1] != "w" and self.map[i-1][j] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j * t + t // 2, i * t + t // 2, t, t), math.pi / 2, math.pi,3)

                    # RU =====
                    # inter
                    elif self.map[i][j + 1] == "w" and self.map[i - 1][j] == "w" and self.map[i-1][j+1] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j*t+t//2,i*t-t//2,t,t),math.pi,3*math.pi/2,3)

                    # exter
                    elif self.map[i][j + 1] == "w" and self.map[i - 1][j] == "w" and self.map[i+1][j-1] != "w" and self.map[i][j-1] != "w" and self.map[i+1][j] != "w":
                        pg.draw.rect(self.surface, "black", (j * t, i * t, t, t))
                        pg.draw.arc(self.surface, "blue", (j * t + t // 2, i * t - t // 2, t, t), math.pi,3 * math.pi / 2, 3)
                elif self.map[i][j] == ".":
                    pg.draw.circle(self.surface, "yellow", (j*t+t//2, i*t+t//2),2)
                elif self.map[i][j] == "o":
                    if self.cptSprite == 0:
                        pg.draw.circle(self.surface, "white", (j*t+t//2, i*t+t//2),8)
                    elif self.cptSprite == 1:
                        pg.draw.circle(self.surface, "white", (j * t + t // 2, i * t + t // 2), 4)
        pg.draw.line(self.surface, "blue", (1 * t, 14 * t + t // 2), (1 * t + t, 14 * t + t // 2), 3)
        pg.draw.line(self.surface, "blue", (1 * t, 16 * t + t // 2), (1 * t + t, 16 * t + t // 2), 3)
        pg.draw.line(self.surface, "blue", (28 * t, 14 * t + t // 2), (28 * t + t, 14 * t + t // 2), 3)
        pg.draw.line(self.surface, "blue", (28 * t, 16 * t + t // 2), (28 * t + t, 16 * t + t // 2), 3)



    def drawUi(self):
        t = 20
        pg.draw.rect(self.surface, "black", (0, 13*t, 2 * t - t // 2 -1, 5 * t))
        pg.draw.rect(self.surface, "black", (29*t-6, 13*t, 2 * t, 5 * t))
        life = self.p.lifeGet()
        if life != 0:
            for i in range(life):
                self.surface.blit(self.p.imgUiGet(), (5*t-i*t, 32*t))
        self.score = self.font.render(str(self.p.pointGet()), True, "white")
        self.surface.blit(self.score, (2*t, t//2))
        self.surface.blit(self.font.render(("lvl "+str(self.p.lvlGet())), True, "white"), ((14*t, t//2)))

    def mainLoop(self):
        while True:
            self.updateSprite()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.m2.ecrireScores()
                    pg.quit()
                    sys.exit()

            if self.m1.stateGet():
                self.m1.run()
                self.m1.draw()
            else:
                if self.m1.indGet() == 0:
                    if self.start:
                        if self.run and testDead(self.blinky.xGet(), self.blinky.yGet(), self.p.xGet(), self.p.yGet(), self.blinky.stateGet()):
                            self.run = False
                            self.timer = time.time()
                        elif self.run and self.p.pBouleGet() == 240 and self.p.gBouleGet() == 4:
                            self.run = False
                            self.win = True
                            self.timer = time.time()


                        if not self.run and (time.time() - self.timer >= 3):
                            if self.win:
                                self.map = creerMap()[:]
                                self.p.passer_lvl_suiv()
                                self.start = False
                                self.blinky.reInit()
                                self.run = True
                                self.win = False

                            else:
                                if self.p.lifeGet() >= 1:
                                    self.p.perdreVie()
                                    self.start = False
                                    self.blinky.reInit()
                                    self.p.reInit()
                                    self.run = True
                                else:
                                    res = "game "+str(self.nbGame)+": "+str(self.p.pointGet())+" pts"
                                    print(res)
                                    self.m2.updateScore(self.p.lvlGet(), self.p.pointGet())
                                    self.nbGame += 1
                                    self.map = creerMap()[:]
                                    self.blinky.reInit()
                                    self.p.respawn()
                                    self.start = False
                                    self.run = True
                                    self.p.estAfficheSet(False)
                                    self.m1.active()

                        if self.blinky.eatenStartGet():
                            self.p.mangerGhost()

                        self.p.controls()
                        self.p.run(self.map, self.run)
                        self.blinky.run(self.p.xGet(), self.p.yGet(), self.map, self.p.powerStartGet(), self.run)
                    else:
                        keys = pg.key.get_pressed()

                        if keys[pg.K_RIGHT]:
                            self.p.dirSet("R")
                            self.start = True
                        if keys[pg.K_LEFT]:
                            self.p.dirSet("L")
                            self.start = True

                    self.draw()
                    self.p.draw(self.surface)
                    self.blinky.draw(self.surface)
                    self.drawUi()

                elif self.m1.indGet() == 1:
                    self.m2.active()
                    self.m2.run()

                    if not self.m2.stateGet():
                        self.m1.active()

                    self.m2.draw()


            pg.display.update()