from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
import sys
import katmanlar
import nesneler
import haritalar
import gorunurluk

pygame.init()
width = 1200
height = 700
display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

katmanlar.init(display)
nesneler.init(display)
haritalar.init(display)
gorunurluk.init(display)

background = (51, 51, 51)

def close():
    pygame.quit()
    sys.exit()

def start_game(map):
    map.draw_map()

def GAME():
    map = haritalar.Maps()

    welcome = gorunurluk.Label(700, 100, 400, 200, None, background)
    welcome.add_text("ANGRY BIRDS", 80, "Fonts/arfmoochikncheez.ttf", (236, 240, 241))

    start = gorunurluk.Button(500, 400, 300, 100, start_game, (244, 208, 63), (247, 220, 111))
    start.add_text("START GAME", 60, "Fonts/arfmoochikncheez.ttf", background)

    exit = gorunurluk.Button(1000, 400, 300, 100, close, (241, 148, 138), (245, 183, 177))
    exit.add_text("QUIT", 60, "Fonts/arfmoochikncheez.ttf", background)

    bbms = gorunurluk.Button(width - 300, height - 80, 300, 100, None, background)
    bbms.add_text("BBMS", 60, "Fonts/arfmoochikncheez.ttf", (41, 41, 41))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit.isActive():
                    exit.action()
                if start.isActive():
                    start_game(map)

        display.fill(background)
        start.draw()
        exit.draw()
        welcome.draw()
        bbms.draw()
        pygame.display.update()
        
        # Döngünün 60 FPS hızında çalışmasını sağlar
        #clock.tick(120)
        clock.tick(60)
GAME()