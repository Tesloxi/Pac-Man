from .constants import *

class Pacman:
    """Create the character"""

    def __init__(self, up, right, down, left, speed, map):
        self.up = up ; self.right = right ; self.down = down ; self.left = left
        self.position = self.right.get_rect(x= 14 * SPRITE_SIZE, y = 23 * SPRITE_SIZE)
        self.orientation = self.left
        self.old_direction = ''
        self.new_direction = ''
        self.map = map
        self.speed = speed

    def reset_position(self):
        """Restart the Pac-Man's position and direction"""
        self.position.x = 14 * SPRITE_SIZE
        self.position.y = 23 * SPRITE_SIZE
        self.orientation = self.left
        self.old_direction = ''
        self.new_direction = ''

    def change_dir(self):
        """Change the direction the Pac-Man's wants to go"""
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
        """Move the Pac-Man accordingly to the directions he wants to go and can go"""
        x = self.position.x; y = self.position.y
        if self.old_direction == 'up':
            if self.map.structure[(y - 1) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.orientation = self.up
                self.position.y -= self.speed
        elif self.old_direction == 'right':
            if x > WIDTH: 
                self.position.x = 0
            elif x > WIDTH - SPRITE_SIZE - 1:
                self.orientation = self.right
                self.position.x += self.speed
            elif self.map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                self.orientation = self.right
                self.position.x += self.speed
        elif self.old_direction == 'down':
            if self.map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.orientation = self.down
                self.position.y += self.speed
        elif self.old_direction == 'left':
            if x < 0 - SPRITE_SIZE:
                self.position.x = WIDTH - SPRITE_SIZE
            elif self.map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                self.orientation = self.left
                self.position.x -= self.speed