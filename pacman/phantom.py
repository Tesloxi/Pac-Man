from .constants import *

class Phantom():
    """Create a phantom"""

    def __init__(self, image, map, spawn_xmin, spawn_xmax, spawn_ymin, spawn_ymax, speed):
        self.image = image
        self.map = map
        self.xmin = spawn_xmin * SPRITE_SIZE; self.xmax = spawn_xmax * SPRITE_SIZE; self.ymin = spawn_ymin * SPRITE_SIZE; self.ymax = spawn_ymax * SPRITE_SIZE
        self.x = random.randrange(self.xmin, self.xmax, SPRITE_SIZE)
        self.y = random.randrange(self.ymin, self.ymax, SPRITE_SIZE)
        self.position = self.image.get_rect(x = self.x, y = self.y)
        self.direction = ''
        self.speed = speed

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
                self.position.y -= self.speed
        elif self.direction == 'right':
            if x > WIDTH: 
                self.position.x = 0
            elif x > WIDTH - SPRITE_SIZE - 1:
                self.position.x += self.speed
            elif self.map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                self.position.x += self.speed
        elif self.direction == 'down':
            if self.map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.position.y +=self.speed
        elif self.direction == 'left':
            if x < 0 - SPRITE_SIZE:
                self.position.x = WIDTH - SPRITE_SIZE
            elif self.map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                self.position.x -= self.speed