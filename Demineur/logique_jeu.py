"""
Fonctions :
    difficulte(niveau) : Renvoie le nombre de lignes, colonnes et mines en fonction du niveau choisi
    create_board(p) : Crée la grille avec nb_mines mines placées aléatoirement
    compter_mines(p, row, column) : Compte le nombre de mines autour de chaque case et determine si la case est deja une mine
    grille_nombres(p) : Crée une grille comportant pour chaque case la valeur de la fonction compter_mines
    ajouter_drapeau(p, row, column) : Ajoute un drapeau à la case souhaitée
    enlever_drapeau(p, row, column) : Enlève un drapeau à la case souhaitée
    reveler_case(grille, row, column) : Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour
    zone_depart(p, row, column, proba) :
    gagne(p) : Condition de victoire
    timer(p) : Actualise le timer à chaque seconde
"""

from random import *
from time import *

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
    if niveau == "Avancé" or niveau == "Avancé Hardcore":
        return (16, 30, 99)

def create_board(p):
    """ Crée la grille avec nb_mines mines placées aléatoirement

    Parameters
    ---------
    p : dict
        Dictionnaire contenant tous les paramètres
        
    Returns
    -------
    list[list[int]]
        La grille remplie de 0 (case vide) et de 1 (bombe)
    """
    mines_count = 0 # compteur de mines 
    while mines_count < p["nb_mines"]:
        randx = randint(0, p["size_x"]- 1) # colonne aléatoire
        randy = randint(0, p["size_y"] - 1) # ligne aléatoire
        if p["tiles"][randy][randx] == 0:
            p["tiles"][randy][randx] = 1
            mines_count += 1
    return p["tiles"]

def compter_mines(p, row, column):
    """ Compte le nombre de mines autour de chaque case et determine si la case est deja une mine

    Returns
    -------
    list[list[int ou str]]
        La grille remplie de * (bombe) ou de int (case vide)
    """
    if p["tiles"][row][column]==1:   #vérifie si la case est une mine
        return "*"
    else :
        mine_case = 0
        for x in range (-1,2):  #parcourt les cases voisines
            for y in range (-1,2):
                new_col = column + x
                new_row = row + y
                if 0 <= new_col < p["size_x"] and 0 <= new_row < p["size_y"]:   #vérifie que les cases voisines ne sont pas out of range
                    if p["tiles"][new_row][new_col] == 1: 
                        mine_case += 1  #compte le nombre de mines autour de la case
        return mine_case

def grille_nombres(p):
    """ Crée une grille comportant pour chaque case la valeur de la fonction compter_mines

    Returns
    -------
    str(*) si la case est une mine
    int(mine_case) le nombre de mines autour d'une case n'étant pas une mine
    """
    for column in range (p["size_x"]):
        for row in range (p["size_y"]):
            p["grille"][row][column]=compter_mines(p, row, column)  #créé la grille en utilisant la fonction compter_mines
    return p["grille"]

def ajouter_drapeau(p, row, column):
    """ Ajoute un drapeau à la case souhaitée"""
    p["grille"][row][column] = "d" + str(p["grille"][row][column])
    p["drapeaux_restants"]["text"] -= 1

def enlever_drapeau(p, row, column):
    """ Enlève un drapeau à la case souhaitée """
    p["grille"][row][column] = p["grille"][row][column][-1]
    if p["grille"][row][column] != "*" :
        p["grille"][row][column] = int(p["grille"][row][column]) 
    p["drapeaux_restants"]["text"] += 1

def reveler_case(grille, row, column):
    """Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour"""
    if grille[row][column] == "*" :
        return "Mine" 
    elif type(grille[row][column]) == str and grille[row][column][0] == "d":
        return "Drapeau"
    else :
        return grille[row][column] # le nombre de mines autour

def zone_depart(p, row, column, proba):
    if 0 <= column < p["size_x"] and 0 <= row < p["size_y"] :   #vérifie que la case n'est pas out of range
        if p["tiles"][row][column] != []:
            if proba >= 0.2:   #empêche d'avoir une zone trop grande
                p["tiles"][row][column] = []    #empeche de placer une mine ici
                for dx, dy in [(0,-1),(0,1),(1,0),(-1,0)]:   #parcourt les cases cases adjacentes (gauche,droite,haut,bas)
                    if random() <= proba:   #genere un nombre entre 0 et 1, devant être inférieur à proba pour supprimer cette case
                        zone_depart(p, row + dy, column + dx, proba*0.7)    #pour déterminer aléatoirement les cases safes

def gagne(p):
    """Condition de victoire"""
    if p["compteur"] == p["size_y"] * p["size_y"] - p["nb_mines"] :
        return True

def timer(p) : 
    """Actualise le timer à chaque seconde"""
    if not p["fin"]: # si la partie n'est pas terminée
        p["label_timer"]["text"] += 1 # ajoute 1 au compteur
        p["board"].after(1000, lambda p = p : timer(p)) # répète la fonction après 1sec