import pygame
from gui_cell import gui_cell

# Global Variables
SIZE = 630 # size of board (should be a multiple of 90
BG_COLOR = (255,255,255) # background color
TEXT_COLOR = (0,0,0) # default text color
BORDERSIZE = 4 # size of the borders
CELLSIZE = SIZE/9 # dimension of single cell


'''
test function REMOVE LATER
'''
def generate_board(difficulty):
    if difficulty == "easy":
        board = [[1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    elif difficulty == "medium":
        board = [[2,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    elif difficulty == "hard":
        board = [[3, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return board

'''
fills gui board with sudoku data
'''
def fill_gui_board(screen,cells,difficulty):
    board = generate_board(difficulty)
    # add entered number to the active cell
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text_surface = pygame.font.Font(None, 70).render(str(board[i][j]), True, (50, 50, 50))
                text_rectangle = text_surface.get_rect(
                    center=(
                    CELLSIZE // 2 + cells[i][j].left, CELLSIZE // 2 + cells[i][j].top)
                )
                screen.blit(text_surface, text_rectangle)

                # set the value of the active cell to the entered number
                cells[i][j].value = board[i][j]
                cells[i][j].set = True

'''
draw_game_start loads the start page for sudoku
Parameters:
    screen: a pygame surface that the sudoku board is on
'''
def draw_game_start(screen):
    # initialize title font
    start_title_font = pygame.font.Font(None,100)
    button_font = pygame.font.Font(None,70)

    # set background
    screen.fill(BG_COLOR)

    # create the title
    title_surface = start_title_font.render("Sudoku",0,(0,0,0))
    title_rectangle = title_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 - 150)
    )
    screen.blit(title_surface, title_rectangle)

    # create the easy button
    easy_text = button_font.render("EASY",0, (255,255,255))
    easy_surface = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surface.fill((0, 0, 0))
    easy_surface.blit(easy_text, (10, 10))
    easy_rectangle = easy_surface.get_rect(
        center=(SIZE // 2, SIZE // 2)
    )
    screen.blit(easy_surface, easy_rectangle)

    # create the medium button
    med_text = button_font.render("MEDIUM", 0, (255, 255, 255))
    med_surface = pygame.Surface((med_text.get_size()[0] + 20, med_text.get_size()[1] + 20))
    med_surface.fill((0, 0, 0))
    med_surface.blit(med_text, (10, 10))
    med_rectangle = med_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 + 100)
    )
    screen.blit(med_surface, med_rectangle)

    # create the hard button
    hard_text = button_font.render("HARD", 0, (255, 255, 255))
    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill((0, 0, 0))
    hard_surface.blit(hard_text, (10, 10))
    hard_rectangle = hard_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 + 200)
    )
    screen.blit(hard_surface, hard_rectangle)


    while True:

        for event in pygame.event.get():
            # quit on exit
            if event.type == pygame.QUIT:
                pygame.quit()

            # check if user clicked on one of the buttons, and create the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    print("Easy")
                    sudoku_game(screen,"easy")
                elif med_rectangle.collidepoint(event.pos):
                    print("Medium")
                    sudoku_game(screen,"medium")
                elif hard_rectangle.collidepoint(event.pos):
                    print("Hard")
                    sudoku_game(screen,"hard")

        pygame.display.flip()


'''
draw_borders draws the thick borders of the sudoku board

Parameters:
    screen: a pygame surface that the sudoku board is on
'''
def draw_borders(screen):
    dark_grey = (90,90,90)
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 - BORDERSIZE / 2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 * 2 - BORDERSIZE / 2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 - BORDERSIZE / 2, SIZE, BORDERSIZE))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 * 2 - BORDERSIZE / 2, SIZE, BORDERSIZE))


