import pygame
from cell import Cell
import sudoku_generator
import random
import time
# Global Variables
SIZE = 630  # size of board (should be a multiple of 9)
BG_COLOR = (255, 255, 255)  # background color
TEXT_COLOR = (0, 0, 0)  # default text color
BORDERSIZE = 4  # size of the borders
CELLSIZE = SIZE // 9  # dimension of single cell


def check_all_cells(cells,func):
    """
    checks if all cells in a list match with a specific function
    :param cells: list of cells
    :param func: function that takes in one parameter and returns a boolean
    :return: True if all cells return True, False otherwise
    """
    for i in range(len(cells)):
        for j in range(len(cells[i])):
            if not func(cells[i][j]):
                return False
    return True


def check_valid(cells, x, y):
    """
    checks if a single cell of the board is valid
    :param cells: list of cells
    :param x: x coordinate of the cell being checked
    :param y: y coordinate of the cell being check
    :return: True if the cell is valid, false if it is not
    """

    # get cell x y
    val = cells[x][y].value
    if val != 0:
        # compare all the x values of that cell (columns)
        for i in range(0, 9):
            if val == cells[i][y].value and i != x:
                return False  # if values match, it is not valid

        # compare all the y values of that cell (rows)
        for i in range(0, 9):
            if val == cells[x][i].value and i != y:
                return False  # if values match, it is not valid

        # BOX
        # start in top left corner (x and y division by 3)
        # nested for loops to check
        box_x = (x // 3) * 3
        box_y = (y // 3) * 3
        for i in range(box_x, box_x + 3):
            for j in range(box_y, box_y + 3):
                if val == cells[i][j].value and not (i == x and j == y):
                    return False
        return True
    return False


def check_pygame_digit(key):
    '''
    checks if a pygame key event is a number 1-9
    :param key: a pygame event.key
    :return: a boolean of if the event is a number 1-9
    '''
    return key == pygame.K_1 or key == pygame.K_2 or key == pygame.K_3 or key == pygame.K_4 or key == pygame.K_5 or key == pygame.K_6 or key == pygame.K_7 or key == pygame.K_8 or key == pygame.K_9


def generate_button(screen,text,x,y ,color = (255,255,255),font_size = 70, background_color = (0,0,0), padding = 20):
    '''
    generates a button and puts it to the screen, returns a rectangle to be used as a collision box
    :param screen: pygame screen the button is on
    :param text: text for the button
    :param x: x coordinate of the center of the button
    :param y: y coordinate of the center of the button
    :param color: color of the text in the button (Default=(255,255,255))
    :param font_size: font size of the text in the button (Default=70)
    :param background_color: background colo of the button (Default-(0,0,0))
    :param padding: padding around the text in the button (Default=20px)
    :return: rectangle representing the button
    '''
    text_surface = pygame.font.Font(None, font_size).render(text, True, color)
    button_surface = pygame.Surface((text_surface.get_size()[0] + padding, text_surface.get_size()[1] + padding))
    button_surface.fill(background_color)
    button_surface.blit(text_surface, (padding//2, padding//2))
    text_rectangle = button_surface.get_rect(
        center=(x, y)
    )
    screen.blit(button_surface, text_rectangle)
    return text_rectangle


def activate_cell(screen, cells, x, y, pastx, pasty):
    '''
    active_cell() activates a cell on the board
    :param screen: pygame screen the cell is on
    :param cells: list of cells
    :param x: x coordinate of the cell to be activated
    :param y: y coordinate of the cell to be activated
    :param pastx: x coordinate of the currently active cell
    :param pasty: y coordinate of the currently active cell
    :return: tuple containing (x coordinate of the newly active cell, y coordinate of the newly active)
    '''
    # activate current cell
    cells[x][y].set_active()
    # un-activate last chosen cell
    if pastx is not None and pasty is not None:
        cells[pastx][pasty].draw_border()
    pastx = x
    pasty = y
    # redraw borders (in case the activated cell was on a border
    draw_borders(screen)

    # return the newly active cell coordinates
    return pastx, pasty


def generate_board(difficulty):
    """
    generate board gets a board for sudoku to be played done
    :param difficulty: difficulty for the game (easy, medium, or hard)
    :return: 2D array representing sudoku game [[Int]]
    """
    if difficulty == "easy":
        board = sudoku_generator.generate_sudoku(9, 30)
    elif difficulty == "medium":
        board = sudoku_generator.generate_sudoku(9,40)
    elif difficulty == "hard":
        board = sudoku_generator.generate_sudoku(9,50)
    return board


def fill_gui_board(screen, difficulty, board=None):
    '''
    fill_gui_board fills the sudoku board with a correct game
    :param screen: pygame screen the game is on
    :param difficulty: easy, medium, or hard
    :param board: Optional ([[Int]]), unsolved sudoku board, used when resetting a board to defualt
    :return: (a generated sudoku board, a list of cells representing the board)
    '''
    if board is None:
        board = generate_board(difficulty)

    # define list of cells and add to the board
    cells = []
    for i in range(9):
        cells.append([])
        for j in range(9):
            # if the board has a number in a location, the cells gets that number and becomes set
            if board[i][j] != 0:
                cells[i].append(Cell(i * CELLSIZE, j * CELLSIZE, CELLSIZE, screen, BORDERSIZE / 2,set=True,sketched=str(board[i][j])))
                cells[i][j].update()
            # if the board has a zero in a location, the cell is a default cell
            else:
                cells[i].append(Cell(i * CELLSIZE, j * CELLSIZE, CELLSIZE, screen, BORDERSIZE / 2))
    return board,cells

def draw_info_screen(screen):
    """
    draw_info_screen draws the game explanation
    :param screen: pygame screen that is drawn on
    """
    screen.fill((255,255,255))
    generate_button(screen, "HOW TO PLAY", SIZE // 2, SIZE // 2 - 125, font_size=70)
    generate_button(screen, "1. Click on a cell (or use arrow keys) to select it", SIZE // 2, SIZE // 2 - 50, font_size=30, color=(0,0,0),background_color=(255,255,255))
    generate_button(screen, "2. Type in a number to sketch it to the cell", SIZE // 2, SIZE // 2 - 15, font_size=30, color=(0,0,0),background_color=(255,255,255))
    generate_button(screen, "3. Hit enter to lock in a cell's number", SIZE // 2, SIZE // 2 + 20, font_size=30, color=(0,0,0),background_color=(255,255,255))
    generate_button(screen, "4. Use delete to erase the value of a non-set cell", SIZE // 2, SIZE // 2 + 55, font_size=30, color=(0,0,0),background_color=(255,255,255))

    continue_button = generate_button(screen, "CONTINUE", SIZE // 2, SIZE // 2 + 200, font_size=50)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # continue button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    draw_game_start(screen)
                    return

def draw_lose_screen(screen, timer):
    """
        draws the win screen
        :param screen: pygame screen that game is on
        :param timer: time that the user took to win
        """

    screen.fill((0, 0, 0))
    generate_button(screen, "UH OH", SIZE // 2, SIZE // 2 - 125, font_size=70)
    generate_button(screen, "YOU LOST!", SIZE // 2, SIZE // 2 + 150, font_size=70)
    generate_button(screen, "Time: " + timer, SIZE // 2, SIZE // 2 + 225, font_size=70)
    return_button2 = generate_button(screen, "Main Menu", 60, SIZE // 2 + 380, font_size=30)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and return_button2.collidepoint(event.pos):
                draw_game_start(screen)
                return
        # draw the frowny face
        pygame.draw.circle(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                           (SIZE // 2 - 60, SIZE // 2), 50, 10)
        pygame.draw.circle(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                           (SIZE // 2 + 60, SIZE // 2), 50, 10)
        smileyRec = (SIZE // 2 - 28, SIZE // 2 + 50, 50, 50)
        pygame.draw.arc(screen, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), smileyRec,
                        0, 3.14, 5)

        time.sleep(.01)
        pygame.display.flip()



def draw_win_screen(screen,timer):
    """
    draws the win screen
    :param screen: pygame screen that game is on
    :param timer: time that the user took to win
    """
    screen.fill((0,0,0))
    generate_button(screen, "CONGRATULATIONS", SIZE // 2, SIZE // 2 - 125, font_size=70)
    generate_button(screen, "YOU WIN!", SIZE // 2, SIZE // 2 + 150, font_size=70)
    generate_button(screen, "Time: " + timer, SIZE // 2, SIZE // 2 + 225, font_size=70)
    return_button = generate_button(screen, "Main Menu",60 , SIZE // 2 + 380, font_size=30)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and return_button.collidepoint(event.pos):
                draw_game_start(screen)
                return
        # draw the smiley face
        pygame.draw.circle(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),(SIZE//2-60,SIZE//2),50, 10)
        pygame.draw.circle(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)),(SIZE//2+60,SIZE//2),50, 10)
        smileyRec = (SIZE//2-28 ,SIZE//2 + 50,50,50)
        pygame.draw.arc(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), smileyRec, 3.14, 0, 5 )

        time.sleep(.01)
        pygame.display.flip()




    pygame.mixer.music.load('yippee.mp3')
    pygame.mixer.music.play(-1)
    pygame.display.flip()


def draw_game_start(screen):
    '''
    draw_game_start loads the start page for sudoku
    :param screen: a pygame surface that the sudoku board is on
    '''
    # initialize title font
    start_title_font = pygame.font.Font(None,100)

    # set background
    screen.fill(BG_COLOR)

    # create the title
    title_surface = start_title_font.render("Sudoku",0,(0,0,0))
    title_rectangle = title_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 - 150)
    )
    screen.blit(title_surface, title_rectangle)

    # create the easy button
    easy_rectangle = generate_button(screen,"EASY", SIZE//2, SIZE//2)

    # create the medium button
    med_rectangle = generate_button(screen, "MEDIUM", SIZE // 2, SIZE // 2 + 100)

    # create the hard button
    hard_rectangle = generate_button(screen, "HARD", SIZE // 2, SIZE // 2 + 200)


    while True:

        for event in pygame.event.get():
            # quit on exit
            if event.type == pygame.QUIT:
                pygame.quit()

            # check if user clicked on one of the buttons, and create the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    sudoku_game(screen,"easy")
                elif med_rectangle.collidepoint(event.pos):
                    sudoku_game(screen,"medium")
                elif hard_rectangle.collidepoint(event.pos):
                    sudoku_game(screen,"hard")

        pygame.display.flip()


def draw_borders(screen):
    '''
    draw_borders draws the thick borders of the sudoku board
    
    :param screen: a pygame surface that the sudoku board is on
    '''
    dark_grey = (90,90,90)
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 - BORDERSIZE / 2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 * 2 - BORDERSIZE / 2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 - BORDERSIZE / 2, SIZE, BORDERSIZE))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 * 2 - BORDERSIZE / 2, SIZE, BORDERSIZE))


def sudoku_game(screen, difficulty):
    '''
    sudoku_game draws the sudoku grid and allows for user input to actually play the game

    :param screen: a pygame surface that the sudoku board is on
    :param difficulty: difficulty of the game (easy, medium, or hard)
    '''
    # reset screen
    screen.fill((255, 255, 255))

    # draw the borders of the game

    board,cells = fill_gui_board(screen,difficulty)
    draw_borders(screen)
    pygame.display.update()

    # create the restart button
    reset_rectangle = generate_button(screen, "Reset", SIZE // 2 - 25, SIZE + 50, font_size=50)

    # create the reset button
    restart_rectangle = generate_button(screen,"Restart", SIZE // 2 - 175, SIZE + 50, font_size=50)

    # create the exit button
    exit_rectangle = generate_button(screen, "Exit", SIZE // 2 + 100, SIZE + 50, font_size=50)

    # Create the timer
    generate_button(screen,"0", SIZE // 2 + 250, SIZE + 50, font_size=50)
    pygame.time.set_timer(pygame.USEREVENT, 100)
    seconds = 0.0

    # initialize variables

    pastx = None # stores the x coordinate of the last active cell
    pasty = None # stores the y coordinate of the last active cell
    x = None # stores the x coordinate of the currently active cell
    y = None # stores the y coordinate of the currently active cell

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():

            # quit on exit
            if event.type == pygame.QUIT:
                pygame.quit()

            # timer
            if event.type == pygame.USEREVENT:
                seconds+=.1
                generate_button(screen, str(round(seconds,1)), SIZE // 2 + 250, SIZE + 50, font_size=50)

            # user clicks on the screen
            if event.type == pygame.MOUSEBUTTONDOWN:

                # reset button
                if reset_rectangle.collidepoint(event.pos):
                    board,cells = fill_gui_board(screen,difficulty,board)
                    draw_borders(screen)
                    pastx, pasty = None, None
                    pygame.display.update()

                # restart button
                elif restart_rectangle.collidepoint(event.pos):
                    draw_game_start(screen)
                    return

                # exit button
                elif exit_rectangle.collidepoint(event.pos):
                    pygame.quit()
                    return

                # user clicks a cell (pygame.Rect(0,0,SIZE,SIZE) represents the entire space that the cells are on)
                elif pygame.Rect(0,0,SIZE,SIZE).collidepoint(event.pos):
                    # get the location where the user clicked
                    x = int((event.pos[0] - (event.pos[0] % (CELLSIZE))) / (CELLSIZE))
                    y = int((event.pos[1] - (event.pos[1] % (CELLSIZE))) / (CELLSIZE))

                    #active the new cell, unactivate the past cell, and reset user text
                    pastx, pasty = activate_cell(screen, cells, x, y, pastx, pasty)

            # key click events (can only occur if there is an active cell (x,y are not none)
            if event.type == pygame.KEYDOWN and x is not None and y is not None:

                # arrow keys
                if event.key == pygame.K_UP:
                    if y != 0:
                        y -= 1
                        pastx, pasty = activate_cell(screen, cells, x, y, pastx, pasty)

                elif event.key == pygame.K_DOWN:
                    if y != 8:
                        y += 1
                        pastx, pasty = activate_cell(screen, cells, x, y, pastx, pasty)

                elif event.key == pygame.K_LEFT:
                    if x != 0:
                        x -= 1
                        pastx, pasty = activate_cell(screen, cells, x, y, pastx, pasty)

                elif event.key == pygame.K_RIGHT:
                    if x != 8:
                        x += 1
                        pastx, pasty = activate_cell(screen, cells, x, y, pastx, pasty)

                # if a number key is hit, sketch the entered value to the active cell
                elif check_pygame_digit(event.key):
                        cells[x][y].sketch(event.unicode)

                # enter is clicked, update the currently active cell
                elif event.key ==pygame.K_RETURN:
                    cells[x][y].update()

                # if enter is clicked, clear the active cell
                elif event.key == pygame.K_BACKSPACE:
                    cells[x][y].clear()

                # check if the board has been filled (there are no values of 0 left)
                clear = check_all_cells(cells, lambda x: x.value != 0)

                # if the board is cleared, check if there is a win
                if clear:
                    # checks each cell to see if it follows the rules of sudoku
                    won = True
                    for i in range(9):
                        for j in range(9):
                            if not check_valid(cells,i,j):
                                won = False

                    if won:
                        draw_win_screen(screen,str(round(seconds,1)))
                        return
                    else:
                        draw_lose_screen(screen,str(round(seconds,1)))
                        return


            # update display
            pygame.display.flip()
            clock.tick(60)






if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SIZE, SIZE+100))
    pygame.display.set_caption("sudoku")
    draw_info_screen(screen)
