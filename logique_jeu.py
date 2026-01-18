"""
logique_jeu
Ce fichier gère :
- la création de la grille
- le type de cases
- la création d'une zone de départ
- la condition de victoire
- le timer
"""

from random import *

def create_board(p) :
    """ Crée la grille avec nb_mines mines placées aléatoirement

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    
    Returns
    -------
    list[list[int]]
        La grille remplie de 0 (case vide) et de 1 (bombe)
    """
    mines_count = 0 # compteur de mines placées
    while mines_count < p["nb_mines"] :
        # Détermine une ligne et une colonne aléatoire
        randx = randint(0, p["size_x"] - 1) 
        randy = randint(0, p["size_y"] - 1) 
        # Place la mine si la case n'est pas déjà une mine
        if p["tiles"][randy][randx] == 0 :
            p["tiles"][randy][randx] = 1
            mines_count += 1
    return p["tiles"]

def compter_mines(p, row, column) :
    """ Compte le nombre de mines autour de chaque case et determine si la case est deja une mine

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne

    Returns
    -------
    list[list[int ou str]]
        La grille remplie de * (bombe) ou de int (case vide)
    """
    # Vérifie si la case est une mine
    if p["tiles"][row][column] == 1 :   
        return "*"
    else :
        mine_case = 0 # nombre de mines autour d'une case
        # Parcourt les cases voisines
        for x in range (-1, 2) :  
            for y in range (-1, 2) :
                new_col = column + x
                new_row = row + y
                # Vérifie que les cases voisines ne sont pas out of range
                if 0 <= new_col < p["size_x"] and 0 <= new_row < p["size_y"] :   
                    if p["tiles"][new_row][new_col] == 1 : 
                        mine_case += 1  # compte le nombre de mines autour de la case
        return mine_case

def grille_nombres(p):
    """ Crée une grille comportant pour chaque case la valeur de la fonction compter_mines

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    
    Returns
    -------
    str(*) si la case est une mine
    int(mine_case) le nombre de mines autour d'une case n'étant pas une mine
    """
    # Crée la grille en utilisant la fonction compter_mines
    for column in range (p["size_x"]) :
        for row in range (p["size_y"]) :
            p["grille"][row][column] = compter_mines(p, row, column)  
    return p["grille"]

def case_type(grille, row, column) :
    """Renvoie si la case est une mine, marquée par un drapeau ou le nombre de mines autour

    Parameters
    ----------
    grille : list
        La grille 
    row : int
        Ligne
    column : int
        Colonne

    Returns
    -------
    "Mine", "Drapeau" ou int (nombre de mines autour)
    """
    if grille[row][column] == "*" :
        return "Mine" 
    elif type(grille[row][column]) == str and grille[row][column][0] == "d" :
        return "Drapeau"
    else :
        return grille[row][column] # le nombre de mines autour

def zone_depart(p, row, column, proba) :
    """ Crée une zone de départ safe

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    proba : float
        
    """
    # Vérifie que la case n'est pas out of range
    if 0 <= column < p["size_x"] and 0 <= row < p["size_y"] :  
        if p["tiles"][row][column] != [] :

            # Empêche d'avoir une zone trop grande
            if proba >= 0.2:   

                # Empêche de placer une mine ici
                p["tiles"][row][column] = []

                # Parcourt les cases adjacentes (gauche, droite, haut, bas)
                for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)] :  

                    # Génère un nombre entre 0 et 1, 
                    # devant être inférieur à proba pour supprimer cette case
                    # pour déterminer aléatoirement les cases safe
                    if random() <= proba:   
                        zone_depart(p, row + dy, column + dx, proba * 0.7)    

def reveler_mines(p):
    """ Révèle toutes les mines sur le board à la fin de la partie

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """
    # Parcourt la grille
    for row in range(p["size_y"]) :
        for column in range(p["size_x"]) :
            # Détermine la case et le bouton 
            case = case_type(p["grille"], row, column)
            bouton = p["boutons"][row][column]
            # Affiche les mines
            if case == "Mine" and bouton not in p["cases_desactivees"] :
                bouton.config(image = p["images"]["Mine"])
                p["cases_desactivees"].append(bouton)


def gagne(p):
    """ Condition de victoire, si le joueur a cliqué sur toutes les cases sauf les mines
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres

    Returns
    -------
    True ou False
    """
    return p["compteur"] == p["size_y"] * p["size_x"] - p["nb_mines"] 

def timer(p) : 
    """Actualise le timer à chaque seconde

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """
    if not p["fin"]: # si la partie n'est pas terminée
        p["label_timer"]["text"] += 1 # ajoute 1 au compteur
        p["board"].after(1000, lambda p = p : timer(p)) # répète la fonction après 1sec