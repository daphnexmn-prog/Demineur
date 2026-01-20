"""
gestion_images_et_musiques
Ce fichier :
- découpe les images des cases
- crée le dictionnaire contenant ces images
- définit les différents effets sonores
- gère le lancement des musiques
"""
from random import randint
from PIL import Image, ImageTk
import pygame

IMAGE_SIZE = 16  # taille réelle d’une image

image_path = "demineur_sprite_sheet.png"
sprite_sheet = Image.open(image_path) 

def decouper_image(col, row, niveau) :
    """ Découpe l'image de la case souhaitée
    Parameters 
    ----------
    col : int
        La colonne de l'image choisie
    row : int
        La ligne de l'image choisie
    niveau : str
        Le niveau choisi
    
    Returns
    -------
    PhotoImage 
        L'image correspondante
    """
    x1 = col * IMAGE_SIZE
    y1 = row * IMAGE_SIZE
    x2 = x1 + IMAGE_SIZE
    y2 = y1 + IMAGE_SIZE

    # Découpe l'image
    image = sprite_sheet.crop((x1, y1, x2, y2))

    # Redimensionne l'image en fonction du niveau
    if niveau == "Débutant" :
        image = image.resize((50, 50), Image.NEAREST)
    else : 
        image = image.resize((30, 30), Image.NEAREST)
    image = ImageTk.PhotoImage(image)
    return image

def charger_images(niveau):
    """Charge et retourne le dictionnaire des images

    Parameters
    ----------
    niveau : str
        Le niveau choisi
    
    Returns
    -------
    dict
        Le dictionnaire contenant les images
    """
    images = {
        1: decouper_image(0, 0, niveau),
        2: decouper_image(1, 0, niveau),
        3: decouper_image(2, 0, niveau),
        4: decouper_image(3, 0, niveau),
        5: decouper_image(0, 1, niveau),
        6: decouper_image(1, 1, niveau),
        7: decouper_image(2, 1, niveau),
        8: decouper_image(3, 1, niveau),
        0: decouper_image(0, 2, niveau),
        "Bouton" : decouper_image(1, 2, niveau),
        "Mine": decouper_image(2, 2, niveau),
        "Drapeau" : decouper_image(3, 2, niveau),
    }
    return images

pygame.mixer.init()

Son_win = pygame.mixer.Sound('musiques/Win.mp3')
Son_lose = pygame.mixer.Sound('musiques/Game_over.mp3')
Son_clic = pygame.mixer.Sound('musiques/Clic.wav')
Son_explosion = pygame.mixer.Sound('musiques/Explosion.mp3')
Son_menu_clic_1 = pygame.mixer.Sound('musiques/Menu_clic_1.mp3')
Son_menu_clic_2 = pygame.mixer.Sound('musiques/Menu_clic_2.mp3')
Enlever_drapeau = pygame.mixer.Sound('musiques/Enlever_drapeau.wav')
Placer_drapeau = pygame.mixer.Sound('musiques/Placer_drapeau.wav')
Propagation = pygame.mixer.Sound('musiques/Propagation_des_0.mp3')

pygame.mixer.music.set_volume(0.7) # pour diminuer et équilibrer le volume des musiques de fond

def musique_suivante(p):
    """ Lance la musique suivante choisie aléatoirement
    Parameters 
    ----------
    p : dict
        Le dictionnaire contenant tous les paramètres
    """
    if p["fin"]: # si la partie est terminée
        return # pour éviter de lancer une nouvelle musique après la fin de la partie
    
    # Choisit un numéro de musique aléatoire
    numero = randint(1,12)

    # Joue la musique
    pygame.mixer.music.load("musiques/Musique_" + str(numero) + ".mp3") # charge la musique associée au numéro aléatoire
    pygame.mixer.music.play()
    duree = pygame.mixer.Sound("musiques/Musique_" + str(numero) + ".mp3").get_length()

    # Exécute de nouveau la fonction à la fin de la musique
    p["board"].after(int(duree * 1000), lambda p = p : musique_suivante(p))
