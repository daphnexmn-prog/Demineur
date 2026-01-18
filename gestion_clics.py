""" 
gestions_clics
Ce fichier :
- gère les clics de l'utilisateur 
- clic gauche : 
    révèle la case ou la zone cliquée si elle n'est pas marquée par un drapeau
    gère la fin d'une partie (victoire et défaite)
- clic droit : ajoute ou enlève un drapeau
"""

from logique_jeu import *
from gestion_images_et_musiques import *
from tkinter import messagebox

def clic_gauche(p, row, column): 
    """ Révèle la case/zone cliquée si elle n'est pas marquée par un drapeau 
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
    "break"
    """

    # Import la fonction après pour éviter l'import circulaire
    from affichage_board import reveler_zone

    # Premier clic
    if p["first_clic"] == False:
        p["first_clic"] = True
        if p["niveau"] != "Avancé Hardcore" :
            proba = 1.3     #proba > 1 pour garantir les premieres cases
            zone_depart(p, row, column, proba)
        else :
            p["tiles"][row][column] = []

        # Crée la grille
        p["tiles"] = create_board(p)
        p["grille"] = grille_nombres(p)

    # Détermine le bouton et la case correspondante   
    bouton = p["boutons"][row][column]
    case = case_type(p["grille"], row, column)

    # Si le bouton est activé
    if bouton not in p["cases_desactivees"] and case != "Drapeau" :

        if case == "Mine" :
            reveler_mines(p) # révèle les mines
            p["fin"] = True 

            # Effets sonores
            pygame.mixer.music.stop()
            Son_explosion.play()
            Son_lose.play()

            # Affiche message de défaite et détruit la fenêtre après 10ms
            messagebox.showinfo("Perdu !", "Perdu !")
            p["board"].after(10, p["board"].destroy) 
        else :
            zero = reveler_zone(p, row, column) # révèle la zone

            # Effets sonores
            if zero :
                Propagation.play()
            else :
                Son_clic.play()

            # Victoire
            if gagne(p) :
                p["fin"] = True 

                # Effets sonores
                pygame.mixer.music.stop()
                Son_win.play()

                # Affiche message de victoire et détruit la fenêtre après 10ms
                messagebox.showinfo("Gagné !", "Vous avez gagné en " + 
                                    str(p["label_timer"]["text"]) + " secondes !")
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
    # Détermine le bouton cliqué
    bouton = p["boutons"][row][column]

    # Premier clic
    if not p["first_clic"] :
        return
    
    # Enlève le drapeau s'il y en a un
    if case_type(p["grille"], row, column) == "Drapeau" : 
        # Enlève le drapeau à la case de la grille correspondante
        enlever_drapeau(p, row, column) 

        # Change l'image du bouton et effet sonore
        bouton.config(image = p["images"]["Bouton"])
        Enlever_drapeau.play()

        # Enlève le bouton de la liste des cases désactivées
        p["cases_desactivees"].remove(bouton) 

    # Place un drapeau si la case n'est pas désactivée et qu'il reste des drapeaux à placer
    elif bouton not in p["cases_desactivees"] and p["drapeaux_restants"]["text"] > 0 : 
        # Ajoute un drapeau à la case de la grille correspondante
        ajouter_drapeau(p, row, column)

        # Change l'image du bouton et effet sonore
        bouton.config(image = p["images"]["Drapeau"]) 
        Placer_drapeau.play()

        # Ajoute le bouton à la liste des cases désactivées
        p["cases_desactivees"].append(bouton) 

def ajouter_drapeau(p, row, column) :
    """ Ajoute un drapeau à la case souhaitée 

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    """
    p["grille"][row][column] = "d" + str(p["grille"][row][column]) # marque la case correspondante
    p["drapeaux_restants"]["text"] -= 1 # enlève 1 au compteur de drapeaux

def enlever_drapeau(p, row, column) :
    """ Enlève un drapeau à la case souhaitée 

    Parameters
    ----------
    p : dict
        Dictionnaire contenant tous les paramètres
    row : int
        Ligne
    column : int
        Colonne
    """
    # Enlève le caractère "d" de la case
    p["grille"][row][column] = p["grille"][row][column][-1]
    # Re-transforme en int si ce n'est pas une mine
    if p["grille"][row][column] != "*" :
        p["grille"][row][column] = int(p["grille"][row][column]) 
    p["drapeaux_restants"]["text"] += 1 # ajoute 1 au compteur de drapeaux
