import random

import pygame as pg
import time

class Blinky:

    def __init__(self):

        self.img = {}
        for name in "DLRU":
            self.img[name+"0"] = pg.transform.scale(pg.image.load("./sprite/ghost/blinky/"+name+"/0.png").convert_alpha(), (35,35))
            self.img[name+"1"] = pg.transform.scale(pg.image.load("./sprite/ghost/blinky/"+name+"/1.png").convert_alpha(), (35,35))
            self.img[name+"eyes"] = pg.transform.scale(pg.image.load("./sprite/ghost/blinky/"+name+"/eyes.png").convert_alpha(), (35,35))
        self.img["B0"] = pg.transform.scale(pg.image.load("./sprite/ghost/blinky/B0.png").convert_alpha(), (35, 35))
        self.img["B1"] = pg.transform.scale(pg.image.load("./sprite/ghost/blinky/B1.png").convert_alpha(), (35, 35))

        self.state = "scatter"
        self.frightenedTmp = False
        self.speed = 0.30

        self.eatenStart = False

        self.x = 20 * 15 -10
        self.y = 20 * 12

        self.dir = "L"
        self.coordTmp = (self.x+17)//20, (self.y+17)//20
        self.cptSprite = 0
        self.timeSprite = time.time()
        self.timer = time.time()
        self.timerFrightened = time.time()
        self.frightenedStart = False
        self.estAffiche = True

    def in_couloir(self):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if y == 15 and (x < 5 or x > 24):
            return True
        return False

    def xGet(self):
        return (self.x+17) // 20

    def yGet(self):
        return (self.y+17) // 20

    def stateGet(self):
        return self.state

    def eatenStartGet(self):
        return self.eatenStart

    def setTimer(self, t):
        self.timer = t


    def reInit(self):
        self.state = "scatter"
        self.frightenedTmp = False
        self.speed = 0.30

        self.x = 20 * 15 - 10
        self.y = 20 * 12

        self.dir = "L"
        self.coordTmp = (self.x+17) // 20, (self.y+17) // 20
        self.cptSprite = 0
        self.timeSprite = time.time()
        self.timer = time.time()
        self.timerFrightened = time.time()
        self.frightenedStart = False
        self.estAffiche = True

    def deplacement(self, map):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if x == -1:
            self.x = 28 * t
            self.y = 15 * t
            self.dir = "L"
        elif x == 29:
            self.x = 0
            self.y = 15 * t
            self.dir = "R"
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
        if self.estAffiche:
            if self.state in ["chase","scatter"]:
                surface.blit(self.img[self.dir + str(self.cptSprite)], (self.x - 8, self.y - 8))
            elif self.state == "frightened":
                surface.blit(self.img["B" + str(self.cptSprite)], (self.x - 8, self.y - 8))
            elif self.state == "eaten":
                surface.blit(self.img[self.dir + "eyes"], (self.x - 8, self.y - 8))

    def directionPossible(self, map):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        d = ""
        list = []
        match self.dir:
            case "U":
                if not self.in_couloir():
                    if map[y][x-1] not in "wd":
                        d += "L"
                        list.append((y,x-1))
                    if map[y-1][x] not in "wd":
                        d += "U"
                        list.append((y - 1, x))
                    if map[y][x+1] not in "wd":
                        d += "R"
                        list.append((y, x + 1))
            case "D":
                if not self.in_couloir():
                    if map[y+1][x] not in "wd":
                        d += "D"
                        list.append((y+1, x))
                    if map[y][x - 1] not in "wd":
                        d += "L"
                        list.append((y, x - 1))
                    if map[y][x + 1] not in "wd":
                        d += "R"
                        list.append((y, x + 1))
            case "R":
                if map[y - 1][x] not in "wd":
                    d += "U"
                    list.append((y - 1, x))
                if map[y][x + 1] not in "wd":
                    d += "R"
                    list.append((y, x + 1))
                if map[y+1][x] not in "wd":
                    d += "D"
                    list.append((y + 1, x))
            case "L":
                if map[y - 1][x] not in "wd":
                    d += "U"
                    list.append((y - 1, x))
                if map[y + 1][x] not in "wd":
                    d += "D"
                    list.append((y + 1, x))
                if map[y][x - 1] not in "wd":
                    d += "L"
                list.append((y, x - 1))
        return d, list

    def calculDist(self,xt, yt, x, y):
        return (y-yt)**2 + (x-xt)**2

    def choisirRotate(self, xt, yt, map):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        self.coordTmp = x, y
        if self.in_couloir():
            tmp = (self.dir, [(x,y)])
        else:
            tmp = self.directionPossible(map)
        if self.state == "frightened":
            res = random.choice(tmp[0])
            return res

        list = []
        for a in range(len(tmp[0])):
            list.append((tmp[0][a],(self.calculDist(xt, yt, tmp[1][a][1],tmp[1][a][0]))))


        min = list[0][1],list[0][0]
        for b in range(1,len(list)):
            if list[b][1] < min[0]:
                min = list[b][1],list[b][0]


        return min[1]


    def rotate(self, xt, yt, map):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if ((x != self.coordTmp[0]) or (y != self.coordTmp[1])):
            dir = self.choisirRotate(xt, yt, map)
            match dir:
                case "U":
                    self.dir = "U"
                case "D":
                    self.dir = "D"
                case "R":
                    self.dir = "R"
                case "L":
                    self.dir = "L"



    def updateSprite(self):
        if time.time() - self.timeSprite >= 0.2:
            if self.cptSprite == 1:
                self.cptSprite = 0
            else:
                self.cptSprite += 1
            self.timeSprite = time.time()


    def principal(self, xt, yt, map):
        self.updateSprite()

        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if int(self.x) % t == 0 and int(self.y) % t == 0:
            if self.dir == "U":
                if map[y-1][x] == "w" or map[y][x-1] != "w" or map[y][x+1] != "w":
                    self.rotate(xt, yt, map)
            elif self.dir == "D":
                if map[y + 1][x] == "w" or map[y][x-1] != "w" or map[y][x+1] != "w":
                    self.rotate(xt, yt, map)
            elif self.dir == "R":
                if map[y][x+1] == "w" or map[y-1][x] != "w" or map[y+1][x] != "w":
                    self.rotate(xt, yt, map)
            elif self.dir == "L":
                if map[y][x-1] == "w" or map[y-1][x] != "w" or map[y+1][x] != "w":
                    self.rotate(xt, yt, map)


        self.deplacement(map)

    def inverseDir(self):
        match self.dir:
            case "U":
                self.dir = "D"
            case "D":
                self.dir = "U"
            case "R":
                self.dir = "L"
            case "L":
                self.dir = "R"

    def eaten(self, xt, yt):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if xt == x and yt == y and self.state == "frightened":
            return True
        return False


    def arriver(self):
        t = 20
        x = round(self.x+17) // t
        y = round(self.y+17) // t
        if x == 14 and y == 12:
            return True
        return False

    def run(self,xt, yt, map,start, run):
        t = 20
        x = round(self.x + 17) // t
        y = round(self.y + 17) // t
        if int(self.x) % t == 0 and int(self.y) % t == 0 and self.frightenedTmp == True:
            self.state = "frightened"
            self.frightenedTmp = False
            self.inverseDir()
            self.speed = 0.20
            self.frihtenedStart = True
            self.state = "frightened"
            self.coordTmp = (self.x + 17) // 20, (self.y + 17) // 20
            self.timer = time.time()

        if run:
            if self.eaten(xt, yt):
                self.eatenStart = True
                self.state = "eaten"
                self.speed = 0.40
            else:
                if self.eatenStart:
                    self.eatenStart = False

            if start:
                self.frightenedTmp = True
            elif self.state == "frightened" and time.time() - self.timer >= 5:
                self.speed = 0.30
                self.state = "scatter"
                self.timer = time.time()
            elif self.state == "scatter" and time.time() - self.timer >= 2:
                self.state = "chase"

            if self.state == "scatter":
                self.principal(26,-3,map)
            elif self.state == "chase":
                self.principal(xt, yt, map)
            elif self.state == "frightened":
                self.principal(0,0,map)
            elif self.state == "eaten":
                if self.arriver():
                    self.state = "chase"
                    self.speed = 0.30
                else:
                    self.principal(14,12,map)
        else:
            if time.time() - self.timer >= 3:
                self.estAffiche = False

        if self.frightenedTmp == True:
            self.state = "frightened"






