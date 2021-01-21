#!/usr/bin/env python
import os
import pygame,pigame
import sys
from time import sleep
from pygame.locals import *

current_path = os.path.dirname(__file__) # Where your .py file is located
image_path = os.path.join(current_path, 'resources/menu.png') # The image folder path

BLACK=(0,0,0)

os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

pygame.init()
pitft = pigame.PiTft()
pygame.mouse.set_visible(True)
#screen = pygame.display.set_mode((320,240),0,0)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
screen.fill(BLACK)

img = pygame.image.load(image_path)
screen.blit(img, (0,0))
pygame.display.update()
def deploy():
    while True:
        pitft.update()
	for event in pygame.event.get():
		if(event.type is MOUSEBUTTONDOWN):
			x,y = pygame.mouse.get_pos()
			print(x,y)
		elif(event.type is MOUSEBUTTONUP):
			x,y = pygame.mouse.get_pos()
			print(x,y)
			if y > 120:
	                	if x < 160:
	                        	print("17off")
	                	else:
	                        	print("4off")
	                else:
	                	if x < 160:
	                        	pygame.quit() ; import sys
		                        os.system("sudo poweroff") ; sys.exit(0)
	                        else:
	            	        	pygame.quit()
	                	        import sys
	                        	sys.exit(0)
        sleep(0.1)
if __name__ == '__main__':
    deploy()
