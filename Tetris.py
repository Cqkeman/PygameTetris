import pygame
import random

pygame.font.init()

#Global vars
S_Height = 800
S_Width = 900
Play_Width = 250
Play_Height = 500
Block_Size = 25
Col_Count = 10
Row_Count = 20

Top_Left_X = (S_Width - Play_Width) // 2
Top_Left_Y = S_Height - Play_Height - 10


#shape config
S = [['.....',
    '.....',
    '..00.',
    '.00..',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....',],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.....',
    '.0...',
    '.000.',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '.....',
    '...0.',
    '.000.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]



shape_list = [S,Z,I,O,J,L,T]
temp_shape_list = shape_list
temp3 = 0
lines = 0
level = 0
#defining a list of the objects
shape_colors = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(255,165,0),(0,0,200), (221,160,221)]

class Piece(object):

    def __init__(self, column, row, shape):
        self.col = column

        self.row = row

        self.shape = shape

        self.color = shape_colors[temp3]

        self.rotation = 0

        self.title_pos = None

    def get_piece_title_pos(self):
        positions = []

        shape_list = self.shape[self.rotation % len(self.shape)]


        for row_index, line in enumerate(shape_list):
            row = list(line)
            for col_index, column in enumerate(row):
                if column == '0':
                    positions.append((self.row + row_index, self.col + col_index))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 4, pos[1] - 2)
        

        self.title_pos = positions

        return self.title_pos
    

    def is_valid_pos(self):
        self.get_piece_title_pos()
        accepted_positions = [[(i, j) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        #nested list comprehention to flatten a given 2d matrix
        accepted_positions = [j for sub in accepted_positions for j in sub]

        for pos in self.get_piece_title_pos():
            if pos not in accepted_positions:
                if pos [0] > -1:
                    return False
        return True

    def draw_current_piece(self, surface):
        if self.title_pos is not None:
            for pos in self.title_pos:
                pygame.draw.rect(surface, self.color, (Top_Left_X + pos[1]*Block_Size, Top_Left_Y + pos[0]*Block_Size, Block_Size, Block_Size), 0)
                #stuff is supposed to be here lmao

    def draw_next_piece(self, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('next Shape', 1, (255,255,255))
        shape_list = self.shape[self.rotation % len(self.shape)]

        sx = Top_Left_X + Play_Width + 50
        sy = Top_Left_Y + Play_Height/2 - 100

        for row_index, line in enumerate(shape_list):
            row = list(line)
            for col_index, column in enumerate(row):
                if column == '0':
                    #draw filled rect
                    pygame.draw.rect(surface, self.color, (sx + col_index*Block_Size, sy + row_index*Block_Size, Block_Size, Block_Size), 0)
                    #stuff here too
        
        surface.blit(label, (sx + 10, sy - 30))
    
        


def remake_next_piece_list(num):
    global temp_shape_list,shape_list, S, Z, I, O, J, L, T

    temp_shape_list.remove(num)
    if len(temp_shape_list) < 1:
        shape_list = [S ,Z, I, O, J, L, T]
        temp_shape_list = shape_list
    

    
    
    
    # colours are fucked because it reads colours in an order of when picked


def make_colour(num):
    global shape_list, temp3, S, Z, I, O, J, L, T
    shape_list = [S,Z,I,O,J,L,T]
    temp3 = shape_list.index(num)



def check_lost():
    #that emans to check if the player has lost the game
    for i in range(Col_Count):
        if grid[0][i] !=(0,0,0):
            return True
    return False
    

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (Top_Left_X + Play_Width/2 - (label.get_width() / 2), Top_Left_Y + Play_Height/2 - label.get_height()/2))
    #stuff go here

def draw_score(text, size, color, surface):
    global score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score {}'.format(score), 1, (255,255,255))
    sx = Top_Left_X - label.get_width() - 100
    sy = Top_Left_Y + Play_Height/2 - 100
    surface.blit(label, (sx + 10, sy - 30))


def draw_grid_line(surface, row, col):
    sx = Top_Left_X
    sy = Top_Left_Y
    #draw horizontal line
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*Block_Size), (sx + Play_Width, sy + i * Block_Size))
        #draw vertical lines
        #bruh
    for j in range(col):
        pygame.draw.line(surface, (128,128,128), (sx + j * Block_Size, sy), (sx + j * Block_Size, sy + Play_Height))
        #yes


