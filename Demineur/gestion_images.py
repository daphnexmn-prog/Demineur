from PIL import Image, ImageTk
import tkinter as tk
IMAGE_SIZE = 16  # taille réelle d’une image
image_path = "demineur_sprite_sheet.png"
sprite_sheet = Image.open(image_path) 

def decouper_image(col, row):
    
    x1 = col * IMAGE_SIZE
    y1 = row * IMAGE_SIZE
    x2 = x1 + IMAGE_SIZE
    y2 = y1 + IMAGE_SIZE

    image = sprite_sheet.crop((x1, y1, x2, y2))
    return ImageTk.PhotoImage(image)

IMAGES = None

def charger_images():
    """Charge et retourne le dictionnaire des images"""
    global IMAGES
    IMAGES = {
        1: decouper_image(0, 0),
        2: decouper_image(1, 0),
        3: decouper_image(2, 0),
        4: decouper_image(3, 0),
        5: decouper_image(0, 1),
        6: decouper_image(1, 1,),
        7: decouper_image(2, 1),
        8: decouper_image(3, 1,),
        0: decouper_image(0, 2),
        "Bouton" : decouper_image(1, 2),
        "Mine": decouper_image(2, 2),
        "Drapeau": decouper_image(3, 2),
    }
    return IMAGES
