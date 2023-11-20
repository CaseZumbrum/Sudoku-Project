import pygame
from gui_cell import gui_cell
SIZE = 540
BG_COLOR = (255,255,255)
TEXT_COLOR = (0,0,0)
BORDERSIZE = 6
CELLSIZE = (SIZE - BORDERSIZE*9)/9
CELLSIZE = SIZE/9

def draw_game_start(screen):
    # initialize title font
    start_title_font = pygame.font.Font(None,100)
    button_font = pygame.font.Font(None,70)

    # set background
    screen.fill(BG_COLOR)

    # initialize and draw title
    title_surface = start_title_font.render("Sudoku",0,(0,0,0))
    title_rectangle = title_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 - 150)
    )
    screen.blit(title_surface, title_rectangle)

    # initialize buttons
    easy_text = button_font.render("EASY",0, (255,255,255))
    med_text = button_font.render("MEDIUM", 0, (255, 255, 255))
    hard_text = button_font.render("HARD", 0, (255, 255, 255))

    # intialize button background color and text
    easy_surface = pygame.Surface((easy_text.get_size()[0]+20, easy_text.get_size()[1]+20))
    easy_surface.fill((0,0,0))
    easy_surface.blit(easy_text, (10,10))

    med_surface = pygame.Surface((med_text.get_size()[0] + 20, med_text.get_size()[1] + 20))
    med_surface.fill((0, 0, 0))
    med_surface.blit(med_text, (10, 10))

    hard_surface = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surface.fill((0, 0, 0))
    hard_surface.blit(hard_text, (10, 10))

    # initialize button rectangle
    easy_rectangle = easy_surface.get_rect(
        center=(SIZE//2,SIZE//2)
    )

    med_rectangle = med_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 + 100)
    )
    hard_rectangle = hard_surface.get_rect(
        center=(SIZE // 2, SIZE // 2 + 200)
    )

    screen.blit(easy_surface,easy_rectangle)
    screen.blit(med_surface,med_rectangle)
    screen.blit(hard_surface, hard_rectangle)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rectangle.collidepoint(event.pos):
                    print("Easy")
                    draw_grid(screen)
                elif med_rectangle.collidepoint(event.pos):
                    print("Medium")
                    draw_grid(screen)
                elif hard_rectangle.collidepoint(event.pos):
                    print("Hard")
                    draw_grid(screen)
        pygame.display.flip()



def draw_borders(screen):
    dark_grey = (90,90,90)
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 - 4 / 2, 0, 4, SIZE))
    pygame.draw.rect(screen, dark_grey, (SIZE // 3 * 2 - 4 / 2, 0, 4, SIZE))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 - 4 / 2, SIZE, 4))
    pygame.draw.rect(screen, dark_grey, (0, SIZE // 3 * 2 - 4 / 2, SIZE, 4))


def draw_grid(screen):
    screen.fill((255, 255, 255))
    cells = []
    for i in range(9):
        cells.append([])
        for j in range(9):
            cells[i].append(gui_cell(i * CELLSIZE, j * CELLSIZE, CELLSIZE, screen, 2))

    draw_borders(screen)

    pygame.display.update()

    pastx = 0
    pasty = 0
    user_text = None
    clicked_xloc = None
    clicked_yloc = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                '''
            if event.type == pygame.MOUSEMOTION:
                xloc = int((event.pos[0]-(event.pos[0]%(CELLSIZE)))/(CELLSIZE))
                yloc = int((event.pos[1]-(event.pos[1]%(CELLSIZE)))/(CELLSIZE))
                cells[pastx][pasty].draw_border()
                cells[xloc][yloc].set_active()
                pastx = xloc
                pasty = yloc
                draw_borders(screen)
                '''

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_xloc = int((event.pos[0] - (event.pos[0] % (CELLSIZE))) / (CELLSIZE))
                clicked_yloc = int((event.pos[1] - (event.pos[1] % (CELLSIZE))) / (CELLSIZE))
                cells[clicked_xloc][clicked_yloc].set_active()
                cells[pastx][pasty].draw_border()
                pastx = clicked_xloc
                pasty = clicked_yloc
                draw_borders(screen)

                user_text = None
                print(clicked_xloc, clicked_yloc)

            if event.type == pygame.KEYDOWN:

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
                # Check for backspace
                elif event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    # Unicode standard is used for string
                # formation
                else:
                    user_text = event.unicode

            if user_text is not None and clicked_yloc is not None and clicked_xloc is not None and cells[clicked_xloc][clicked_yloc].value == 0:

                text_surface = pygame.font.Font(None,70).render(user_text, True, (50, 50, 50))

                text_rectangle = text_surface.get_rect(
                    center=(CELLSIZE // 2 + cells[clicked_xloc][clicked_yloc].left, CELLSIZE // 2 + cells[clicked_xloc][clicked_yloc].top)
                )

                cells[clicked_xloc][clicked_yloc].value = int(user_text)

                screen.blit(text_surface, text_rectangle)

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