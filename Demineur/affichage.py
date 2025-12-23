from fonctions import *

board = tk.Tk()
board.geometry("930x520")
board.title("Démineur")
for col in range(SIZE_X):
    for row in range(SIZE_Y):
        bouton = tk.Button(board, width=3)
        bouton.grid(row = row, column = col)
