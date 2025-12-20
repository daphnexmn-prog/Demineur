import tkinter as tk
from random import randint

board = tk.Tk()
board.geometry("930x520")

SIZE_X = 30
SIZE_Y = 20
NB_MINES = 100



def create_board():
    mines=0
    tiles=[[[0] for i in range (SIZE_X)] for j in range (SIZE_Y)]
    for n in range (NB_MINES):
        while mines<NB_MINES:
            randx=randint(0,SIZE_X-1)
            randy=randint(0,SIZE_Y-1)
            if tiles[randy][randx]==[0]:
                tiles[randy][randx]=[1]
                mines+=1
    return tiles


for col in range(SIZE_X):
    for row in range(SIZE_Y):
        bouton = tk.Button(board, width=3)
        bouton.grid(row = row, column = col)

