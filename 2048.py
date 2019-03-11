import pygame
import os
from random import randint, choice




def load_image(name, colorkey=None, ):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 


class Board:
    # создание поля
    def __init__(self, width, height,  top = 80, left = 50, cell_size = 50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.free_cell = []
        # значения по умолчанию
        self.left = left
        self.top = top
        self.cell_size = cell_size
 
                
class Game(Board):
    # создание игры
    def __init__(self, width, height,  top = 70, left = 35, cell_size = 70,):
        super().__init__(width, height, top, left, cell_size)
        #числа на карточках
        self.num = [2**i for i in range(1, 12)]
        #цвета карточек
        self.colors = {0: (0, 0, 0)}
        #цвет цифр
        self.font_colors = {0: (255, 255, 255)}
        #счет
        self.score = 0
        #количество пустых клеток
        self.empty = width * height
        
        
    
    def is_can_game(self):
        k = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    k += 1
        self.empty = k
        if k == 0:
            f = False
            y = 0
            while y < self.height and not f:
                for x in range(self.width - 1):
                    if self.board[y][x] == self.board[y][x + 1]:
                        f = True
                        break
                y +=1
                
            x = 0
            while x < self.width and not f:
                for y in range(self.height - 1):
                    if self.board[y][x] == self.board[y + 1][x]:
                        f = True
                        break
                x +=1 
        else:
            f = True
            
        return  f
    
    
    
    
        
        
    def new_game(self):
        for y in range(self.height):
            for x in range(self.width):
                self.board[y][x] = 0
        
        
        for n in self.num:
            r, g, b = randint(3, 8), randint(3, 8), randint(3, 8)
            self.colors[n] = (r * 32 - 1, g * 32 - 1,  b * 32 - 1)
        
        # добавление фишек
        self.add_chip()
        self.add_chip()


    def add_chip(self):
        self.free_cell = []
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    self.free_cell.append(y *self.height + x)

        while len(self.free_cell) > 0:
            n = randint(0, len(self.free_cell) - 1)
            n_cell = self.free_cell.pop(n)
            x = n_cell % self.width
            y = n_cell // self.height
            if self.board[y][x] == 0:
                self.board[y][x] = choice([2, 2, 2, 2, 4])
                break
        
        
    def count(self):
        summ = 0
        for y in range(self.height):
            for x in range(self.width):
                summ += self.board[y][x]
        return summ

            
    def update(self):
        #вывод названия игры
        font = pygame.font.Font('data/freesansbold.ttf', 
                                            int(self.cell_size *0.8))
        
        text = font.render("2048", 1, (128, 0, 196))
        screen.blit(text, (self.cell_size // 2 + 1,
                                       self.cell_size // 6 + 1))
        text = font.render("2048", 1, (255, 255, 255))
        screen.blit(text, (self.cell_size // 2,
                                       self.cell_size // 6))
        #вывод счета
        self.score = self.count()
        pygame.draw.rect(screen,
                         (196, 196, 196),
                         (self.cell_size // 2 + self.cell_size * 3,
                          self.cell_size // 4 + self.cell_size // 4,
                          self.cell_size * 2, 
                          self.cell_size - self.cell_size // 4), 0)
        pygame.draw.rect(screen,
                         (128, 128, 128),
                         (self.cell_size // 2 + self.cell_size * 3,
                          self.cell_size // 4 + self.cell_size // 4,
                          self.cell_size * 2, 
                          self.cell_size - self.cell_size // 4), 4)
        font = pygame.font.Font('data/freesansbold.ttf', 
                                            int(self.cell_size * 0.3))
        dx = self.cell_size // 5
        text = font.render("счёт: " + " " *(4 - len(str(self.score))) +
                           str(self.score), 1, (33, 33, 33))
        screen.blit(text, (self.cell_size // 2 + self.cell_size * 3 + dx,
                            self.cell_size // 2 + self.cell_size // 6))

        #вывод поля
        for y in range(self.height): 
            for x in range(self.width):
                left = x * self.cell_size + self.left
                top = y * self.cell_size + self.top
                size = self.cell_size
         #вывод карточек
                if 0 < self.board[y][x] < 2049:
                    color = (216, 216, 216)
                    if self.board[y][x] in self.colors:
                        color = self.colors[self.board[y][x]]
                    width = 0            
                    pygame.draw.rect(screen, color,
                                 (left + 2, top + 2,
                                  size - 4, size - 4), width)
                    font = pygame.font.Font('data/freesansbold.ttf', 
                                            int(self.cell_size * 0.4))
                    #определяем длину числа
                    l = len(str(self.board[y][x]))
                    #по длине числа определяем смещение цифры на карточке
                    dx = int((4-l) * self.cell_size // 8)
                    text = font.render(str(self.board[y][x]), 1, (0, 0, 0))
                    screen.blit(text, (x * self.cell_size + dx + self.left,
                                       y * self.cell_size +
                                       int(self.cell_size * 0.3) + self.top))
                #вывод белой границы клеток
                color = (255, 255, 255)
                width = 1            
                pygame.draw.rect(screen, color,
                                 (left, top, size, size), width)


    def key_pressedL(self, key):
        #возвращает True, если можно выполнить ход
        #сдвигает карточки влево
        #складывает одну пару одинаковых, начиная слева
        if key == 'left':
            shift = False
            for y in range(self.height):
                a = [self.board[y][i] for i in range(self.width)
                     if self.board[y][i] != 0]
                if a != self.board[y][:len(a)]:
                    shift = True 
                summ = False
                k = 0
                while k < len(a) - 1 and not summ:
                    if a[k] == a[k + 1]:
                        a[k] += a[k + 1]
                        a.pop(k + 1)
                        summ = True
                    k += 1
                
                for k in range(len(a)):
                    self.board[y][k] = a[k]
                for k in range(len(a), self.width):
                    self.board[y][k] = 0

        return  summ or shift


    def key_pressedR(self, key):
        #возвращает True, если можно выполнить ход
        #сдвигает карточки вправо
        #складывает одну пару одинаковых, начиная справа
        if key == 'right':
            shift = False
            for y in range(self.height):
                a = [self.board[y][i] for i in range(self.width - 1, -1, -1)
                     if self.board[y][i] != 0]
                if a != self.board[y][self.width - 1:self.width - len(a) + 1:-1]:
                    shift = True 
                summ = False
                k = 0
                while k < len(a) - 1 and not summ:
                    if a[k] == a[k + 1]:
                        a[k] += a[k + 1]
                        a.pop(k + 1)
                        summ = True
                    k += 1
                
                for k in range(0, self.width):
                    self.board[y][k] = 0
                for k in range(0, len(a)):
                    self.board[y][self.width - 1 - k] = a[k]

        return  summ or shift


    def key_pressedD(self, key):
        #возвращает True, если можно выполнить ход
        #сдвигает карточки вниз
        #складывает одну пару одинаковых, начиная снизу
        if key == 'down':
            shift = False
            for x in range(self.width):
                a = [self.board[i][x] for i in range(self.height - 1, -1, -1)
                     if self.board[i][x] != 0]
                b = [self.board[self.height - 1 - i][x] for i in range(len(a))]
                if a != b:
                    shift = True 
                summ = False
                k = 0
                while k < len(a) - 1 and not summ:
                    if a[k] == a[k + 1]:
                        a[k] += a[k + 1]
                        a.pop(k + 1)
                        summ = True
                    k += 1
                
                for k in range(self.height):
                    self.board[k][x] = 0
                for k in range(len(a)):
                    self.board[self.height - 1 - k][x] = a[k]
                

        return  summ or shift


    def key_pressedU(self, key):
        #возвращает True, если можно выполнить ход
        #сдвигает карточки вверх
        #складывает одну пару одинаковых, начиная сверху
        if key == 'up':
            shift = False
            for x in range(self.width):
                a = [self.board[i][x] for i in range(self.height)
                     if self.board[i][x] != 0]
                b = [self.board[i][x] for i in range(len(a))]
                if a != b:
                    shift = True 
                summ = False
                k = 0
                while k < len(a) - 1 and not summ:
                    if a[k] == a[k + 1]:
                        a[k] += a[k + 1]
                        a.pop(k + 1)
                        summ = True
                    k += 1
                
                for k in range(len(a)):
                    self.board[k][x] = a[k]
                for k in range(len(a), self.height):
                    self.board[k][x] = 0

        return  summ or shift


#кнопка новая игра
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    
    return image


class Button(pygame.sprite.Sprite):
    image = load_image("button.png")
    #image_mouse = load_image("button_.png") рисунок при наведении курсора

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite
        super().__init__(group)
        self.image = Button.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    
    def update(self, event):
        pos_x, pos_y = event.pos
        if self.rect.collidepoint(pos_x, pos_y):
            self.image = Button.image_mouse
            
            
    def click(self, event):
        pos_x, pos_y = event.pos
        if self.rect.collidepoint(pos_x, pos_y):
            board.new_game()
            
            
'''    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 


class Game_over(pygame.sprite.Sprite):
    image = load_image("images.png")
 
    def __init__(self, group):
        super().__init__(group)
        self.image = Game_over.image
        self.rect = self.image.get_rect()
        self.rect.top = -300
        self.rect.left = -300
        self.speed = 4
    def update(self):
        if self.rect.top < 0 :
            self.rect.top += 5
            self.rect.left += 5 
        else:
            self.speed = 0'''
    

#main                
pygame.init()
#значения по умолчанию n=5 w=80
n = 3 #количество столбцов
w = 120 #размер ячейки
size = width, height = w * (n + 1), w * (n + 2)
screen = pygame.display.set_mode(size)

board = Game(n, n, w + w // 2, w // 2, w)
board.new_game()

# кнопка новая игра
all_sprites = pygame.sprite.Group()
button_new = Button(all_sprites)
button_new.rect.x = w // 2 + w * 2 + 15
button_new.rect.y = w // 4

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in all_sprites:
                b.click(event)
                
        '''
        if event.type == pygame.MOUSEMOTION:
            for b in all_sprites:
                b.update(event)'''
 
 
        if event.type == pygame.KEYDOWN:
            can_game = False
            if event.key == pygame.K_LEFT:
                if board.key_pressedL('left'):
                    board.add_chip()
                    
                    
                    
            if event.key == pygame.K_RIGHT:
                if board.key_pressedR('right'):
                    board.add_chip()
                    
                    
                    
            if event.key == pygame.K_UP:
                if board.key_pressedU('up'):
                    board.add_chip()
                   
                    
                    
            if event.key == pygame.K_DOWN:
                if board.key_pressedD('down'):
                    board.add_chip()   
                    
                    
            if board.is_can_game() and board.empty == 0:
                print('Конец игры')            
        
        screen.fill((0, 0, 0))
        #if can_game == False and summ == 0:
            #game_over()          
        board.update()
        all_sprites.draw(screen)
        pygame.display.flip()

pygame.quit()

