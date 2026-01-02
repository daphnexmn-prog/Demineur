"""
Affichage 
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from logique_jeu import *

def creation_fenetre(p):
    """ Crée la fenêtre avec les boutons 
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """
    board = tk.Tk() # création de la fenêtre
    board.title("Démineur")
    for column in range(p["size_x"]):
        for row in range(p["size_y"]):
            bouton = tk.Button(board, width = 3) 
            bouton.bind("<Button-1>", 
                        lambda event, p = p, r = row, c = column : 
                        clic_gauche(p, r, c,)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, g = p["grille"], r = row, c = column : 
                        clic_droit(event, g, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            p["boutons"][row][column] = bouton   # stocke chaque bouton dans la liste
    board.mainloop() 

def clic_gauche(p, row, column): 
    """ Révèle la case cliquée si elle n'est pas marquée par un drapeau 
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    """
    if p["first_clic"][0] == False:
        p["first_clic"][0] = True
        print("cbon")
        if p["hardcore_mode"][0] == True:
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(p, row, column, proba)
            print ("ccbon")
        else:
            p["tiles"][row][column]=[]
        p["tiles"] = create_board(p)
        p["grille"] = grille_nombres(p)
    bouton = p["boutons"][row][column]
    case = reveler_case(p["grille"], row, column)
    if bouton["state"] != "disabled":
        if case != "Drapeau" : 
            if case == "Mine" :
                bouton.config(state = "disabled", text = "💣", bg = "red")
                messagebox.showinfo("", "Perdu !")
            else :
                reveler_zone(p, row, column)
                if gagne(p) :
                    messagebox.showinfo("", "Gagné !")

def clic_droit(event, grille, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton"""
    bouton = event.widget
    if reveler_case(grille, row, column) == "Drapeau" : # s'il y a un drapeau
        grille = enlever_drapeau(grille, row, column)
        bouton.config(text = "", state = "normal") # enlève le drapeau, réactive le bouton
    elif bouton["state"] != "disabled": # si la case n'est pas désactivée
        grille = ajouter_drapeau(grille, row, column)
        bouton.config(text = "🚩", state = "disabled") # met le drapeau, désactive le bouton

def reveler_zone(p, row, column):
    case = reveler_case(p["grille"], row, column)
    bouton = p["boutons"][row][column]
    if case != "Drapeau":
        if bouton["state"] != "disabled":
            bouton.config(state = "disabled", relief = "groove", bg = "#CBEDD7", 
                          text = str(case) if case != 0 else "")
            p["compteur"][0] += 1
    if case == 0:
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < p["size_y"] and 0 <= new_col < p["size_x"] :
                    if p["boutons"][new_row][new_col]["state"] != "disabled" \
                        and not (new_row == row and new_col == column):
                        reveler_zone(p, new_row, new_col)
