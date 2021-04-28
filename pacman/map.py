from pygame.draw import circle, rect
from .constants import *

class Map:
    """Create a map"""

    def __init__(self, file):
        self.file = file
        self.intersections = {}
        self.spawn_sprites = []
        self.pacgums = []
        self.structure = 0

    def generate(self):
        """Generate a map according to the file"""

        with open(self.file, "r") as file:
            structure = []
            for line in file:
                sub_line = []
                for sprite in line:
                    if sprite != '\n':
                        sub_line.append(sprite)
                structure.append(sub_line)
            self.structure = structure

    def draw(self, surface):
        """Draw the map and the remaining pacgums"""

        for line in range(len(self.structure)):
            for sprite in range(len(self.structure[line])):
                x = sprite * SPRITE_SIZE
                y = line * SPRITE_SIZE
                if self.structure[line][sprite] == 'b':          
                    rect(surface, BLUE, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'n':  
                    rect(surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'o':  
                    rect(surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                    if sprite > 5 and sprite < len(self.structure[line]) - 5: self.spawn_sprites.append((sprite, line))
                elif self.structure[line][sprite] == 'v':
                    rect(surface, GREEN, (x, y, SPRITE_SIZE, SPRITE_SIZE))
        
        for pacgum in self.pacgums:
            x = pacgum[0] * SPRITE_SIZE + SPRITE_SIZE // 2
            y = pacgum[1] * SPRITE_SIZE + SPRITE_SIZE // 2
            circle(surface, YELLOW, (x, y), SPRITE_SIZE // 5)
            
    def find_intersections(self):
        """Find every intersection on the map where a phantom would have to turn"""
        """Also finds the available cases for the pacgums"""
        for line in range(len(self.structure)):
            for sprite in range(len(self.structure[line])):
                x = sprite * SPRITE_SIZE
                y = line * SPRITE_SIZE
                # check if there are multiple ways going from this point
                ways = []
                if self.structure[line][sprite] == 'n':  
                    self.pacgums.append((sprite, line))
                    if self.structure[line - 1][sprite] == 'n': ways.append('up')
                    if sprite < len(self.structure[line]) - 1: 
                        if self.structure[line][sprite + 1] == 'n': ways.append('right')
                    if self.structure[line + 1][sprite] == 'n': ways.append('down')
                    if sprite > 0: 
                        if self.structure[line][sprite - 1] == 'n': ways.append('left')

                if len(ways) > 2: self.intersections[(sprite, line)] = ways
                elif len(ways) == 2 and ways != ['up', 'down'] and ways != ['right', 'left']: self.intersections[(sprite, line)] = ways
                elif self.structure[line][sprite] == 'v': self.intersections[(sprite, line - 1)] = ['right', 'left']
