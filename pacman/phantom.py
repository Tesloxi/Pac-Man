from .constants import *
from random import choice

class Phantom():
    """Create a phantom"""

    def __init__(self, image, map, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.position = self.image.get_rect(x = self.x, y = self.y)
        self.direction = 'up'
        self.speed = speed

    def reset_position(self):
        self.position.x = self.x
        self.position.y = self.y
        self.direction = ''
    
    def change_dir(self, map):
        x = self.position.x
        y = self.position.y
        if x % SPRITE_SIZE == 0 and y % SPRITE_SIZE == 0:
            col = x // SPRITE_SIZE
            row = y // SPRITE_SIZE
            ways = self.find_ways(map.structure, col, row)
            if len(ways) > 0 and len(ways) != 2:
                self.direction = choice(ways)  
            elif len(ways) == 2 and ways != ["up", 'down'] and ways != ["right", "left"]:
                if self.direction == "up":
                    ways.remove("down")
                elif self.direction == "right":
                    ways.remove("left")
                elif self.direction == "down":
                    ways.remove("up")
                elif self.direction == "left":
                    ways.remove("right")
                self.direction = ways[0]
            elif len(ways) > 0 and map.structure[row][col] == 'o':
                self.direction = choice(ways)
            elif ways == ["right", "left"] and map.structure[row + 1][col] == 'v':
                self.direction = choice(ways)

    def find_ways(self, map, col, row):
        """Find where the phantom can go from its current position"""
        ways = []

        if map[row][col] == 'n':
            if map[row - 1][col] == 'n':
                ways.append("up")
            if col < NB_SPRITES_WIDTH - 1:
                if map[row][col + 1] == 'n':
                    ways.append("right")
            if map[row + 1][col] == 'n':
                ways.append("down")
            if col > 0:
                if map[row][col - 1] == 'n':
                    ways.append("left")
        elif map[row][col] == 'v':
            if map[row - 1][col] == 'n':
                ways.append("up")
        elif map[row][col] == 'o':
            if map[row - 1][col] == 'o' or map[row - 1][col] == 'v':
                ways.append("up")
            if map[row][col + 1] == 'o':
                ways.append("right")
            if map[row][col - 1] == 'o':
                ways.append("left")
        return ways

    def move(self, map):
        x = self.position.x
        y = self.position.y

        if self.direction == 'up':
            if map.structure[(y - 1) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.position.y -= self.speed
        elif self.direction == 'right':
            if x > WIDTH: 
                self.position.x = 0
            elif x > WIDTH - SPRITE_SIZE - 1:
                self.position.x += self.speed
            elif map.structure[y // SPRITE_SIZE][(x + SPRITE_SIZE) // SPRITE_SIZE] != 'b':
                self.position.x += self.speed
        elif self.direction == 'down':
            if map.structure[(y + SPRITE_SIZE) // SPRITE_SIZE][x // SPRITE_SIZE] != 'b':
                self.position.y +=self.speed
        elif self.direction == 'left':
            if x < 0 - SPRITE_SIZE:
                self.position.x = WIDTH - SPRITE_SIZE
            elif map.structure[y // SPRITE_SIZE][(x - 1) // SPRITE_SIZE] != 'b':
                self.position.x -= self.speed