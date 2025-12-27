"""
Affichage 
"""

import tkinter as tk
from fonctions import *

def creation_fenetre():
    """ Crée la fenêtre avec les boutons """
    board = tk.Tk() # création de la fenêtre
    board.title("Démineur")
    for column in range(SIZE_X):
        for row in range(SIZE_Y):
            bouton = tk.Button(board, width = 3) 
            bouton.bind("<Button-1>", 
                        lambda event, g = grille, r = row, c = column, cpt = compteur : 
                        clic_gauche(event, g, r, c, cpt)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, g = grille, r = row, c = column : 
                        clic_droit(event, g, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
    board.mainloop()

def clic_gauche(event, grille, row, column, compteur): 
    """ Révèle la case cliquée si elle n'est pas marquée par un drapeau """
    bouton = event.widget
    case = reveler_case(grille, row, column)
    if case != "Drapeau" : 
        if case == "Mine" :
            pass # message perdu
        elif type(case) == int :
            bouton.config(state = "disabled", relief = "sunken")
            bouton.config(text = "") # faudra changer l'apparence du bouton avec le nombre
            compteur[0] += 1
            if gagne(compteur) :
                pass # message gagné

def clic_droit(event, grille, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton"""
    bouton = event.widget
    if reveler_case(grille, row, column) == "Drapeau" : # s'il y a un drapeau
        grille = enlever_drapeau(grille, row, column)
        bouton.config(text = "")
        bouton.config(state = "normal") # réactive le bouton
    elif bouton["state"] != "disabled":
        grille = ajouter_drapeau(grille, row, column)
        bouton.config(text = "🚩")
        bouton.config(state = "disabled") # désactive le bouton

compteur = [0]
grille = create_board()
creation_fenetre()