'''
sudoku_game draws the sudoku grid and allows for user input

Parameters:
    screen: a pygame surface that the sudoku board is on
'''
def sudoku_game(screen,difficulty):
    # reset screen
    screen.fill((255, 255, 255))

    # define list of cells and add to the board
    cells = []
    for i in range(9):
        cells.append([])
        for j in range(9):
            cells[i].append(gui_cell(i * CELLSIZE, j * CELLSIZE, CELLSIZE, screen, BORDERSIZE/2))

    # draw the borders of the game
    draw_borders(screen)
    fill_gui_board(screen,cells,difficulty)
    pygame.display.update()

    # initialize variables
    pastx = 0
    pasty = 0
    user_text = None
    clicked_xloc = None
    clicked_yloc = None

    while True:
        for event in pygame.event.get():

            # quit on exit
            if event.type == pygame.QUIT:
                pygame.quit()

            # user clicks a cell
            if event.type == pygame.MOUSEBUTTONDOWN:

                # get the location where the user clicked
                clicked_xloc = int((event.pos[0] - (event.pos[0] % (CELLSIZE))) / (CELLSIZE))
                clicked_yloc = int((event.pos[1] - (event.pos[1] % (CELLSIZE))) / (CELLSIZE))

                # activate current cell
                cells[clicked_xloc][clicked_yloc].set_active()
                # un-activate last chosen cell
                cells[pastx][pasty].draw_border()
                pastx = clicked_xloc
                pasty = clicked_yloc
                # redraw borders (in case the activated cell was on a border
                draw_borders(screen)

                # if a new box is chosen, you have to reset user text
                user_text = None

            if event.type == pygame.KEYDOWN:

                # arrow keys
                if event.key == pygame.K_UP and clicked_yloc is not None:
                    clicked_yloc -= 1
                    cells[clicked_xloc][clicked_yloc].set_active()
                    cells[pastx][pasty].draw_border()
                    pastx = clicked_xloc
                    pasty = clicked_yloc
                    draw_borders(screen)

                    user_text = None
                elif event.key == pygame.K_DOWN and clicked_yloc is not None:
                    clicked_yloc += 1
                    cells[clicked_xloc][clicked_yloc].set_active()
                    cells[pastx][pasty].draw_border()
                    pastx = clicked_xloc
                    pasty = clicked_yloc
                    draw_borders(screen)

                    user_text = None
                elif event.key == pygame.K_LEFT and clicked_xloc is not None:
                    clicked_xloc -= 1
                    cells[clicked_xloc][clicked_yloc].set_active()
                    cells[pastx][pasty].draw_border()
                    pastx = clicked_xloc
                    pasty = clicked_yloc
                    draw_borders(screen)

                    user_text = None
                elif event.key == pygame.K_RIGHT and clicked_xloc is not None:
                    clicked_xloc += 1
                    cells[clicked_xloc][clicked_yloc].set_active()
                    cells[pastx][pasty].draw_border()
                    pastx = clicked_xloc
                    pasty = clicked_yloc
                    draw_borders(screen)

                    user_text = None

                # all number keys
                elif event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                    user_text = event.unicode

            # if a number has been entered and there is a currently active cell
            if user_text is not None and clicked_yloc is not None and clicked_xloc is not None and not cells[clicked_xloc][clicked_yloc].set:
                # erase whatever is in the cell
                cells[clicked_xloc][clicked_yloc].clear()

                # add entered number to the active cell
                text_surface = pygame.font.Font(None,70).render(user_text, True, (50, 50, 50))
                text_rectangle = text_surface.get_rect(
                    center=(CELLSIZE // 2 + cells[clicked_xloc][clicked_yloc].left, CELLSIZE // 2 + cells[clicked_xloc][clicked_yloc].top)
                )
                screen.blit(text_surface, text_rectangle)

                # set the value of the active cell to the entered number
                cells[clicked_xloc][clicked_yloc].value = int(user_text)

            # update display
            pygame.display.flip()



if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("sudoku")
    draw_game_start(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()