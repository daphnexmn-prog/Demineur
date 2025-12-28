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

def compter_mines(tiles, row, column):
    """ Compte le nombre de mines autour de chaque case et determine si la case est deja une mine

    Returns
    -------
    list[list[int ou str]]
        La grille remplie de * (bombe) ou de int (case vide)
    """
    for i in range (row):
        for j in range (column):
            if tiles[row][column]==1:   #vérifie si la case est une mine
                return "*"
            else :
                mine_case=0
                for x in range (-1,2):  #parcourt les cases voisines
                    for y in range (-1,2):
                        new_col = column + x
                        new_row = row + y
                        if 0 <= new_col < SIZE_X and 0 <= new_row < SIZE_Y:   #vérifie que les cases voisines ne sont pas out of range
                            if tiles[new_row][new_col] == 1: 
                                mine_case += 1  #compte le nombre de mines autour de la case
                return mine_case

def grille_nombres(tiles,row,column):
    """ Crée une grille comportant pour chaque case la valeur de la fonction compter_mines

    Returns
    -------
    str(*) si la case est une mine
    int(mine_case) le nombre de mines autour d'une case n'étant pas une mine
    """
    grille=[[compter_mines(tiles,row,column) for column in range(SIZE_X)] for row in range(SIZE_Y)]  #créé la grille en utilisant la fonction compter_mines
    return grille

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
        return grille[row][column] # le nombre de mines autour

def gagne(compteur):
    """Condition de victoire"""
    if compteur[0] == SIZE_X * SIZE_Y - NB_MINES :
        return True

        