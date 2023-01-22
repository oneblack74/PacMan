import pygame as pg

class Menu1:

    def __init__(self, surface):
        self.surface = surface

        self.ind = 0
        self.key_UP = False
        self.key_DOWN = False

        self.state = True

    def indGet(self):
        return self.ind

    def stateGet(self):
        return self.state

    def active(self):
        self.state = True

    def draw(self):
        t = 20
        self.surface.fill("black")
        self.surface.blit(pg.font.Font(None, 50).render("Play", True, "white"), (t*12, t*20))
        self.surface.blit(pg.font.Font(None, 50).render("Highscore", True, "white"), (t*12, t*22))

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

    def stateGet(self):
        return self.state

    def updateScore(self, lvl, score):
        list = []
        i = 0
        max = 9
        while len(list) < max:
            if self.scores[i][1] >= score:
                list.append(self.scores[i])
                i+=1
            else:
                list.append([lvl, score])
                score = 0
                max -= 1
        self.scores = list[:]


    def scoresGet(self):
        return self.scores


    def active(self):
        self.state = True

    def ecrireScores(self):
        tmp = ""
        for i in range(8):
            tmp += str(self.scores[i][0])
            tmp += "/" + str(self.scores[i][1]) + "$"
        tmp += "@"


        fichier = open("./saves/scores.txt", "w")
        fichier.write(tmp)
        fichier.close()

    def lireScores(self):
        fichier = open("./saves/scores.txt", "r")
        f = fichier.read()
        i = 0
        res = []
        tmp = '0'
        while f[i] != '@':
            if f[i] == '/':
                res.append(int(tmp))
                tmp = '0'
            elif f[i] == '$':
                res.append(int(tmp))
                self.scores.append(res[:])
                res = []
                tmp = '0'
            else:
                tmp += f[i]
            i+=1

        fichier.close()


        fichier.close()


    def draw(self):
        t = 20
        self.surface.fill("black")
        self.surface.blit(pg.font.Font(None, 50).render("HIGHSCORE", True, "white"), (t * 10, t * 3))

        i = 0
        while self.scores[i][0] != 0:
            tmp = "- LVL " + str(self.scores[i][0]) + " | " + str(self.scores[i][1]) + " pts"
            self.surface.blit(pg.font.Font(None, 30).render(tmp, True, "white"), (t * 8, t * 10 + i * 2 *t))
            i+=1
        for j in range(i,9):
            tmp = "- LVL --- | ------- pts"
            self.surface.blit(pg.font.Font(None, 30).render(tmp, True, "white"), (t * 8, t * 10 + j * 2 * t))


    def run(self):

        if self.state:
            keys = pg.key.get_pressed()

            if keys[pg.K_ESCAPE]:
                self.state = False






