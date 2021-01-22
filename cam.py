import datetime
import atexit
import io
import os
import picamera
import pygame
import time
import yuv2rgb
import RPi.GPIO as GPIO
from pygame.locals import *

current_path = os.path.dirname(__file__) # Where your .py file is located

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

screenMode      =  3
sizeMode        =  0

sizeData = [[(1440, 1080), (320, 240), (0.2222, 0.2222, 0.5556, 0.5556)]]

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')

rgb = bytearray(320 * 240 * 3)
yuv = bytearray(320 * 240 * 3 / 2)

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

camera            = picamera.PiCamera()
atexit.register(camera.close)
camera.resolution = sizeData[sizeMode][1]
camera.crop       = (0.0, 0.0, 1.0, 1.0)
camera.rotation = 270
def deploy():
    while(True):
      button_23 = GPIO.input(23)
      event = pygame.event.poll()
      stream = io.BytesIO()
      camera.capture(stream, use_video_port=True, format='raw')
      stream.seek(0)
      stream.readinto(yuv)
      stream.close()
      yuv2rgb.convert(yuv, rgb, sizeData[sizeMode][1][0],
        sizeData[sizeMode][1][1])
      img = pygame.image.frombuffer(rgb[0:
        (sizeData[sizeMode][1][0] * sizeData[sizeMode][1][1] * 3)],
        sizeData[sizeMode][1], 'RGB')
      if img:
        screen.blit(img,
          ((320 - img.get_width() ) / 2,
           (240 - img.get_height()) / 2))
      if event.type == pygame.MOUSEBUTTONDOWN:
        pygame.draw.rect(screen,(255,255,255), (0,0,320,240))
        pygame.display.update()
        now = datetime.datetime.now()
        image_date = now.strftime("pics/%Y-%m-%d_%H%M%S.jpg")
        image_path = os.path.join(current_path, image_date)
        camera.capture(image_path)
        img = pygame.image.load(image_path)
        screen.blit(img, (0,0))
        pygame.display.update()
        time.sleep(1)
      pygame.display.update()
if __name__ == '__main__':
    deploy()
