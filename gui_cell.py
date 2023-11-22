from pygame import Rect
import pygame

'''
gui_cell extends pygame.Rect and represents a single cell of a sudoku board

upon creation, the cell is drawn on the board
'''
class gui_cell(Rect):
    '''
    Attributes:
        left (Int): distance from the left side of the screen
        top (Int): distance from the top of the screen
        dim (Int): dimensions of a single cell
        screen (pygame.Surface): pygame surface that the game is on
        border_size (Int): size of the borders of a cell
        set (Bool: if the cell can be changed
        value (Int): the number stored in the cell
    '''
    def __init__(self,left,top,dim,screen,border_size, set = False):
        super().__init__(left, top, dim, dim)
        self.dim = dim
        self.screen = screen
        self.border_size = border_size
        self.value = 0
        pygame.draw.rect(self.screen, (240,240,240),self)
        self.draw_border()
        self.set = set

    '''
    draw_border draws the border of the cell (occurs within the bounds of the cell)
    '''
    def draw_border(self):
        grey = (150,150,150)
        pygame.draw.rect(self.screen, grey, (self.left,self.top,2,self.dim))
        pygame.draw.rect(self.screen, grey, (self.left, self.top, self.dim, 2))
        pygame.draw.rect(self.screen, grey, (self.left + self.dim- self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, grey, (self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))

    '''
    set_active activates a cell and turns its borders to be orange
    '''
    def set_active(self):
        orange = (255,140,0)
        pygame.draw.rect(self.screen, orange, (self.left, self.top, 2, self.dim))
        pygame.draw.rect(self.screen, orange, (self.left, self.top, self.dim, 2))
        pygame.draw.rect(self.screen, orange,(self.left + self.dim - self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, orange,(self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))

    '''
    clear clears the interior of the cell (this is purely a visual change, nothing happens to the cells value)
    '''
    def clear(self):
        pygame.draw.rect(self.screen, (240, 240, 240), (self.left + self.border_size,self.top + self.border_size,self.dim - 2*self.border_size, self.dim - 2*self.border_size))
