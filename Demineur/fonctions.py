"""
Fonctions :
    create_board() : Crée la grille avec NB_MINES placées aléatoirement
    ajouter_drapeau(grille, row, column) : Ajoute un drapeau à la case souhaitée
    enlever_drapeau(grille, row, column) : Enlève un drapeau à la case souhaitée
    reveler_case(grille, row, column) : Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour
    gagne(compteur) : Condition de victoire
"""

from random import randint

SIZE_X = 30 # nombre de colonnes
SIZE_Y = 20 # nombre de lignes
NB_MINES = 100 # nombre de mines

def create_board():
    """ Crée la grille avec NB_MINES mines placées aléatoirement

    Returns
    -------
    list[list[int]]
        La grille remplie de 0 (case vide) et de 1 (bombe)
    """
    mines_count = 0 # compteur de mines 
    tiles = [[0 for i in range (SIZE_X)] for j in range (SIZE_Y)] # remplit la grille de [0]
    while mines_count < NB_MINES:
        randx = randint(0,SIZE_X-1) # colonne aléatoire
        randy = randint(0,SIZE_Y-1) # ligne aléatoire
        if tiles[randy][randx] == 0:
            tiles[randy][randx] = 1
            mines_count += 1
    return tiles

def ajouter_drapeau(grille, row, column):
    """ Ajoute un drapeau à la case souhaitée"""
    grille[row][column] = "d" + str(grille[row][column]) 
    return grille

def enlever_drapeau(grille, row, column):
    """ Enlève un drapeau à la case souhaitée """
    grille[row][column] = grille[row][column][-1]
    if grille[row][column] != "*" :
        grille[row][column] = int(grille[row][column]) 
    return grille

def reveler_case(grille, row, column):
    """Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour"""
    if grille[row][column] == "*" :
        return "Mine" 
    elif type(grille[row][column]) == str and grille[row][column][0] == "d":
        return "Drapeau"
    else :
        return grille[row][column] 

def gagne(compteur):
    """Condition de victoire"""
    if compteur[0] == SIZE_X * SIZE_Y - NB_MINES :
        return True

        