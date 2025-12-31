"""
Affichage 
"""

import tkinter as tk
from fonctions import *

def creation_fenetre():
    """ Crée la fenêtre avec les boutons """
    board = tk.Tk() # création de la fenêtre
    board.title("Démineur")
    boutons = [[None for i in range(SIZE_X)] for j in range(SIZE_Y)] # créé une liste vide qui servira à accueillir tous les boutons du board
    for column in range(SIZE_X):
        for row in range(SIZE_Y):
            bouton = tk.Button(board, width = 3) 
            bouton.bind("<Button-1>", 
                        lambda event, fc = first_clic, t = tiles, g = grille, b = boutons, r = row, c = column, cpt = compteur : 
                        clic_gauche(event, fc, t, g, b, r, c, cpt)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, g = grille, r = row, c = column : 
                        clic_droit(event, g, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            boutons[row][column] = bouton   # stocke chaque bouton dans la liste
    board.mainloop()

def clic_gauche(event, first_clic, tiles, grille, boutons, row, column, compteur): 
    """ Révèle la case cliquée si elle n'est pas marquée par un drapeau """
    
    if first_clic[0]==False:
        first_clic[0]=True
        print("cbon")
        if hardcore_mode[0]==True:
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(tiles, row, column, proba)
            print ("ccbon")
        else:
            tiles[row][column]=[]
        tiles = create_board(tiles)
        grille = grille_nombres(tiles,grille)
    bouton = event.widget
    case = reveler_case(grille, row, column)
    if bouton["state"] != "disabled":
        if case != "Drapeau" : 
            if case == "Mine" :
                bouton.config(text="💣", bg="red")
                print("Perdu !") # message perdu (à améliorer)
            else :
                reveler_zone (grille, boutons, row, column, compteur)
                if gagne(compteur) :
                    print("gagné !") # message gagné (à améliorer)

def clic_droit(event, grille, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton"""
    bouton = event.widget
    if reveler_case(grille, row, column) == "Drapeau" : # s'il y a un drapeau
        grille = enlever_drapeau(grille, row, column)
        bouton.config(text = "", state = "normal") # enlève le drapeau, réactive le bouton
    elif bouton["state"] != "disabled": # si la case n'est pas désactivée
        grille = ajouter_drapeau(grille, row, column)
        bouton.config(text = "🚩", state = "disabled") # met le drapeau, désactive le bouton

def reveler_zone(grille, boutons, row, column, compteur):
    case = reveler_case(grille, row, column)
    bouton = boutons[row][column]
    if case != "Drapeau":
        if bouton["state"] != "disabled":
            bouton.config(state = "disabled", relief = "sunken", text = str(case) if case != 0 else "")
            compteur[0] += 1
    if case == 0:
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < SIZE_Y and 0 <= new_col < SIZE_X:
                    if boutons[new_row][new_col]["state"] != "disabled" and not (new_row == row and new_col == column):
                        reveler_zone(grille, boutons, new_row, new_col, compteur)

compteur = [0]
first_clic=[False]
hardcore_mode=[True]
tiles = [[0 for i in range (SIZE_X)] for j in range (SIZE_Y)]   # crée une grille remplie de [0]
grille=[[None for column in range(SIZE_X)] for row in range(SIZE_Y)]    
creation_fenetre()