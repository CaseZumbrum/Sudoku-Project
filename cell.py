from pygame import Rect
import pygame


class Cell(Rect):
    '''

    gui_cell extends pygame.Rect and represents a single cell of a sudoku board

    upon creation, the cell is drawn on the board

    Attributes:
        left (Int): distance from the left side of the screen
        top (Int): distance from the top of the screen
        dim (Int): dimensions of a single cell
        screen (pygame.Surface): pygame surface that the game is on
        border_size (Int): size of the borders of a cell
        set (Bool: if the cell can be changed
        value (Int): the number stored in the cell
        sketched (Int): the number sketched onto the cell
    '''
    def __init__(self,left,top,dim,screen,border_size, set = False,value = 0,sketched = None):
        super().__init__(left, top, dim, dim)
        self.dim = dim
        self.screen = screen
        self.border_size = border_size
        self.value = value
        self.set = set
        pygame.draw.rect(self.screen, (240,240,240),self)
        self.draw_border()
        self.sketched = sketched

    def draw_border(self):
        '''
        draw_border draws the border of the cell (occurs within the bounds of the cell)
        '''
        color = (150,150,150)
        pygame.draw.rect(self.screen, color, (self.left,self.top,self.border_size,self.dim))
        pygame.draw.rect(self.screen, color, (self.left, self.top, self.dim, self.border_size))
        pygame.draw.rect(self.screen, color, (self.left + self.dim- self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, color, (self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))

    def set_active(self):
        '''
        set_active activates a cell and turns its borders to be orange
        '''
        orange = (255,140,0)
        pygame.draw.rect(self.screen, orange, (self.left, self.top, 2, self.dim))
        pygame.draw.rect(self.screen, orange, (self.left, self.top, self.dim, 2))
        pygame.draw.rect(self.screen, orange,(self.left + self.dim - self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, orange,(self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))


    def clear(self):
        '''
        clear clears the interior of the cell and resets its value to be zero (set cells cannot be cleared)
        '''
        if not self.set:
            self.value = 0
            self.sketched = None
            pygame.draw.rect(self.screen, (240, 240, 240), (self.left + self.border_size,self.top + self.border_size,self.dim - 2*self.border_size, self.dim - 2*self.border_size))

    def update(self):
        '''
        update moves the sketched value to the actual value of the cell
        '''
        if self.sketched is not None:
            sketched = self.sketched
            # erase whatever is in the cell
            self.clear()
            if self.set:
                color = (50, 50, 50)
            else:
                color = (100,100,100)
            # add entered number to the active cell
            text_surface = pygame.font.Font(None, 70).render(sketched, True, color)
            text_rectangle = text_surface.get_rect(
                center=(self.dim // 2 + self.left,
                        self.dim // 2 + self.top)
            )
            self.screen.blit(text_surface, text_rectangle)

            # set the value of the active cell to the entered number
            self.value = int(sketched)

    def sketch(self,user_text):
        '''
        sketch adds a sketched value to the cell
        :param user_text: (String) number sketched into the cell
        '''

        # you can only sketch empty/not set cells
        if not self.set and self.value == 0:
            self.clear()
            # add entered number to the active cell
            text_surface = pygame.font.Font(None, 40).render(user_text, True, (100, 100, 100))
            text_rectangle = text_surface.get_rect(
                center = (self.dim // 4 + self.left,
                        self.dim // 4 + self.top)
            )
            self.screen.blit(text_surface, text_rectangle)
            self.sketched = user_text

