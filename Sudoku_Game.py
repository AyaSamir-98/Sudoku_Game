import pygame
import time
from sudoku import Sudoku
import math
import random

## Tricks: exit_window when click continue, class button, dimensions##
# puzzle is given by n^2 x n^2. So, by using puzzle = Sudoku(2), you are creating a 6x6 Sudoku puzzle,
puzzle = Sudoku(2)
pygame.font.init()

# Set the window dimensions
WINDOW_SIZE = (650, 650)
Message_window=(450,450)
# Set the font and size for displaying the puzzle
FONT_SIZE = 40
font = pygame.font.SysFont('Comic Sans Ms', 35)
message_font=pygame.font.SysFont('Comic Sans Ms',20)
# Set the colors for the puzzle
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Calculate the dimensions for each cell of the puzzle
CELL_SIZE = int(WINDOW_SIZE[0] / puzzle.size)
CELL_PADDING = 1

# Initialize pygame
pygame.init()

# Set the title of the window
pygame.display.set_caption("Sudoku")

# Create a new window
screen = pygame.display.set_mode(WINDOW_SIZE)
screen.fill(WHITE)

#exit/continue screen setup
exit_img=pygame.image.load('Exit.jpg').convert_alpha()
continue_img=pygame.image.load('Continue.jpg').convert_alpha()
playAgain_img=pygame.image.load('playAgain.png').convert_alpha()
   
#size for exit window 
exit_window_size = (450, 250)



#button class
class button():
    def __init__(self, x, y, image, scale):
        self.exit_window_size = (450, 250)
        self.exit_window = pygame.display.set_mode(self.exit_window_size)
        self.exit_window.fill(WHITE)

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.message_displayed = False


    def draw(self,message):
        self.exit_window.blit(self.image, (self.rect.x, self.rect.y))
        if not self.message_displayed:
            if int(message)==0:
                return
            elif int(message)==1:
                font = pygame.font.SysFont(None, 35)
                text = font.render("Exit the game?", True, BLACK)
                text_rect = text.get_rect(center=(self.exit_window_size[0]//2, self.exit_window_size[1]//2 - 40))
                self.exit_window.blit(text, text_rect)
                self.message_displayed = True
                
            elif int(message)==2:
                font = pygame.font.SysFont(None, 35)
                text = font.render("Congratulations, passed!", True, BLACK)
                text_rect = text.get_rect(center=(self.exit_window_size[0]//2, self.exit_window_size[1]//2 - 40))
                self.exit_window.blit(text, text_rect)
                self.message_displayed = True

            
    def exit(self):
        pygame.quit()
                     
        
    
def return_to_game():
    global continue_game
    continue_game = True
    main_screen_size = (650, 650)
    main_screen=pygame.display.set_mode(main_screen_size)
    main_screen.fill(WHITE)
    
        
    


def main():
    continue_game=True
    while continue_game:
                    
        # Handle events
        for event in pygame.event.get():
            #when click on exit button in main screen display exit/continue screen
            if event.type == pygame.QUIT:
                #message for exit windoe
                display_exit_window=True
                #create button instances
                exit_button=button(50,100,exit_img,0.5)
                continue_button=button(250,100,continue_img,0.5) 
                exit_button.draw(1)
                continue_button.draw(1)
                pygame.display.update()
                run =True
                while run:
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            return
                        
                        elif event.type== pygame.MOUSEBUTTONDOWN:
                            #this mouse var should be inside the loop to allow button functions to work
                            mouse_pos=pygame.mouse.get_pos() 
                            if exit_button.rect.collidepoint(mouse_pos):
                                pygame.quit()
                                return

                            elif continue_button.rect.collidepoint(mouse_pos):
                                if is_full():
                                    main()
                                else:    
                                    run = False
                                    return_to_game()
                               
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert_value(pos)
        
                
        # Display each cell of the puzzle
        for i in range(puzzle.size):
            for j in range(puzzle.size):
                # Get the value of the cell
                value = puzzle.board[i][j]
                # Calculate the position of the cell 
                x = j * CELL_SIZE + CELL_PADDING
                y = i * CELL_SIZE + CELL_PADDING
                if (i % 2 == 0 and j % 2 == 0):
                    # Draw bold lines between each group of cells  
                    cell = pygame.Rect(x, y, CELL_SIZE * 6, CELL_SIZE * 6)
                    pygame.draw.rect(screen, BLACK, cell, 4)
                else:
                    # Draw the cell
                    cell = pygame.Rect(x, y, CELL_SIZE * 2, CELL_SIZE * 2)
                    pygame.draw.rect(screen, BLACK, cell, CELL_PADDING)
                
                # Display the value of the cell
                if value is not None:
                    text = font.render(str(value), True, BLUE)
                    #getting the center point of the cell rectangle by adding half of the cell width and height to the x and y position respectively
                    text_rect = text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2))
                    #bilt takes arguments: the required text and its position
                    screen.blit(text, text_rect)
        if is_full():
            
            exit_button = button(50, 100, exit_img, 0.5)
            playAgain = button(250, 100, playAgain_img, 0.5)
            exit_button.draw(0)
            playAgain.draw(2)
            for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            return
                        
                        elif event.type== pygame.MOUSEBUTTONDOWN:
                            #this mouse var should be inside the loop to allow button functions to work
                            mouse_pos=pygame.mouse.get_pos() 
                            if exit_button.rect.collidepoint(mouse_pos):
                                pygame.quit()
                                return

                            elif playAgain.rect.collidepoint(mouse_pos):
                                if is_full():
                                   play_Again() 
                                
                               
            pygame.display.update() 
            
            
        # Update the screen
        pygame.display.update()

def play_Again():
    global puzzle
   
    WINDOW_SIZE = (650, 650)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill(WHITE)
    
    # Generate a new Sudoku puzzle
    grid_range = [3, 4, 6]
    random_number = random.choice(grid_range)
    puzzle = Sudoku(random_number)
    CELL_SIZE = int(WINDOW_SIZE[0] / puzzle.size)

    # Calculate the size of each cell in the puzzle
   
    if random_number in [3, 4, 6]:
        
        CELL_PADDING=2
        font= pygame.font.SysFont('Comic Sans Ms', 25)
    else:
           
        CELL_PADDING=3       
        font= pygame.font.SysFont('Comic Sans Ms', 8)
    # Display each cell of the puzzle
    
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            # Get the value of the cell
            value = puzzle.board[i][j]

            # Calculate the position of the cell 
            x = j * CELL_SIZE + CELL_PADDING
            y = i * CELL_SIZE + CELL_PADDING

          
            cell = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, cell, CELL_PADDING)

            # Display the value of the cell
            if value is not None:
                text = font.render(str(value), True, BLUE)
                text_rect = text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2))
                screen.blit(text, text_rect)

    pygame.display.update()