def clear_rows():
    global score, lines, level

    inc = 0
    row_index = Row_Count - 1
    while row_index > -1:
        clear = True
        for col_index in range(Col_Count):
            if grid[row_index][col_index] ==(0, 0, 0):
                clear = False
                break
        
        if clear:
            inc += 1 
            del grid[row_index]
            grid.insert(0, [])
            for i in range(Col_Count):
                grid[0].insert(i, (0, 0, 0))
        else:
            row_index -= 1
        
        if row_index == inc:
            #if clearing two or more lines
            score += (inc **2) * 10
            break


def draw_existing_tiles(surface):
    surface.fill((0,0,0))
    #tetris title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))

    #blit the text
    surface.blit(label, (Top_Left_X + Play_Width / 2 - (label.get_width() / 2), 30))

    #draw each small tile using the rgb values assigned
    for row_index in range(len(grid)):
        for col_index in range(len(grid[row_index])):
            if grid[row_index][col_index ] != (0,0,0):
                pygame.draw.rect(surface, grid[row_index][col_index], (Top_Left_X + col_index * Block_Size, Top_Left_Y + row_index * Block_Size, Block_Size, Block_Size), 0)
                #e
                #e


def main():
    global grid
    global score
    #20 rows, 20 cols grid
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    score = 0
    b_accelerate = False
    change_piece = False
    run = True

    temp1 = random.choice(temp_shape_list)
    make_colour(temp1)
    current_piece = Piece(5, 0, temp1)
    remake_next_piece_list(temp1)
    temp1 = random.choice(temp_shape_list)
    make_colour(temp1)
    next_piece = Piece(5, 0, temp1)
    remake_next_piece_list(temp1)
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27
        fall_time += clock.get_rawtime()
        clock.tick()

        #piece falling code
        if fall_time/1000 >= fall_speed or b_accelerate:
            fall_time = 0
            current_piece.row += 1
            b_accelerate = False
            if not (current_piece.is_valid_pos()) and current_piece.row > -1:
                current_piece.row -= 1
                change_piece = True

        #handling event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.col -= 1
                    if not current_piece.is_valid_pos():
                        current_piece.col += 1
                
                elif event.key == pygame.K_RIGHT:
                    current_piece.col += 1
                    if not current_piece.is_valid_pos():
                        current_piece.col -= 1
                
                elif event.key == pygame.K_UP:
                    #rotate shape
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not current_piece.is_valid_pos():
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                
                if event.key == pygame.K_DOWN or event.key == pygame.KSCAN_SPACE:
                    #move shape down
                    b_accelerate = True
                    current_piece.row += 1
                    if not current_piece.is_valid_pos():
                        current_piece.row -= 1
                
                if event.key == pygame.K_SPACE:
                    while current_piece.is_valid_pos():
                        current_piece.row += 1
                    current_piece.row -= 1
        
        current_piece.get_piece_title_pos()
        draw_existing_tiles(display_surface)
        current_piece.draw_current_piece(display_surface)

        # if piece hit ground, change piece == true
        if change_piece:
            for item in current_piece.title_pos:
                row, column = item
                if row > -1:
                    grid[row][column] = current_piece.color
            
            current_piece = next_piece
            temp1 = random.choice(temp_shape_list)
            make_colour(temp1)
            next_piece = Piece(5, 0, temp1)
            remake_next_piece_list(temp1)
            change_piece = False
            clear_rows()

        next_piece.draw_next_piece(display_surface)
        draw_grid_line(display_surface, 20, 10)

        pygame.draw.rect(display_surface, (255, 0, 0), (Top_Left_X, Top_Left_Y, Play_Width, Play_Height), 5)
        #code lmao
        #draw score
        draw_score("Score: {}".format(score), 30, (255,255,255), display_surface)
        pygame.display.update()

        # # chack if user loses
        if check_lost():
            run = False
        
    draw_text_middle("YOU LOSE", 40, (255,255,255), display_surface)
    pygame.display.update()
    pygame.time.delay(2000)


#this is the beggining of a page loop
def main_menu():
    run = True
    while run:
        display_surface.fill((0,0,0))
        draw_text_middle("Press any key to begin.", 60, (255,255,255), display_surface)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


display_surface = pygame.display.set_mode((S_Width, S_Height))
pygame.display.set_caption("Tetris")

main_menu() #start game