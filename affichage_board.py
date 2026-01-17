"""
Affichage 
"""

import time
import tkinter as tk 
from tkinter import messagebox
from logique_jeu import *
from gestion_images_et_musiques import *

def creation_fenetre(p):
    """ Crée la fenêtre avec les boutons 
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    """
    p["board"] = tk.Tk() # création de la fenêtre
    p["board"].title("Démineur")
    p["board"].configure(bg = "#DEEFF4")
    side = 3 if p["niveau"] == "Débutant" else 2 # taille de la bordure
    p["images"] = charger_images(p["niveau"])  # charge les images après création de la fenêtre principale
    button_size = 50 if p["niveau"] == "Débutant" else 30 # taille des boutons
    for row in range(side, p["size_y"] + side):
        for column in range(side, p["size_x"] + side):
            bouton = tk.Button(p["board"], image = p["images"]["Bouton"], width = button_size, height = button_size, bd = 0, highlightthickness = 0) # crée chaque bouton
            bouton.bind("<Button-1>", 
                        lambda event, p = p, r = row - side, c = column - side : 
                        clic_gauche(p, r, c,)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, p = p, r = row - side, c = column - side : 
                        clic_droit(p, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            p["boutons"][row - side][column - side] = bouton   # stocke chaque bouton dans la liste
    p["label_timer"] = tk.Label(p["board"], text = 0, background = "#DEEFF4")
    p["drapeaux_restants"] = tk.Label(p["board"], text = p["nb_mines"], background = "#DEEFF4")
    for i in range(side):
        for j in range(side) : 
            tk.Label(p["board"], text = "  ", background = "#DEEFF4").grid(row = i, column = p["size_x"] + side + j)
            tk.Label(p["board"], text = "  ", background = "#DEEFF4").grid(row = p["size_y"]+ side + i, column = j)
            # labels invisibles pour les bordures de la fenêtre
    p["board"].after(1000, lambda p = p : timer(p)) # commence à exécuter timer après 1sec
    p["label_timer"].grid(row = 1, column = side)
    p["drapeaux_restants"].grid(row = 1, column = p["size_x"] + side - 1)
    musique_suivante(p)
    p["board"].mainloop() 

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
        if p["niveau"] != "Avancé Hardcore" :
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(p, row, column, proba)
        else :
            p["tiles"][row][column] = []
        p["tiles"] = create_board(p)
        p["grille"] = grille_nombres(p)
    bouton = p["boutons"][row][column]
    case = reveler_case(p["grille"], row, column)
    if bouton not in p["cases_desactivees"] and case != "Drapeau" :
        if case == "Mine" :
            reveler_mines(p)
            p["fin"] = True # pour que le after s'arrête
            pygame.mixer.music.stop()
            Son_explosion.play()
            Son_lose.play()
            messagebox.showinfo("Perdu !", "Perdu !")
            p["board"].after(10, p["board"].destroy) # détruit la fenêtre après 10ms 
        else :
            zero = reveler_zone(p, row, column)
            if zero :
                Propagation.play()
            else :
                Son_clic.play()
            if gagne(p) :
                p["fin"] = True 
                pygame.mixer.music.stop()
                Son_win.play()
                messagebox.showinfo("Gagné !", "Vous avez gagné en "+ str(p["label_timer"]["text"])+" secondes !")
                p["board"].after(10, p["board"].destroy) 
    return "break"
                    
def clic_droit(p, row, column):
    """Ajoute/enlève un drapeau sur la case cliquée et désactive/réactive le bouton
    
    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    """
    bouton = p["boutons"][row][column]
    if not p["first_clic"] :
        return
    if reveler_case(p["grille"], row, column) == "Drapeau" : # s'il y a un drapeau 
        enlever_drapeau(p, row, column)
        bouton.config(image = p["images"]["Bouton"]) # enlève le drapeau
        Enlever_drapeau.play()
        p["cases_desactivees"].remove(bouton) 
    elif bouton not in p["cases_desactivees"] and p["drapeaux_restants"]["text"] > 0 : # si la case n'est pas désactivée et qu'il reste des drapeaux à placer
        ajouter_drapeau(p, row, column)
        bouton.config(image = p["images"]["Drapeau"]) # met le drapeau 
        Placer_drapeau.play()
        p["cases_desactivees"].append(bouton) 

def reveler_zone(p, row, column) :
    case = reveler_case(p["grille"], row, column)
    bouton = p["boutons"][row][column]
    PROPAGATION_DES_0 = False
    if case != "Drapeau":
        if bouton not in p["cases_desactivees"]:
            p["cases_desactivees"].append(bouton)
            bouton.config(relief = "sunken", image = p["images"][case])
            p["compteur"] += 1
    if case == 0:
        PROPAGATION_DES_0 = True
        for x in range(-1, 2) :
            for y in range(-1, 2) :
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < p["size_y"] and 0 <= new_col < p["size_x"] :
                    if p["boutons"][new_row][new_col] not in p["cases_desactivees"] :
                        reveler_zone(p, new_row, new_col)
    return PROPAGATION_DES_0
    