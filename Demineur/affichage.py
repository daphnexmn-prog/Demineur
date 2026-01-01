"""
Affichage 
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from fonctions import *

def creation_fenetre(size_x, size_y, nb_mines):
    """ Crée la fenêtre avec les boutons """
    tiles = [[0 for i in range (size_x)] for j in range (size_y)]   # crée une grille remplie de 0
    grille=[[None for column in range(size_x)] for row in range(size_y)]  
    board = tk.Tk() # création de la fenêtre
    board.title("Démineur")
    boutons = [[None for i in range(size_x)] for j in range(size_y)] # créé une liste vide qui servira à accueillir tous les boutons du board
    for column in range(size_x):
        for row in range(size_y):
            bouton = tk.Button(board, width = 3) 
            bouton.bind("<Button-1>", 
                        lambda event, fc = first_clic, t = tiles, g = grille, b = boutons, r = row, c = column, cpt = compteur, x = size_x, y = size_y, m = nb_mines : 
                        clic_gauche(fc, t, g, b, r, c, cpt, x, y, m)) # commande pour clic gauche
            bouton.bind("<Button-3>", 
                        lambda event, g = grille, r = row, c = column : 
                        clic_droit(event, g, r, c)) # commande pour clic droit
            bouton.grid(row = row, column = column) # place chaque bouton
            boutons[row][column] = bouton   # stocke chaque bouton dans la liste
    board.mainloop()

def clic_gauche(first_clic, tiles, grille, boutons, row, column, compteur, size_x, size_y, nb_mines): 
    """ Révèle la case cliquée si elle n'est pas marquée par un drapeau """
    # faudra vraiment qu'on trouve un moyen pour réduire le nombre de paramètres 
    if first_clic[0]==False:
        first_clic[0]=True
        print("cbon")
        if hardcore_mode[0]==True:
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(tiles, row, column, proba, size_x, size_y)
            print ("ccbon")
        else:
            tiles[row][column]=[]
        tiles = create_board(tiles, size_x, size_y, nb_mines)
        grille = grille_nombres(tiles,grille, size_x, size_y)
    bouton = boutons[row][column]
    case = reveler_case(grille, row, column)
    if bouton["state"] != "disabled":
        if case != "Drapeau" : 
            if case == "Mine" :
                bouton.config(state = "disabled", text="💣", bg="red")
                messagebox.showinfo("", "Perdu !")
            else :
                reveler_zone(grille, boutons, row, column, compteur, size_x, size_y)
                if gagne(compteur, size_x, size_y, nb_mines) :
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

def reveler_zone(grille, boutons, row, column, compteur, size_x, size_y):
    case = reveler_case(grille, row, column)
    bouton = boutons[row][column]
    if case != "Drapeau":
        if bouton["state"] != "disabled":
            bouton.config(state = "disabled", relief = "groove", bg = "#CBEDD7", text = str(case) if case != 0 else "")
            compteur[0] += 1
    if case == 0:
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_row = row + y
                new_col = column + x
                if 0 <= new_row < size_y and 0 <= new_col < size_x :
                    if boutons[new_row][new_col]["state"] != "disabled" and not (new_row == row and new_col == column):
                        reveler_zone(grille, boutons, new_row, new_col, compteur, size_x, size_y)

def interface_accueil():
    """Crée l'interface d'accueil"""
    accueil = tk.Tk()
    accueil.title("Démineur - Nouvelle partie")
    titre = ttk.Label(accueil, text="Démineur", font=("Helvetica", 20))
    lancer_partie = tk.Button(accueil, width = 100, height = 2, text = "Nouvelle partie", command = lambda a = accueil : debut_jeu(a))
    titre.pack() # place le titre
    lancer_partie.pack() # place le bouton de nouvelle partie
    accueil.mainloop()

def choix_niveau(accueil):
        """ Détermine le choix du niveau
        Returns
        -------
        str
            Le niveau choisi
        """
        accueil.destroy() # ferme l'écran d'accueil
        menu = tk.Tk()
        menu.title("Choix du niveau")
        menu.geometry("500x120")
        choix = tk.StringVar() # crée la variable pour récupérer le niveau
        for niveau in ["Débutant", "Intermédiaire", "Avancé"]:
            option = tk.Button(menu, width = 100, height = 2, text = niveau,
                command = lambda n = niveau : (choix.set(n), menu.destroy()))
            option.pack()
        menu.wait_window() # attend que la fenêtre menu soit détruite pour passer à la suite
        return choix.get() 

def debut_jeu(accueil):
    """Lance une partie en fonction du niveau choisi"""
    niveau = choix_niveau(accueil)
    size_y, size_x, nb_mines = difficulte(niveau)
    creation_fenetre(size_x, size_y, nb_mines)

   
compteur = [0] # compteur de cases révélées
first_clic=[False]
hardcore_mode=[True]  

interface_accueil()
