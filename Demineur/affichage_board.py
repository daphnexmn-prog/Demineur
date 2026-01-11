"""
Affichage 
"""

import tkinter as tk 
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from logique_jeu import *
import gestion_images

def creation_fenetre(p):
    """ Crée la fenêtre avec les boutons 
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """
    board = tk.Tk() # création de la fenêtre
    board.title("Démineur")
    board.configure(bg = "#DEEFF4")
    p["board"] = board
    side = 3 if p["niveau"] == "Débutant" else 2 # taille de la bordure
    p["images"] = gestion_images.charger_images(p["niveau"])  # charge les images après création de la fenêtre principale
    image_pixel = tk.PhotoImage(width = 1, height = 1) # crée une image de 1 pixel de côté pour pouvoir exprimer la taille du bouton en pixels
    button_size = 45 if p["niveau"] == "Débutant" else 25 # taille des boutons
    for row in range(side,p["size_y"]+side):
        for column in range(side, p["size_x"]+side):
            bouton = tk.Button(board, image = image_pixel, compound="c", width = button_size, height = button_size) 
            bouton.bind("<Button-1>", 
                        lambda event, p = p, r = row-side, c = column-side : 
                        clic_gauche(p, r, c,)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, p = p, r = row-side, c = column-side : 
                        clic_droit(p, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            bouton.config(image = p["images"]["Bouton"]) # assigne l'image du bouton
            p["boutons"][row-side][column-side] = bouton   # stocke chaque bouton dans la liste
    p["label_timer"] = ttk.Label(board, text = 0, background = "#DEEFF4")
    for i in range(side):
        for j in range(side) : 
            ttk.Label(board, text = "  ", background = "#DEEFF4").grid(row = i, column = p["size_x"]+ side + j)
            ttk.Label(board, text = "  ", background = "#DEEFF4").grid(row = p["size_y"]+ side + i, column = j)
            # labels invisibles pour les bordures de la fenêtre
    p["label_timer"].grid(row = 1, column = side)
    board.after(1000, lambda p = p : timer(p)) # commence à exécuter timer après 1sec
    p["drapeaux_restants"] = ttk.Label(board, text = p["nb_mines"], background = "#DEEFF4")
    p["drapeaux_restants"].grid(row = 1, column = p["size_x"]+side-1)
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
        if p["hardcore_mode"] == False:
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(p, row, column, proba)
        else:
            p["tiles"][row][column]=[]
        p["tiles"] = create_board(p)
        p["grille"] = grille_nombres(p)
    bouton = p["boutons"][row][column]
    case = reveler_case(p["grille"], row, column)
    if bouton not in p["cases_desactivees"]:
        if case != "Drapeau" : 
            if case == "Mine" :
                bouton.config(image = p["images"]["Mine"])
                p["cases_desactivees"].append(bouton)
                p["fin"] = True # pour que le after s'arrête
                messagebox.showinfo("Perdu !", "Perdu !")
                p["board"].after(10, p["board"].destroy) # détruit la fenêtre après 10ms 
                # (sinon tkinter n'a pas fini de gérer les derniers clics de boutons)
            else :
                reveler_zone(p, row, column)
                if gagne(p) :
                    p["fin"] = True # idem
                    messagebox.showinfo("Gagné !", "Vous avez gagné en "+ str(p["label_timer"]["text"])+" secondes !")
                    p["board"].after(10, p["board"].destroy) # idem
    return "break"
                    
def clic_droit(p, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton"""
    bouton = p["boutons"][row][column]
    if p["first_clic"] == False:
        return
    if reveler_case(p["grille"], row, column) == "Drapeau" : # s'il y a un drapeau
        enlever_drapeau(p, row, column)
        bouton.config(image = p["images"]["Bouton"]) # enlève le drapeau
        p["cases_desactivees"].remove(bouton) 
    elif bouton not in p["cases_desactivees"]: # si la case n'est pas désactivée
        ajouter_drapeau(p, row, column)
        bouton.config(image = p["images"]["Drapeau"]) # met le drapeau 
        p["cases_desactivees"].append(bouton) 


def reveler_zone(p, row, column):
    case = reveler_case(p["grille"], row, column)
    bouton = p["boutons"][row][column]
    if case != "Drapeau":
        if bouton not in p["cases_desactivees"]:
            p["cases_desactivees"].append(bouton)
            bouton.config(relief = "sunken", image = p["images"][case])
            p["compteur"] += 1
    if case == 0:
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < p["size_y"] and 0 <= new_col < p["size_x"] :
                    if p["boutons"][new_row][new_col] not in p["cases_desactivees"]:
                        reveler_zone(p, new_row, new_col)
    
                    