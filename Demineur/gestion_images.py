
from PIL import Image, ImageTk
import tkinter as tk
IMAGE_SIZE = 16  # taille réelle d’une image
image_path = "demineur_sprite_sheet.png"
sprite_sheet = Image.open(image_path) 

def decouper_image(col, row, niveau):
    
    x1 = col * IMAGE_SIZE
    y1 = row * IMAGE_SIZE
    x2 = x1 + IMAGE_SIZE
    y2 = y1 + IMAGE_SIZE
    image = sprite_sheet.crop((x1, y1, x2, y2))
    if niveau == "Débutant" :
        image = image.resize((45, 45))
    else : 
        image = image.resize((25, 25))
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
        "Drapeau": decouper_image(3, 2, niveau),
    }
    return images
