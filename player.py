import pygame as pg
import time, function
from constante import *

class Player:
    def __init__(self):
        self.img = {}
        for name in "DLUR":
            self.img[name+"0"] = pg.transform.scale(pg.image.load("./sprite/player/"+name+"/P00.png").convert_alpha(),(25,25))
            self.img[name+"1"] = pg.transform.scale(pg.image.load("./sprite/player/"+name+"/P01.png").convert_alpha(),(25,25))

        self.life = 3
        self.dir = "R"
        self.dirTmp = "R"
        self.cptSprite = 0
        self.timeSprite = time.time()
        self.x = 20*15 -10
        self.y = 20*24
        self.tmpx = 20*15

        self.power = False
        self.timer = time.time()
        self.powerStart = False

        self.death = False
        self.estAffiche = True
        self.speed = 0.30
        self.point = 0
        self.cptPBoule = 0
        self.cptGBoule = 0

        self.lvl = 1

    def in_couloir(self):
        t = 20
        x = round(self.x+12) // t
        y = round(self.y+12) // t
        if y == 15 and (x < 6 or x > 23):
            self.dirTmp = self.dir
            return True
        return False

    def lifeGet(self):
        return self.life

    def estAfficheSet(self, bool):
        self.estAffiche = bool

    def lvlGet(self):
        return self.lvl

    def pBouleGet(self):
        return self.cptPBoule

    def gBouleGet(self):
        return self.cptGBoule

    def xGet(self):
        return (self.x+12)//20

    def yGet(self):
        return (self.y+12)//20

    def powerGet(self):
        return self.power

    def pointGet(self):
        return self.point

    def dirGet(self):
        return self.dir

    def imgUiGet(self):
        return self.img["L1"]

    def powerStartGet(self):
        return self.powerStart

    def dirSet(self, dir):
        self.dir = dir
        self.dirTmp = dir



    def perdreVie(self):
        self.life -= 1

    def passer_lvl_suiv(self):
        self.reInit()
        self.cptPBoule = 0
        self.cptGBoule = 0
        self.lvl += 1

    def respawn(self):
        self.life = 3
        self.point = 0
        self.cptPBoule = 0
        self.cptGBoule = 0
        self.lvl = 1
        self.reInit()

    def mangerGhost(self):
        self.point += ghost_1

    def reInit(self):
        self.dir = "R"
        self.dirTmp = "R"
        self.cptSprite = 0
        self.timeSprite = time.time()
        # 15 18
        self.x = 20 * 15 - 10
        self.y = 20 * 24
        self.tmpx = 20 * 15

        self.power = False
        self.timer = time.time()
        self.powerStart = False

        self.death = False
        self.estAffiche = True


    def updateSprite(self):
        if time.time() - self.timeSprite >= 0.3:
            if self.cptSprite == 1:
                self.cptSprite = 0
            else:
                self.cptSprite += 1
            self.timeSprite = time.time()


    def controls(self):
        keys = pg.key.get_pressed()

        if not self.in_couloir():
            if keys[pg.K_UP]:
                self.dirTmp = "U"
            if keys[pg.K_DOWN]:
                self.dirTmp = "D"
        if keys[pg.K_RIGHT]:
            self.dirTmp = "R"
        if keys[pg.K_LEFT]:
            self.dirTmp = "L"


    def verifRotate(self, map):
        t = 20
        x = round(self.x+12) // t
        y = round(self.y+12) // t
        if int(self.x) % t == 0 and int(self.y) % t == 0:
            match self.dirTmp:
                case "U":
                    if map[y-1][x] != "w":
                        self.dir = self.dirTmp
                case "D":
                    if map[y + 1][x] != "w":
                        self.dir = self.dirTmp
                case "R":
                    if map[y][x+1] != "w":
                        self.dir = self.dirTmp
                case "L":
                    if map[y][x-1] != "w":
                        self.dir = self.dirTmp


    def verifDeplacement(self, map):
        t = 20
        x = round(self.x+12) // t
        y = round(self.y+12) // t
        if int(self.x) % t == 0 and int(self.y) % t == 0:
            match self.dir:
                case "U":
                    if map[y-1][x] in "wd":
                        return False
                case "D":
                    if map[y + 1][x] in "wd":
                        return False
                case "R":
                    if map[y][x+1] in "wd":
                        return False
                case "L":
                    if map[y][x-1] in "wd":
                        return False
        return True


    def deplacement(self):
        t = 20
        x = round(self.x+12) // t
        y = round(self.y+12) // t
        if x == -1:
            self.x = 28*t
            self.y = 15*t
            self.dir = "L"
            self.dirTmp = "L"
        elif x == 29:
            self.x = 0
            self.y = 15 * t
            self.dir = "R"
            self.dirTmp = "R"
        else:
            match self.dir:
                case "U":
                    self.y -= self.speed
                case "D":
                    self.y += self.speed
                case "R":
                    self.x += self.speed
                case "L":
                    self.x -= self.speed

    def draw(self, surface):
        surface.blit(self.img[self.dir+str(self.cptSprite)], (self.x-2, self.y-2))

    def eat(self, map):
        t = 20
        x = round(self.x+12) // t
        y = round(self.y+12) // t
        if map[y][x] == ".":
            self.cptPBoule += 1
            self.point += pac_dot
            map[y][x] = "*"
        elif map[y][x] == "o":
            self.cptGBoule += 1
            self.point += power_pellet
            self.powerStart = True
            self.power = True
            self.timer = time.time()
            map[y][x] = "*"
        else:
            self.powerStart = False

    def run(self, map, run):
        if run:
            self.verifRotate(map)
            self.updateSprite()
            if self.verifDeplacement(map):
                self.deplacement()
                self.eat(map)
            if self.power == True:
                if time.time() - self.timer >= 5:
                    self.power = False
        else:
            if time.time() - self.timer >= 4:
                self.estAffiche = False

