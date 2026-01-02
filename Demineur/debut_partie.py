"""Début partie"""

from affichage import *

def interface_accueil():
    """Crée l'interface d'accueil"""
    accueil = tk.Tk() # crée la fenêtre d'accueil
    accueil.title("Démineur - Nouvelle partie")
    titre = ttk.Label(accueil, text="Démineur", font=("Helvetica", 20))
    lancer_partie = tk.Button(accueil, width = 100, height = 2, text = "Nouvelle partie", 
                              command = lambda a = accueil : debut_jeu(a))
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
        menu = tk.Tk() # crée une fenêtre menu
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
    """Lance une partie en fonction du niveau choisi et définit les paramètres"""
    niveau = choix_niveau(accueil)
    size_y, size_x, nb_mines = difficulte(niveau)
    tiles = [[0 for i in range (size_x)] for j in range (size_y)]   # crée une grille remplie de 0
    grille = [[None for column in range(size_x)] for row in range(size_y)]
    boutons = [[None for i in range(size_x)] for j in range(size_y)] # crée une liste vide qui servira à accueillir tous les boutons du board
    parametres = {"tiles": tiles, 
                  "grille" : grille, 
                  "boutons" : boutons,
                  "first_clic" : [False],
                  "hardcore_mode" : [True],
                  "compteur" : [0], # compteur de cases révélées
                  "size_x" : size_x, 
                  "size_y" : size_y, 
                  "nb_mines" : nb_mines 
                  }
    creation_fenetre(parametres)
   
interface_accueil()