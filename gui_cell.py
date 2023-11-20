from pygame import Rect
import pygame
class gui_cell(Rect):
    def __init__(self,left,top,size,screen,border_size):
        super().__init__(left, top, size, size)
        self.dim = size
        self.screen = screen
        self.border_size = border_size
        pygame.draw.rect(self.screen, (240,240,240),self)
        self.draw_border()
        self.value = 0

    def draw_border(self):
        grey = (150,150,150)
        pygame.draw.rect(self.screen, grey, (self.left,self.top,2,self.dim))
        pygame.draw.rect(self.screen, grey, (self.left, self.top, self.dim, 2))
        pygame.draw.rect(self.screen, grey, (self.left + self.dim- self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, grey, (self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))

    def set_active(self):
        orange = (255,140,0)
        pygame.draw.rect(self.screen, orange, (self.left, self.top, 2, self.dim))
        pygame.draw.rect(self.screen, orange, (self.left, self.top, self.dim, 2))
        pygame.draw.rect(self.screen, orange,(self.left + self.dim - self.border_size, self.top, self.border_size, self.dim))
        pygame.draw.rect(self.screen, orange,(self.left, self.top + self.dim - self.border_size, self.dim, self.border_size))

    def clear(self):
        pygame.draw.rect(self.screen, (240, 240, 240), (self.left + self.border_size,self.top + self.border_size,self.dim - 2*self.border_size, self.dim - 2*self.border_size))
