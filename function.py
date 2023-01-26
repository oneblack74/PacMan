import pygame as pg


def creerMap():
    fichier = open("map.txt", "r")
    f = fichier.read()
    map = []
    for i in range(33):
        map.append([])
        for j in range(30):
            map[i].append(f[j + i * 30 + i])

    fichier.close()
    return map




def coordPossible(x, y):
    """x = hauteur, y = largeur"""
    if 0 <= x < 31 and 0 <= y < 28:
        return True
    return False


def testDead(gx, gy, px, py, state):
    if (gx == px) and (gy == py) and (state in ["chase", "scatter"]):
        return True
    return False
