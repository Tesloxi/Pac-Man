from pygame.draw import circle, rect
from .constants import *

class Map:
    """Create a map"""

    def __init__(self, file):
        self.file = file
        self.pacgums = []
        self.structure = 0
        self.generate()
        self.find_pacgums()

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
                if line == 0 and sprite == 0: #top left corner
                    self.draw_top_left_corner(surface, BLUE, x, y, SPRITE_SIZE)
                elif self.structure[line][sprite] == 'b':          
                    rect(surface, BLUE, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'n':  
                    rect(surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'o':  
                    rect(surface, BLACK, (x, y, SPRITE_SIZE, SPRITE_SIZE))
                elif self.structure[line][sprite] == 'v':
                    rect(surface, GREEN, (x, y, SPRITE_SIZE, SPRITE_SIZE))
        
        for pacgum in self.pacgums:
            x = pacgum[0] * SPRITE_SIZE + SPRITE_SIZE // 2
            y = pacgum[1] * SPRITE_SIZE + SPRITE_SIZE // 2
            circle(surface, YELLOW, (x, y), SPRITE_SIZE // 5)
    
    def draw_top_left_corner(self, surface, color, x, y, s):
        circle(surface, color, (x + s//2, y + s//2), s//2)
        rect(surface, color, (x, y + s//2, s, s//2))
        rect(surface, color, (x + s//2, y, s//2, s//2))
            
    def find_pacgums(self):
        """Find the available cases for the pacgums"""
        for row in range(len(self.structure)):
            for col in range(len(self.structure[row])):
                if self.structure[row][col] == 'n':  
                    self.pacgums.append((col, row))
