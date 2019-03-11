import pygame
from random import choice, randint


pygame.init()


class Game:
    # создание поля
    def __init__(self, width, height,  top = 80, left = 20, cell_size = 50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size
        
        
    def new_game(self):
        # добавляем 2 фишки
        game.add_chip() 
        game.render()
    # помещаем  2 фишки   
    
    
    def add_chip(self):
        k = 2
        while True:
            x = randint(0, width)
            y = randint(0, height)
            if self.board[y][x] == 0:
                self.board[y][x] = choice(2, 2, 2, 4)
                k -= 1
            
               
class Board(Game):
    # создание поля
    def __init__(self, width, height,  top = 80, left = 20, cell_size = 50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size
 
 
    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                left = x * self.cell_size + self.left
                top = y * self.cell_size + self.top
                size = self.cell_size
                # список цветов
                colors = {0 : (128, 128, 128),
                          2 : (255, 255, 255),
                          4 : (255, 255, 128),
                          8 : (255, 128, 0),
                          16 : (255, 0 , 128) 
                          }
                font_color = (128, 128, 128)
                pygame.draw.rect(screen,
                                 colors[self.board[y][x]],
                                 (left, top, size, size),
                                 0)
                              
                # устанавливаем шрифт
                font = pygame.font.Font('data/freesansbold.ttf', 
                                            int(self.cell_size * 0.4))
                text = font.render(str(self.board[y][x]), 1, font_color)
                # выводим текст 
                #dx - зависит от длины числа
                screen.blit(text, (x * self.cell_size +
                                   int(self.cell_size * 0.2) + self.left,
                                   y * self.cell_size +
                                   int(self.cell_size * 0.2) + self.top))
                pygame.draw.rect(screen,
                                 (0, 0, 0),
                                 (left, top, size, size),
                                 1)                  
        
        
size = width, height = 300, 240
screen = pygame.display.set_mode(size)
game = Board(4, 4, 80, 20, 50)

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        screen.fill((0, 0, 0))
        game.render()
        pygame.display.flip()
pygame.quit()