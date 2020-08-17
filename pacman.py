import pygame, os, random

pygame.init()

# setup display
NB_SPRITES_WIDTH = 28
NB_SPRITES_HEIGHT = 31
SPRITE_SIZE = 20
WIDTH = NB_SPRITES_WIDTH * SPRITE_SIZE
HEIGHT = NB_SPRITES_HEIGHT * SPRITE_SIZE

os.environ['SDL_VIDEO_WINDOW_POS'] = "400,100"
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac Man")

# character images
UP = pygame.image.load("./images/character/up.png")
RIGHT = pygame.image.load("./images/character/right.png")
DOWN = pygame.image.load("./images/character/down.png")
LEFT = pygame.image.load("./images/character/left.png")

# lives and score
TOTALLIVES = 3
LIVE = pygame.image.load("./images/character/heart.png")
MAX_SCORE = 0

# phantom images
phantoms = [
    pygame.image.load("./images/phantom/blue.png"),
    pygame.image.load("./images/phantom/green.png"),
    pygame.image.load("./images/phantom/orange.png")
]

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# fonts
READY_FONT = pygame.font.SysFont('comicsans', 80)
SCORE_FONT = pygame.font.SysFont('comicsans', 30)

class Map:
    """Create a self.map"""
    def __init__(self, surface, file):
        self.surface = surface
        self.file = file
        self.intersections = {}
        self.spawn_sprites = []
        self.pacgums = []
        self.structure = 0

    def generate(self):
        """Generate a self.map according to the file"""
        with open(self.file, "r") as file:
            structure = []
            for line in file:
                sub_line = []
                for sprite in line:
                    if sprite != '\n':
                        sub_line.append(sprite)
                structure.append(sub_line)
            self.structure = structure

    def draw(self):
        """Print the self.map after having generating it"""
        for line in range(len(self.structure)):
            for sprite in range(len(self.structure[line])):
                x = sprite * SPRITE_SIZE
                y = line * SPRITE_SIZE
                if self.structure[line][sprite] == 'b':          
                    pygame.draw.rect(self.surface, BLUE, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'n':  
                    pygame.draw.rect(self.surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'o':  
                    pygame.draw.rect(self.surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                    if sprite > 5 and sprite < len(self.structure[line]) - 5: self.spawn_sprites.append((sprite, line))
                elif self.structure[line][sprite] == 'v':
                    pygame.draw.rect(self.surface, GREEN, (x, y, SPRITE_SIZE, SPRITE_SIZE))
            
    def find_intersections(self):
        """Find every intersection on the map for which a phantom would have to turn"""
        """Also finds the available cases for the pacgums"""
        for line in range(len(self.structure)):
            for sprite in range(len(self.structure[line])):
                x = sprite * SPRITE_SIZE
                y = line * SPRITE_SIZE
                # check if there are multiple ways going from this point
                ways = []
                if self.structure[line][sprite] == 'n':  
                    self.pacgums.append([(sprite, line), True])
                    if self.structure[line - 1][sprite] == 'n': ways.append('up')
                    if sprite < len(self.structure[line]) - 1: 
                        if self.structure[line][sprite + 1] == 'n': ways.append('right')
                    if self.structure[line + 1][sprite] == 'n': ways.append('down')
                    if sprite > 0: 
                        if self.structure[line][sprite - 1] == 'n': ways.append('left')

                if len(ways) > 2: self.intersections[(sprite, line)] = ways
                elif len(ways) == 2 and ways != ['up', 'down'] and ways != ['right', 'left']: self.intersections[(sprite, line)] = ways
                elif self.structure[line][sprite] == 'v': self.intersections[(sprite, line - 1)] = ['right', 'left']

class Pacman:
    """Create the character"""
    def __init__(self, up, right, down, left, map):
        # character images
        self.up = up ; self.right = right ; self.down = down ; self.left = left
        self.position = self.right.get_rect(x= 14 * SPRITE_SIZE, y = 23 * SPRITE_SIZE)
        self.orientation = self.left
        self.old_direction = ''
        self.new_direction = ''
        self.map = map
        self.remaining_lives = TOTALLIVES
        self.score = 0

    def reset_position(self):
        self.position.x = 14 * SPRITE_SIZE
        self.position.y = 23 * SPRITE_SIZE
        self.orientation = self.left
        self.old_direction = ''
        self.new_direction = ''

    def change_dir(self):
        x = self.position.x; y = self.position.y
        if self.new_direction == 'up':
            if x % SPRITE_SIZE == 0:
                if self.map.structure[(y - 1) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                    self.old_direction = self.new_direction
        elif self.new_direction == 'right':
            if y % SPRITE_SIZE == 0:
                if x < WIDTH - SPRITE_SIZE * 2:
                    if self.map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                        self.old_direction = self.new_direction
        elif self.new_direction == 'down':
            if x % SPRITE_SIZE == 0:
                if self.map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                    self.old_direction = self.new_direction
        elif self.new_direction == 'left':
            if y % SPRITE_SIZE == 0:
                if self.map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                    self.old_direction = self.new_direction            
    
    def move(self):
        x = self.position.x; y = self.position.y
        if self.old_direction == 'up':
            if self.map.structure[(y - 1) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.orientation = self.up
                self.position.y -= 1 
        elif self.old_direction == 'right':
            if x > WIDTH: 
                self.position.x = 0
            elif x > WIDTH - SPRITE_SIZE - 1:
                self.orientation = self.right
                self.position.x += 1 
            elif self.map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                self.orientation = self.right
                self.position.x += 1 
        elif self.old_direction == 'down':
            if self.map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.orientation = self.down
                self.position.y += 1
        elif self.old_direction == 'left':
            if x < 0 - SPRITE_SIZE:
                self.position.x = WIDTH - SPRITE_SIZE
            elif self.map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                self.orientation = self.left
                self.position.x -= 1 

class Phantom():
    """Create a phantom"""
    def __init__(self, image, map, spawn_xmin, spawn_xmax, spawn_ymin, spawn_ymax):
        self.image = image
        self.map = map
        self.xmin = spawn_xmin * SPRITE_SIZE; self.xmax = spawn_xmax * SPRITE_SIZE; self.ymin = spawn_ymin * SPRITE_SIZE; self.ymax = spawn_ymax * SPRITE_SIZE
        self.x = random.randrange(self.xmin, self.xmax, SPRITE_SIZE)
        self.y = random.randrange(self.ymin, self.ymax, SPRITE_SIZE)
        self.position = self.image.get_rect(x = self.x, y = self.y)
        self.direction = ''

    def reset_position(self):
        self.position.x = self.x
        self.position.y = self.y
        self.direction = ''
    
    def change_dir(self):
        x = self.position.x; y = self.position.y
        if x >= self.xmin and x < self.xmax and y >= self.ymin and y < self.ymax:
            if x < self.xmin + SPRITE_SIZE * 2: self.direction = 'right'
            elif x > self.xmax - SPRITE_SIZE * 3: self.direction = 'left'
            else: self.direction = 'up'
        elif x >= self.xmin + SPRITE_SIZE * 2 and x <= self.xmax - SPRITE_SIZE * 2 and y > self.ymin - SPRITE_SIZE * 2 and y <= self.ymin: self.direction = 'up'
        else:
            if x % SPRITE_SIZE == 0 and y % SPRITE_SIZE == 0:
                for i, j in self.map.intersections.items():
                    if i[0] == x // SPRITE_SIZE and i[1] == y // SPRITE_SIZE:
                        self.direction = random.choice(j)                  
                        break

    def move(self):
        x = self.position.x; y = self.position.y
        if self.direction == 'up':
            if self.map.structure[(y - 1) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.position.y -= 1 
        elif self.direction == 'right':
            if x > WIDTH: 
                self.position.x = 0
            elif x > WIDTH - SPRITE_SIZE - 1:
                self.position.x += 1 
            elif self.map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                self.position.x += 1 
        elif self.direction == 'down':
            if self.map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.position.y += 1
        elif self.direction == 'left':
            if x < 0 - SPRITE_SIZE:
                self.position.x = WIDTH - SPRITE_SIZE
            elif self.map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                self.position.x -= 1 

class Pacgum():
    def __init__(self, surface, size, color, x, y):
        self.surface = surface
        self.size = size
        self.color = color
        self.x = x + SPRITE_SIZE / 2 - self.size / 2
        self.y = y + SPRITE_SIZE / 2 - self.size / 2
        self.display = True

# create game components
map = Map(win, "./map.txt")
map.generate()
map.find_intersections()
MAX_SCORE = len(map.pacgums) * 10
print(MAX_SCORE)
pacman = Pacman(UP, RIGHT, DOWN, LEFT, map)
phantom = Phantom(random.choice(phantoms), map, 11, 17, 13, 16)

# setup game loop
FPS = 60
clock = pygame.time.Clock()
start = True
run = True

while run:
    clock.tick(FPS)

    # Check collisions
    if (phantom.position.x // SPRITE_SIZE == pacman.position.x //  SPRITE_SIZE and ((phantom.position.y + SPRITE_SIZE >= pacman.position.y and phantom.position.y + SPRITE_SIZE <= pacman.position.y + SPRITE_SIZE) or (phantom.position.y <= pacman.position.y + SPRITE_SIZE and phantom.position.y >= pacman.position.y))) \
        or (phantom.position.y // SPRITE_SIZE == pacman.position.y //  SPRITE_SIZE and ((phantom.position.x + SPRITE_SIZE >= pacman.position.x and phantom.position.x + SPRITE_SIZE <= pacman.position.x + SPRITE_SIZE) or (phantom.position.x <= pacman.position.x + SPRITE_SIZE and phantom.position.x >= pacman.position.x))):
        pacman.remaining_lives -= 1
        print(pacman.remaining_lives)
        pacman.reset_position()
        phantom.reset_position()
        pygame.time.delay(1000)
        start = True

    map.draw()
    for i in range(pacman.remaining_lives):
        win.blit(LIVE, (int(SPRITE_SIZE * (2 + i) + ((SPRITE_SIZE // 2) * i)), 0))
    score = SCORE_FONT.render('SCORE : ' + str(pacman.score), 0, WHITE)
    win.blit(score, (WIDTH // 3 * 2, 2))
    for j in map.pacgums:
        if j[1]:
            if j[0][0] == pacman.position.x // SPRITE_SIZE and j[0][1] == pacman.position.y // SPRITE_SIZE:
                j[1] = False
                pacman.score += 10
            else:
                x = j[0][0] * SPRITE_SIZE + SPRITE_SIZE // 2
                y = j[0][1] * SPRITE_SIZE + SPRITE_SIZE // 2
                pygame.draw.circle(win, YELLOW, (x, y), 3)
    win.blit(pacman.orientation, pacman.position)
    win.blit(phantom.image, phantom.position)
    pygame.display.update()

    if start: 
        text = READY_FONT.render('READY !', 1, YELLOW)
        win.blit(text, (int(WIDTH / 2 - text.get_width() // 2), int(HEIGHT / 2 - text.get_height() // 2)))
        pygame.display.update()
        pygame.time.delay(1000)
        start = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): run = False        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: pacman.new_direction = 'up'
            elif event.key == pygame.K_RIGHT: pacman.new_direction = 'right'
            elif event.key == pygame.K_DOWN: pacman.new_direction = 'down'
            elif event.key == pygame.K_LEFT: pacman.new_direction = 'left'

    pacman.change_dir()
    phantom.change_dir()
    pacman.move()
    phantom.move()

    if pacman.remaining_lives == 0 or pacman.score == MAX_SCORE: run = False
    
pygame.quit()