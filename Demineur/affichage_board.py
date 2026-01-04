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
    p["board"] = board
    for column in range(p["size_x"]):
        for row in range(1,p["size_y"]+1):
            bouton = tk.Button(board, width = 3) 
            bouton.bind("<Button-1>", 
                        lambda event, p = p, r = row-1, c = column : 
                        clic_gauche(p, r, c,)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, p = p, r = row-1, c = column : 
                        clic_droit(p, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            p["boutons"][row-1][column] = bouton   # stocke chaque bouton dans la liste
    p["label_timer"] = ttk.Label(board, text = 0)
    p["label_timer"].grid(row = 0, column = 0)
    board.after(1000, lambda p = p : timer(p))
    p["drapeaux_restants"] = ttk.Label(board, text = p["nb_mines"])
    p["drapeaux_restants"].grid(row = 0, column = p["size_x"]-1)
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
    if p["first_clic"] == False:
        p["first_clic"] = True
        if p["hardcore_mode"] == True:
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(p, row, column, proba)
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
                p["fin"] = True
                messagebox.showinfo("", "Perdu !")
                p["board"].destroy()
            else :
                reveler_zone(p, row, column)
                if gagne(p) :
                    p["fin"] = True
                    messagebox.showinfo("Gagné !", "Vous avez gagné en "+ str(p["label_timer"]["text"])+" secondes !")
                    p["board"].destroy()
                    
def clic_droit(p, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton"""
    bouton = p["boutons"][row][column]
    if reveler_case(p["grille"], row, column) == "Drapeau" : # s'il y a un drapeau
        enlever_drapeau(p, row, column)
        bouton.config(text = "", state = "normal") # enlève le drapeau, réactive le bouton
    elif bouton["state"] != "disabled": # si la case n'est pas désactivée
        ajouter_drapeau(p, row, column)
        bouton.config(text = "🚩", state = "disabled") # met le drapeau, désactive le bouton

def reveler_zone(p, row, column):
    case = reveler_case(p["grille"], row, column)
    bouton = p["boutons"][row][column]
    if case != "Drapeau":
        if bouton["state"] != "disabled":
            bouton.config(state = "disabled", relief = "groove", bg = "#CBEDD7", 
                          text = str(case) if case != 0 else "")
            p["compteur"] += 1
    if case == 0:
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < p["size_y"] and 0 <= new_col < p["size_x"] :
                    if p["boutons"][new_row][new_col]["state"] != "disabled" \
                        and not (new_row == row and new_col == column):
                        reveler_zone(p, new_row, new_col)