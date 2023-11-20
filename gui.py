import pygame

SIZE = 540
BG_COLOR = (255,255,255)
TEXT_COLOR = (0,0,0)
BORDERSIZE = 6
CELLSIZE = (SIZE - BORDERSIZE*9)/9
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



def draw_grid(screen):
    SIZE2 = (SIZE) // 3
    screen.fill((255, 255, 255))
    for i in range(0, 3):
        pygame.draw.rect(screen, (100, 100, 100), (i * SIZE2 + SIZE2 // 3 - BORDERSIZE/2, BORDERSIZE/2, BORDERSIZE, SIZE))
        pygame.draw.rect(screen, (100, 100, 100), (i * SIZE2 + SIZE2 // 3 * 2 - BORDERSIZE/2, BORDERSIZE/2, BORDERSIZE, SIZE))
        pygame.draw.rect(screen, (100, 100, 100), (3, i * SIZE2 + SIZE2 // 3 - BORDERSIZE/2, SIZE, BORDERSIZE))
        pygame.draw.rect(screen, (100, 100, 100), (3, i * SIZE2 + SIZE2 // 3 * 2 - BORDERSIZE/2, SIZE, BORDERSIZE))

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, BORDERSIZE/2, SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (SIZE // 3 - BORDERSIZE/2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (SIZE // 3 * 2 - BORDERSIZE/2, 0, BORDERSIZE, SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (SIZE - BORDERSIZE/2, 0, BORDERSIZE/2, SIZE))

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, SIZE, BORDERSIZE/2))
    pygame.draw.rect(screen, (0, 0, 0), (0, SIZE // 3 - BORDERSIZE/2, SIZE, BORDERSIZE))
    pygame.draw.rect(screen, (0, 0, 0), (0, SIZE // 3 * 2 - BORDERSIZE/2, SIZE, BORDERSIZE))
    pygame.draw.rect(screen, (0, 0, 0), (0, SIZE - BORDERSIZE/2, SIZE, BORDERSIZE/2))

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                xloc = (event.pos[0]-(event.pos[0]%(CELLSIZE+BORDERSIZE)))/(CELLSIZE+BORDERSIZE)
                yloc = (event.pos[1]-(event.pos[1]%(CELLSIZE+BORDERSIZE)))/(CELLSIZE+BORDERSIZE)
                print(xloc,yloc)



if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("sudoku")
    draw_game_start(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()