import tkinter as tk
from random import randint

SIZE_X = 30 # nombre de colonnes
SIZE_Y = 20 # nombre de lignes
NB_MINES = 100 # nombre de mines

SIZE_X = 30
SIZE_Y = 20
NB_MINES = 100

def create_board():
    """Crée la grille avec NB_MINES mines placées aléatoirement

    Parameters
    ----------
    None

    Returns
    ----------
    list
        La grille remplie de [0] (case vide) et de [1] (bombe)
    """
    mines = 0 # compteur de mines 
    tiles = [[[0] for i in range (SIZE_X)] for j in range (SIZE_Y)] # remplit la grille de [0]
 
    while mines < NB_MINES:
        randx = randint(0,SIZE_X-1)
        randy = randint(0,SIZE_Y-1)
        if tiles[randy][randx] == [0]:
            tiles[randy][randx] = [1]
            mines += 1
        
    return tiles

board = tk.Tk()
board.geometry("930x520")
board.title("Démineur")
for col in range(SIZE_X):
    for row in range(SIZE_Y):
        bouton = tk.Button(board, width=3)
        bouton.grid(row = row, column = col)
