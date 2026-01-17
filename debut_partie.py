"""Début partie"""

from affichage_board import *

def interface_accueil() :
    """ Crée l'interface d'accueil """
    accueil = tk.Tk() # crée la fenêtre d'accueil
    accueil.attributes("-topmost", True) # met la fenêtre au premier plan
    accueil.title("Démineur - Nouvelle partie")
    lancer_partie = tk.Button(accueil, width = 100, height = 3, text = "Nouvelle partie", command = accueil.destroy)
    tk.Label(accueil, text = "Démineur", font = ("Helvetica", 20)).pack() # place le titre
    lancer_partie.pack() # place le bouton de nouvelle partie
    accueil.mainloop()
    debut_jeu()

def choix_niveau() :
        """ Détermine le choix du niveau

        Returns
        -------
        str
            Le niveau choisi
        """
        menu = tk.Tk() # crée une fenêtre menu
        menu.title("Choix du niveau")
        choix = tk.StringVar() # crée la variable pour récupérer le niveau
        for niveau in ["Débutant", "Intermédiaire", "Avancé", "Avancé Hardcore"]:
            option = tk.Button(menu, width = 100, height = 4, text = niveau,
                command = lambda n = niveau : (choix.set(n), menu.destroy()))
            option.pack()
        menu.wait_window() # attend que la fenêtre menu soit détruite pour passer à la suite
        return choix.get() 

def debut_jeu() :
    """ Lance une partie en fonction du niveau choisi et définit les paramètres """
    niveau = choix_niveau()
    size_y, size_x, nb_mines = difficulte(niveau)
    tiles = [[0 for i in range (size_x)] for j in range (size_y)]   # crée une grille remplie de 0
    grille = [[None for column in range(size_x)] for row in range(size_y)]
    boutons = [[None for i in range(size_x)] for j in range(size_y)] # crée une liste vide qui servira à accueillir tous les boutons du board
    parametres = {"tiles": tiles, 
                  "grille" : grille, 
                  "boutons" : boutons,
                  "first_clic" : False,
                  "compteur" : 0, # compteur de cases révélées
                  "size_x" : size_x, 
                  "size_y" : size_y, 
                  "nb_mines" : nb_mines,
                  "niveau": niveau,
                  "fin" : False,
                  "cases_desactivees" : []
                  }
    creation_fenetre(parametres)
    if messagebox.askyesno(message = "Souhaitez-vous recommencer ?") == True :
        interface_accueil()
   
interface_accueil()