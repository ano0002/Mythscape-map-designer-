import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vec2

from tile import Tile

pygame.init()

running = True
infoObject = pygame.display.Info()
w,h=infoObject.current_w,infoObject.current_h
windowed_size = (w//2, h//2)

screen = pygame.display.set_mode(windowed_size, RESIZABLE)
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            if not screen.get_flags() & FULLSCREEN:
                windowed_size = event.size
        elif event.type == KEYDOWN:
            if event.key == K_F11:
                if screen.get_flags() & FULLSCREEN:
                    screen = pygame.display.set_mode(windowed_size, RESIZABLE)
                else:
                    screen = pygame.display.set_mode((w,h), FULLSCREEN)
    screen.fill((0, 25, 0))
    pygame.display.flip()
    clock.tick(60)