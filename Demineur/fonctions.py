"""
Fonctions :
    create_board() : Crée la grille avec NB_MINES placées aléatoirement
"""

import tkinter as tk
from random import randint

SIZE_X = 30 # nombre de colonnes
SIZE_Y = 20 # nombre de lignes
NB_MINES = 100 # nombre de mines

def create_board():
    """
    Crée la grille avec NB_MINES mines placées aléatoirement

    Parameters
    ----------
    None

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
    """
    Ajoute un drapeau à la case souhaitée

    Parameters
    ----------
    grille : list[list]
        La grille, chaque case étant assimilée au nombre de mines qui l'entoure 
        ou à * pour les mines
    row : int
        La rangée de la case 
    column : int
        La colonne de la case

    Returns
    -------
    list[list]
        La grille actualisée avec le drapeau sur la case concernée
    """
    grille[row][column] = "d" + str(grille[row][column]) 
    return grille

def enlever_drapeau(grille, row, column):
    """
    Enlève un drapeau à la case souhaitée

    Parameters
    ----------
    grille : list[list]
        La grille, chaque case étant assimilée au nombre de mines qui l'entoure 
        ou à * pour les mines
    row : int
        La rangée de la case 
    column : int
        La colonne de la case

    Returns
    -------
    list[list]
        La grille actualisée sans drapeau sur la case concernée
    """
    grille[row][column] = grille[row][column][-1]
    return grille
