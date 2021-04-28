from pygame.display import update

from .constants import *
from .map import Map
from .pacman import Pacman

class Game:
    """Manage the game"""

    def __init__(self, surface):
        self.surface = surface
        self.menu_active = True
        self._init()

    def _init(self):
        self.map = Map("./pacman/map.txt")
        self.map.generate()
        self.map.find_intersections()

        self.max_score = len(self.map.pacgums) * 10
        self.score = 0
        self.remaining_lives = MAX_NUMBER_OF_LIVES

        self.pacman = Pacman(UP_IMAGE, RIGHT_IMAGE, DOWN_IMAGE, LEFT_IMAGE, SPEED, self.map)
        self.phantoms = []

    def draw_lives(self, surface):
        """Draw hearts standing for remaining lives in the top left corner of surface"""
        for i in range(self.remaining_lives):
            surface.blit(HEART_IMAGE, (SPRITE_SIZE * (2+i) + SPRITE_SIZE // 2 * i, 0))

    def draw_menu(self, surface):
        """Draw the menu"""
        text = MENU_FONT.render("Press a key to begin ...", 1, WHITE)
        rect = text.get_rect(center = surface.get_rect().center)
        surface.blit(text, rect)

    def draw_score(self, surface):
        """Draw score on the top right corner of surface"""
        text = SCORE_FONT.render("SCORE : " + str(self.score), 1, WHITE)
        rect = text.get_rect(center = (int(WIDTH * 2 / 3), SPRITE_SIZE // 2))
        surface.blit(text, rect)

    def update(self):
        self.map.draw(self.surface)
        self.draw_lives(self.surface)
        self.draw_score(self.surface)
        self.surface.blit(self.pacman.orientation, self.pacman.position)
        for phantom in self.phantoms:
            pass
        if self.menu_active:
            self.draw_menu(self.surface)
        update()