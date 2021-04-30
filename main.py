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

def main(game):

    run = True
    clock = time.Clock()
    chrono_start = time.get_ticks()
    time_elapsed = 0

    while run:
        clock.tick(FPS)
        time_elapsed = int((time.get_ticks() - chrono_start) / 1000)

        if game.lost():
            run = False
            start = True

        if game.activate_phantoms:
            game.activate_phantom(time_elapsed)

        for e in event.get():
            if e.type == QUIT:
                run = False        
            elif e.type == KEYDOWN:
                game.change_dir(e.key)
        
        game.update(time_elapsed)

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
                main(game)
                run = False
    
    quit()

menu()