def insert_value(pos):
    global puzzle, screen
    KEY_VALUES = {
    pygame.K_0: 0,
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9
                   }


    # Calculate the cell coordinates based on the mouse position
    # Dividing pos[1] by CELL_SIZE gives the row number of the cell clicked on (i),
    # while dividing pos[0] by CELL_SIZE gives the column number of the cell clicked on (j).
    i = pos[1] // CELL_SIZE
    j = pos[0] // CELL_SIZE
    
    # Get the value of the cell
    value = puzzle.board[i][j]
    
    if value is None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        # If the user inputs 0, clear the cell
                        puzzle.board[i][j] = None
                        x = j * CELL_SIZE + CELL_PADDING
                        y = i * CELL_SIZE + CELL_PADDING
                        pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE - CELL_PADDING, CELL_SIZE - CELL_PADDING))
                        pygame.display.update()
                        return
                    elif event.key in KEY_VALUES:
                        value = possible(i, j, KEY_VALUES[event.key])
                        if value is not False:
                            puzzle.board[i][j] = value
                            x = j * CELL_SIZE + CELL_PADDING
                            y = i * CELL_SIZE + CELL_PADDING
                            text = font.render(str(value), True, BLUE)
                            text_rect = text.get_rect(center=(x + CELL_SIZE / 2, y + CELL_SIZE / 2))
                            screen.blit(text, text_rect)
                            pygame.display.update()
                            return

def  is_full ():
    
    for i in range(puzzle.size):
        for j in range(puzzle.size):
            x = j * CELL_SIZE + CELL_PADDING
            y = i * CELL_SIZE + CELL_PADDING
            if puzzle.board[i][j] == None: #if any cell not filled 
                return False
    return True
               

    
    
#display text n window in bothe situations win or loss
#when click exit ask first &display window
    
def possible (y,x,n):
    for i in range (puzzle.size):
         if puzzle.board[y][i]==n:
             return False #if number is in the row sdo nothing and don't write number 
    for j in range (puzzle.size):
        if puzzle.board[j][x]==n:
            return False
    x0=(x//2)*2
    y0=(y//2)*2
    for i in range (2): # check the big rectangle 3*3
        for j in range (2):
            if puzzle.board[y0+i][x0+j]==n:
                return False
    return n
main()