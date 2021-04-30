from pygame.display import update
from pygame import K_UP, K_RIGHT, K_DOWN, K_LEFT

from .constants import *
from .map import Map
from .pacman import Pacman
from .phantom import Phantom

class Game:
    """Manage the game"""

    def __init__(self, surface):
        self.surface = surface
        self.menu_active = True
        self._init()

    def _init(self):
        self.map = Map("./pacman/map.txt")

        self.score = 0
        self.remaining_lives = MAX_NUMBER_OF_LIVES

        self.pacman = Pacman(UP_IMAGE, RIGHT_IMAGE, DOWN_IMAGE, LEFT_IMAGE, SPEED, self.map)
        self.phantoms = []
        self.phantoms_active = [1, 0, 0, 0]
        self.activate_phantoms = True
        self.start_activate_phantoms = 0
        
        # Create phantoms
        x = WIDTH // 2 - 2 * SPRITE_SIZE
        y = (NB_SPRITES_HEIGHT // 2 - 1) * SPRITE_SIZE
        for i in range(4):
            self.phantoms.append(Phantom(PHANTOM_IMAGES[i], self.map, x + SPRITE_SIZE * i, y, SPEED))
        
    def activate_phantom(self, time):
        """Activate a new phantom every 5 seconds"""
        time_elapsed = time - self.start_activate_phantoms
        if time_elapsed < 5 * len(self.phantoms):
            if not self.phantoms_active[time_elapsed // 5]:
                self.phantoms_active[time_elapsed // 5] = 1
        else:
            self.activate_phantoms = False
        

    def change_dir(self, dir):
        """Change the pacman's direction"""
        if dir == K_UP: self.pacman.new_direction = 'up'
        elif dir == K_RIGHT: self.pacman.new_direction = 'right'
        elif dir == K_DOWN: self.pacman.new_direction = 'down'
        elif dir == K_LEFT: self.pacman.new_direction = 'left'

    def check_collisions(self, time):
        """Check collisisons between pacman and phantoms and pacgums"""
        for phantom in self.phantoms:
            if phantom.position.colliderect(self.pacman.position):
                self.remaining_lives -= 1
                self.reset_positions(time)
        for pacgum in self.map.pacgums:
            if pacgum[0] == self.pacman.position.centerx // SPRITE_SIZE\
                and pacgum[1] == self.pacman.position.centery // SPRITE_SIZE:
                self.map.pacgums.remove(pacgum)
                self.score += 10

    def draw_lives(self, surface):
        """Draw hearts standing for remaining lives in the top left corner of surface"""
        for i in range(self.remaining_lives):
            surface.blit(HEART_IMAGE, (SPRITE_SIZE * (2+i) + SPRITE_SIZE // 2 * i, 0))

    def draw_menu(self, surface):
        """Draw the menu"""
        text = MENU_FONT.render("Press a key to begin ...", 1, WHITE)
        rect = text.get_rect(center = surface.get_rect().center)
        surface.blit(text, rect)

    def draw_pacman_and_phantoms(self, surface):
        surface.blit(self.pacman.orientation, self.pacman.position)
        for phantom in self.phantoms:
            surface.blit(phantom.image, phantom.position)

    def draw_score(self, surface):
        """Draw score on the top right corner of surface"""
        text = SCORE_FONT.render("SCORE : " + str(self.score), 1, WHITE)
        rect = text.get_rect(center = (int(WIDTH * 2 / 3), SPRITE_SIZE // 2))
        surface.blit(text, rect)

    def lost(self):
        if self.remaining_lives == 0: 
            return True
        return False

    def move(self):     
        self.pacman.change_dir()
        self.pacman.move()
        for phantom in self.phantoms:
            if self.phantoms_active[self.phantoms.index(phantom)]:
                phantom.change_dir(self.map)
                phantom.move(self.map)

    def reset_positions(self, time):
        self.pacman.reset_position()
        for phantom in self.phantoms:
            phantom.reset_position()
        self.phantoms_active = [1, 0, 0, 0]
        self.activate_phantoms = True
        self.start_activate_phantoms = time

    def update(self, time = 0):
        self.check_collisions(time)
        self.move()
        self.map.draw(self.surface)
        self.draw_lives(self.surface)
        self.draw_score(self.surface)
        self.draw_pacman_and_phantoms(self.surface)
        if self.menu_active:
            self.draw_menu(self.surface)
        if len(self.map.pacgums) == 0:
            self.reset_positions(time)
            self.map.find_pacgums()
        update()