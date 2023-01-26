import pygame as pg

class Menu1:

    def __init__(self, surface):
        self.surface = surface

        self.img = pg.transform.scale(pg.image.load("./sprite/menu/name.png").convert_alpha(), (280*1.5,64*1.5))

        self.ind = 0
        self.key_UP = False
        self.key_DOWN = False

        self.state = True

    def indGet(self):
        return self.ind

    def indSet(self, ind):
        self.ind = ind

    def stateGet(self):
        return self.state

    def stateSet(self, bool):
        self.state = bool

    def draw(self):
        t = 20
        self.surface.fill("black")
        self.surface.blit(pg.font.Font(None, 50).render("Play", True, "white"), (t*12, t*20))
        self.surface.blit(pg.font.Font(None, 50).render("Highscore", True, "white"), (t*12, t*22))

        self.surface.blit(self.img, (90,100))

        pg.draw.polygon(self.surface, "white", ((t*10,t*20.3+2*t*self.ind),(t*10,t*21.3+2*t*self.ind), (t*11,t*20.8+2*t*self.ind)))


    def updateInd(self):
        if self.ind == 0:
            self.ind = 1
        else:
            self.ind = 0

    def run(self):

        if self.state:
            keys = pg.key.get_pressed()

            if keys[pg.K_UP] and not self.key_UP:
                self.updateInd()
                self.key_UP = True
            elif not keys[pg.K_UP] and self.key_UP:
                self.key_UP = False

            if keys[pg.K_DOWN] and not self.key_DOWN:
                self.updateInd()
                self.key_DOWN = True
            elif not keys[pg.K_DOWN] and self.key_DOWN:
                self.key_DOWN = False

            if keys[pg.K_RETURN]:
                self.state = False



class Menu2:

    def __init__(self, surface):

        self.surface = surface
        self.state = True

        self.scores = []
        self.lireScores()
        self.lettre = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.indL = 0
        self.indPosL = 0
        self.stateWrite = False
        self.scoreActuel = [0,0]
        self.name = ["_","_","_"]

        self.key_UP = False
        self.key_DOWN = False
        self.key_RETURN = False

    def stateGet(self):
        return self.state

    def updateInd(self, sens):
        if sens == "P":
            self.indL += 1
        elif sens == "M":
            self.indL -= 1

        if self.indL == -1:
            self.indL = len(self.lettre)-1
        elif self.indL == len(self.lettre):
            self.indL = 0

    def updateScore(self):
        list = []
        i = 0
        max = 9
        while len(list) < max:
            if self.scores[i][2] >= self.scoreActuel[1]:
                list.append(self.scores[i])
                i+=1
            else:
                res = "".join(self.name)
                list.append([res, self.scoreActuel[0], self.scoreActuel[1]])
                self.scoreActuel = [0,0]
                max -= 1
        self.scores = list[:]

    def stateWriteSet(self, bool):
        self.stateWrite = bool

    def scoresGet(self):
        return self.scores

    def scoreActuelSet(self, lvl, score):
        self.scoreActuel = [lvl, score]

    def active(self):
        self.state = True

    def ecrireScores(self):
        tmp = ""
        for i in range(8):
            tmp += self.scores[i][0] + "#"
            tmp += str(self.scores[i][1])
            tmp += "/" + str(self.scores[i][2]) + "$"
        tmp += "@"


        fichier = open("./saves/scores.txt", "w")
        fichier.write(tmp)
        fichier.close()

    def lireScores(self):
        fichier = open("./saves/scores.txt", "r")
        f = fichier.read()
        i = 0
        res = []
        tmp = ''
        while f[i] != '@':
            if f[i] == '#':
                res.append(tmp)
                tmp = ''
            elif f[i] == '/':
                res.append(int(tmp))
                tmp = ''
            elif f[i] == '$':
                res.append(int(tmp))
                self.scores.append(res[:])
                res = []
                tmp = ''
            else:
                tmp += f[i]
            i+=1

        fichier.close()


        fichier.close()

    def updateName(self):
        self.name[self.indPosL] = self.lettre[self.indL]

    def draw(self):
        t = 20
        self.surface.fill("black")
        self.surface.blit(pg.font.Font(None, 50).render("HIGHSCORE", True, "white"), (t * 10, t * 3))
        i = 0
        while (i < 7) and (self.scores[i][1] != 0):
            tmp_lvl = str(self.scores[i][1])
            while len(tmp_lvl) < 3:
                tmp_lvl = "_"+tmp_lvl

            tmp_score = str(self.scores[i][2])
            while len(tmp_score) < 7:
                tmp_score = "_" + tmp_score

            tmp = "- "+self.scores[i][0]+" | LVL " + tmp_lvl + " | " + tmp_score + " pts"
            self.surface.blit(pg.font.Font(None, 30).render(tmp, True, "white"), (t * 8, t * 10 + i * 2 *t))
            i+=1
        if i < 7:
            for j in range(i,8):
                tmp = "- ___ | LVL ___ | _______ pts"
                self.surface.blit(pg.font.Font(None, 30).render(tmp, True, "white"), (t * 8, t * 10 + j * 2 * t))

        if self.stateWrite:
            tmp_lvl = str(self.scoreActuel[0])
            while len(tmp_lvl) < 3:
                tmp_lvl = "_" + tmp_lvl

            tmp_score = str(self.scoreActuel[1])
            while len(tmp_score) < 7:
                tmp_score = "_" + tmp_score

            tmp = "- " + self.name[0]+self.name[1]+self.name[2]+ " | LVL " + tmp_lvl + " | " + tmp_score + " pts"
            self.surface.blit(pg.font.Font(None, 30).render(tmp, True, "white"), (t * 8, t * 30))


    def run(self):

        if self.state:
            if not self.stateWrite:
                keys = pg.key.get_pressed()

                if keys[pg.K_ESCAPE]:
                    self.state = False

            else:
                keys = pg.key.get_pressed()

                if keys[pg.K_UP] and not self.key_UP:
                    self.updateInd("P")
                    self.key_UP = True
                elif not keys[pg.K_UP] and self.key_UP:
                    self.key_UP = False

                if keys[pg.K_DOWN] and not self.key_DOWN:
                    self.updateInd("M")
                    self.key_DOWN = True
                elif not keys[pg.K_DOWN] and self.key_DOWN:
                    self.key_DOWN = False

                self.updateName()

                if keys[pg.K_RETURN] and not self.key_RETURN:
                    self.key_RETURN = True
                    self.indL = 0
                    self.indPosL += 1
                    if self.indPosL == 3:
                        self.stateWrite = False
                        self.indPosL = 0
                        self.updateScore()
                        self.ecrireScores()
                elif not keys[pg.K_RETURN] and self.key_RETURN:
                    self.key_RETURN = False





