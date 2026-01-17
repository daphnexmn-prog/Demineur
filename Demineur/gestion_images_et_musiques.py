from random import randint
from PIL import Image, ImageTk
import pygame
IMAGE_SIZE = 16  # taille réelle d’une image
image_path = "Demineur/demineur_sprite_sheet.png"
sprite_sheet = Image.open(image_path) 

def decouper_image(col, row, niveau) :
    
    x1 = col * IMAGE_SIZE
    y1 = row * IMAGE_SIZE
    x2 = x1 + IMAGE_SIZE
    y2 = y1 + IMAGE_SIZE
    image = sprite_sheet.crop((x1, y1, x2, y2))
    if niveau == "Débutant" :
        image = image.resize((50, 50), Image.NEAREST)
    else : 
        image = image.resize((30, 30), Image.NEAREST)
    image = ImageTk.PhotoImage(image)
    return image

def charger_images(niveau):
    """Charge et retourne le dictionnaire des images"""
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

Son_win = pygame.mixer.Sound('Demineur/musiques/Win.mp3')
Son_lose = pygame.mixer.Sound('Demineur/musiques/Game_over.mp3')
Son_clic = pygame.mixer.Sound('Demineur/musiques/Clic.wav')
Son_explosion = pygame.mixer.Sound('Demineur/musiques/Explosion.mp3')
Enlever_drapeau = pygame.mixer.Sound('Demineur/musiques/Enlever_drapeau.wav')
Placer_drapeau = pygame.mixer.Sound('Demineur/musiques/Placer_drapeau.wav')
Propagation = pygame.mixer.Sound('Demineur/musiques/Propagation_des_0.mp3')


def musique_suivante(p):
    numero = randint(1,4)
    pygame.mixer.music.load("Demineur/musiques/Musique_"+str(numero)+".mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    duree=pygame.mixer.Sound("Demineur/musiques/Musique_"+str(numero)+".mp3").get_length()
    p["board"].after(int(duree * 1000), musique_suivante, p)
