"""
affichage_board
Ce fichier gère :
- la création de la fenêtre principale
- la révélation des zones
"""

import tkinter as tk 
from logique_jeu import *
from gestion_images_et_musiques import *
from gestion_clics import *

def creation_fenetre(p):
    """ Crée la fenêtre avec les boutons 
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """

    # Création de la fenêtre principale
    p["board"] = tk.Tk() 
    p["board"].title("Démineur")
    p["board"].configure(bg = "#DEEFF4")

    button_size = 50 if p["niveau"] == "Débutant" else 30 # taille des boutons
    side = 3 if p["niveau"] == "Débutant" else 2 # taille de la bordure

    # Charge les images après création de la fenêtre principale
    p["images"] = charger_images(p["niveau"])  

    # Crée chaque bouton
    for row in range(side, p["size_y"] + side):
        for column in range(side, p["size_x"] + side):
            bouton = tk.Button(p["board"], image = p["images"]["Bouton"], 
                               width = button_size, height = button_size, 
                               bd = 0.01, highlightthickness = 1) 
            bouton.bind("<Button-1>", 
                        lambda event, p = p, r = row - side, c = column - side : 
                        clic_gauche(p, r, c,)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, p = p, r = row - side, c = column - side : 
                        clic_droit(p, r, c)) # commande pour clic droit
            
            # Place chaque bouton
            bouton.grid(row = row, column = column) 

            # Stocke chaque bouton dans la liste
            p["boutons"][row - side][column - side] = bouton  

    # Crée le timer et le compteur de drapeaux        
    p["label_timer"] = tk.Label(p["board"], text = 0, background = "#DEEFF4")
    p["drapeaux_restants"] = tk.Label(p["board"], text = p["nb_mines"], background = "#DEEFF4")

    # Labels invisibles pour les bordures de la fenêtre
    for i in range(side):
        for j in range(side) : 
            tk.Label(p["board"], text = "  ", background = "#DEEFF4").grid(row = i, column = p["size_x"] + side + j)
            tk.Label(p["board"], text = "  ", background = "#DEEFF4").grid(row = p["size_y"]+ side + i, column = j)

    # Commence à exécuter timer après 1sec        
    p["board"].after(1000, lambda p = p : timer(p)) 

    # Place le timer et le compteur de drapeaux
    p["label_timer"].grid(row = 1, column = side)
    p["drapeaux_restants"].grid(row = 1, column = p["size_x"] + side - 1)

    # Lance la musique
    musique_suivante(p)

    # Affiche la fenêtre
    p["board"].mainloop() 

def reveler_zone(p, row, column) :
    """
    Révèle la zone cliquée
    
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    """
    # Détermine le bouton cliqué et la case de la grille correspondante
    bouton = p["boutons"][row][column]
    case = case_type(p["grille"], row, column)

    propagation_des_0 = False

    # Révèle la case si elle n'est ni marquée par un drapeau ni désactivée
    if case != "Drapeau" and bouton not in p["cases_desactivees"] :
        p["cases_desactivees"].append(bouton)
        bouton.config(relief = "sunken", image = p["images"][case])
        p["compteur"] += 1

    # Propage les 0 si la case cliquée est 0
    if case == 0 :
        propagation_des_0 = True

        # Parcourt les cases voisines
        for x in range(-1, 2) :
            for y in range(-1, 2) :
                new_row = row + y
                new_col = column + x
                # Vérifie que la case n'est pas out of range
                if 0 <= new_row < p["size_y"] and 0 <= new_col < p["size_x"] :
                    if p["boutons"][new_row][new_col] not in p["cases_desactivees"] :
                        reveler_zone(p, new_row, new_col) # révèle la zone
    return propagation_des_0