"""
Fonctions :
    create_board() : Crée la grille avec NB_MINES placées aléatoirement
    ajouter_drapeau(grille, row, column) : Ajoute un drapeau à la case souhaitée
    enlever_drapeau(grille, row, column) : Enlève un drapeau à la case souhaitée
    reveler_case(grille, row, column) : Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour
    gagne(compteur) : Condition de victoire
"""
import tkinter as tk
from random import *

def difficulte(niveau):
    """ Renvoie le nombre de lignes, colonnes et mines en fonction du niveau choisi

    Returns
    -------
    tuple
        tuple contenant respectivement le nombre de lignes, le nombre de colonnes, le nombre de mines 
    """
    if niveau == "Débutant" :
        return (9, 9, 10)
    if niveau == "Intermédiaire":
        return (16, 16, 40)
    if niveau == "Avancé":
        return (16, 30, 99)

def create_board(tiles, size_x, size_y, nb_mines):
    """ Crée la grille avec nb_mines mines placées aléatoirement

    Parameters
    ---------
    size_x : int
        Le nombre de colonnes
    size_y : int
        Le nombre de lignes
        
    Returns
    -------
    list[list[int]]
        La grille remplie de 0 (case vide) et de 1 (bombe)
    """
    # tiles = [[0 for i in range (size_x)] for j in range (size_y)]
    mines_count = 0 # compteur de mines 
    while mines_count < nb_mines:
        randx = randint(0,size_x-1) # colonne aléatoire
        randy = randint(0,size_y-1) # ligne aléatoire
        if tiles[randy][randx] == 0:
            tiles[randy][randx] = 1
            mines_count += 1
    return tiles

def compter_mines(tiles, row, column, size_x, size_y):
    """ Compte le nombre de mines autour de chaque case et determine si la case est deja une mine

    Returns
    -------
    list[list[int ou str]]
        La grille remplie de * (bombe) ou de int (case vide)
    """
    if tiles[row][column]==1:   #vérifie si la case est une mine
        return "*"
    else :
        mine_case = 0
        for x in range (-1,2):  #parcourt les cases voisines
            for y in range (-1,2):
                new_col = column + x
                new_row = row + y
                if 0 <= new_col < size_x and 0 <= new_row < size_y:   #vérifie que les cases voisines ne sont pas out of range
                    if tiles[new_row][new_col] == 1: 
                        mine_case += 1  #compte le nombre de mines autour de la case
        return mine_case

def grille_nombres(tiles,grille, size_x, size_y):
    """ Crée une grille comportant pour chaque case la valeur de la fonction compter_mines

    Returns
    -------
    str(*) si la case est une mine
    int(mine_case) le nombre de mines autour d'une case n'étant pas une mine
    """
    for column in range (size_x):
        for row in range (size_y):
            grille[row][column]=compter_mines(tiles, row, column, size_x, size_y)  #créé la grille en utilisant la fonction compter_mines
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

def zone_depart(tiles, row, column, proba, size_x, size_y):
    if 0 <= column < size_x and 0 <= row < size_y :   #vérifie que la case n'est pas out of range
        if tiles[row][column] != []:
            if proba >= 0.2:   #empêche d'avoir une zone trop grande
                tiles[row][column] = []    #empeche de placer une mine ici
                for dx, dy in [(0,-1),(0,1),(1,0),(-1,0)]:   #parcourt les cases cases adjacentes (gauche,droite,haut,bas)
                    if random() <= proba:   #genere un nombre entre 0 et 1, devant être inférieur à proba pour supprimer cette case
                        zone_depart(tiles, row + dy, column + dx, proba*0.7, size_x, size_y)    #pour déterminer aléatoirement les cases safes

def gagne(compteur, size_x, size_y, nb_mines):
    """Condition de victoire"""
    if compteur[0] == size_y * size_y - nb_mines :
        return True

        