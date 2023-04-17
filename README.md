# Sudoku_Game
 Sudoku game using python 
 
 This is a sumpile form of Sudoku Game in python, that allows user to solve firstly a simple level
and after passing this level, asks user if want to play again it upgrades the level.

 Class Grid :
 responsible of drawing the board of the game, and contains the following functions:
#return_to_game: returns to the current playing game when clxick continue buttom 
#is_Full: checks weather the current board is full or not
#insert_value: insert the input values from users into cells
#possible: check the possibility level of the value as the value (number) shouldn't exist at the same row, column, and diagonal.

class button:
responsible for drawin the screen of exit and continue button  and contains the exit fucntion for exit button

main function:
iniate and display the game, call functions, objects and their corresponding functions.
