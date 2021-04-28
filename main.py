#!/usr/bin/python3
# -*- coding: utf-8 -*

import os, random

from pygame import *
from tkinter import Tk

from pacman.constants import WIDTH, HEIGHT
from pacman.game import Game

init()

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

win_x = screen_height // 2 - WIDTH // 2
win_y = screen_height // 2 - HEIGHT // 2

os.environ['SDL_VIDEO_WINDOW_POS'] = f"{win_x},{win_y}"
WIN = display.set_mode((WIDTH, HEIGHT)) # main window
display.set_caption("Pac Man")

FPS = 60

def main():

    # Setup game loop

    clock = time.Clock()
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
            time.delay(1000)
            start = True
        
        # Draw the remaining pacgums (little yellow points you eat to earn points)
        for j in map.pacgums:
            if j[1]:
                if j[0][0] == pacman.position.x // SPRITE_SIZE and j[0][1] == pacman.position.y // SPRITE_SIZE:
                    j[1] = False
                    pacman.score += 10
                else:
                    x = j[0][0] * SPRITE_SIZE + SPRITE_SIZE // 2
                    y = j[0][1] * SPRITE_SIZE + SPRITE_SIZE // 2
                    draw.circle(WIN, YELLOW, (x, y), 3)

        if start: 
            text = READY_FONT.render('READY !', 1, YELLOW)
            WIN.blit(text, (int(WIDTH / 2 - text.get_width() // 2), int(HEIGHT / 2 - text.get_height() // 2)))
            display.update()
            time.delay(1000)
            start = False

        for event in event.get():
            if event.type == QUIT:
                run = False        
            elif event.type == KEYDOWN:
                if event.key == K_UP: pacman.new_direction = 'up'
                elif event.key == K_RIGHT: pacman.new_direction = 'right'
                elif event.key == K_DOWN: pacman.new_direction = 'down'
                elif event.key == K_LEFT: pacman.new_direction = 'left'

        pacman.change_dir()
        phantom.change_dir()
        pacman.move()
        phantom.move()

        if pacman.remaining_lives == 0 or pacman.score == MAX_SCORE: run = False
        
        game.update()

def menu():
    run = True

    game = Game(WIN)
    game.update()

    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                game.menu_active = False
                main()
    
    quit()

menu()