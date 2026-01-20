""" 
debut_partie
Ce fichier gère :
- le lancement d'une partie
- le choix du niveau 
- et définit les paramètres
"""

from affichage_board import *

NIVEAUX = {"Débutant" : (9, 9, 10),
           "Intermédiaire" : (16, 16, 40),
           "Avancé" : (16, 30, 99),
           "Avancé Hardcore" : (16, 30, 99)}

def interface_accueil() :
    """ Crée l'interface d'accueil """

    accueil = tk.Tk() # crée la fenêtre d'accueil
    accueil.attributes("-topmost", True) # met la fenêtre au premier plan
    accueil.title("Démineur - Nouvelle partie")

    # Lance la musique de menu
    pygame.mixer.init() # initialise le mixer
    pygame.mixer.music.load("musiques/Musique_menu.mp3")
    pygame.mixer.music.play(-1) # le -1 permet de jouer la musique en boucle

    # Image de la fenêtre d'accueil
    image_logo = Image.open("demineur_logo.png")
    image_logo = image_logo.resize((768, 375))
    image_logo = ImageTk.PhotoImage(image_logo)
    logo = tk.Label(accueil, image = image_logo)
    logo.pack()

    # Bouton de nouvelle partie
    lancer_partie = tk.Button(accueil, width = 109, height = 3, 
                              text = "Nouvelle partie", command = lambda : (accueil.destroy(), Son_menu_clic_1.play()))
    lancer_partie.pack() 
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

        # Bouton pour chaque niveau
        for niveau in ["Débutant", "Intermédiaire", "Avancé", "Avancé Hardcore"]:
            option = tk.Button(menu, width = 100, height = 4, text = niveau,
                command = lambda n = niveau : (choix.set(n), menu.destroy(), Son_menu_clic_2.play())) #
            option.pack()
        menu.wait_window() # attend que la fenêtre menu soit détruite pour passer à la suite
        return choix.get() 

def debut_jeu() :
    """ Lance une partie en fonction du niveau choisi et définit les paramètres """

    # Récupère le niveau choisi et détermine les dimensions
    niveau = choix_niveau()
    size_y, size_x, nb_mines = NIVEAUX[niveau]

    # Crée deux listes tiles et grille, remplies respectivement de 0 et de None
    tiles = [[0 for i in range (size_x)] for j in range (size_y)]   
    grille = [[None for column in range(size_x)] for row in range(size_y)]

    # Crée une liste vide qui servira à accueillir tous les boutons du board
    boutons = [[None for i in range(size_x)] for j in range(size_y)] 
    
    # Crée un dictionnaire pour ranger les paramètres
    parametres = {"tiles": tiles, 
                  "grille" : grille, 
                  "boutons" : boutons,
                  "first_clic" : False,
                  "compteur" : 0, # compteur de cases révélées
                  "size_x" : size_x, # nombre de colonnes
                  "size_y" : size_y, # nombre de lignes
                  "nb_mines" : nb_mines, # nombre de mines
                  "niveau": niveau,
                  "fin" : False, # état de la partie (terminée ou non)
                  "cases_desactivees" : [] # liste de cases désactivées
                  }
    creation_fenetre(parametres)

    # Recommence ou non la partie
    if messagebox.askyesno(message = "Souhaitez-vous recommencer ?") == True :
        interface_accueil()

# Lance la partie   
interface_accueil()