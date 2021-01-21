#!/usr/bin/env python
import os
import pygame
import sys
from time import sleep
from pygame.locals import *

current_path = os.path.dirname(__file__) # Where your .py file is located
image_path = os.path.join(current_path, 'resources/menu.png') # The image folder path

BLACK=(0,0,0)

def deploy():
    os.putenv('SDL_FBDEV', '/dev/fb1')
    pygame.init()
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((320,240),0,0)
    screen.fill(BLACK)
    event = pygame.event.poll()
    
    while True:
		img = pygame.image.load(image_path)
		screen.blit(img, (0,0))
		pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
if __name__ == '__main__':
    deploy()