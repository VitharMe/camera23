from __future__ import absolute_import
import pygame,pitft_touchscreen,os
defaultrot = os.getenv(u'PIGAME_ROT') or u'90'
support_gpio = True
envmk = [u'PIGAME_V2',u'PIGAME_INVERTX',u'PIGAME_INVERTY',u'PIGAME_SWAPXY',u'PIGAME_BTN1',u'PIGAME_BTN2',u'PIGAME_BTN3',u'PIGAME_BTN4']
env = {}
for i in envmk:
    env[i] = os.getenv(i)
try:
    import RPi.GPIO as GPIO
except ImportError:
    support_gpio = False
from pygame.locals import *
class PiTft(object):
    def __init__(self,rotation=-1,v2=False if env[u'PIGAME_V2']==u'off' else True,allow_gpio=True,invertx=True if env[u'PIGAME_INVERTX']==u'on' else False,inverty=True if env[u'PIGAME_INVERTY']==u'on' else False,swapxy=True if env[u'PIGAME_SWAPXY']==u'on' else False,buttons=[False if env[u'PIGAME_BTN1']==u'off' else True,False if env[u'PIGAME_BTN2']==u'off' else True,False if env[u'PIGAME_BTN3']==u'off' else True,False if env[u'PIGAME_BTN4']==u'off' else True]):
        self.use_gpio = support_gpio and allow_gpio and not (os.getenv(u'PIGAME_GPIO') == u'off')
        if not self.use_gpio:
            buttons=[False,False,False,False]
        if rotation == -1:
            rotation = int(defaultrot)
        self.pitft=pitft_touchscreen.pitft_touchscreen()
        self.pitft.button_down=False
        self.pitft.pigameapi=2
        self.pitft.pigamerotr=rotation
        self.invertx = invertx
        self.inverty = inverty
        self.swapxy = swapxy
        self.cachedpos = [0,0]
        self.__b1 = False
        self.__b2 = False
        self.__b3 = False
        self.__b4 = False
        self.__pin1 = 17
        self.__pin2 = 22
        self.__pin3 = 23
        self.__pin4 = 27
        if self.use_gpio:
            GPIO.setmode(GPIO.BCM)
        if buttons[0]:
            GPIO.setup(self.__pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b1 = True
        if buttons[1]:
            GPIO.setup(self.__pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b2 = True
        if buttons[2]:
            GPIO.setup(self.__pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b3 = True
        if buttons[3]:
            if not v2:
                self.__pin4 = 21
            GPIO.setup(self.__pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b4 = True
        self.pitft.start()
    def update(self):
        u"""Add Touchscreen Events to PyGame event queue."""
        while not self.pitft.queue_empty():
            for r in self.pitft.get_event():
                e={u"y":(r[u"x"] if r[u"x"] else self.cachedpos[0]),u"x":(r[u"y"] if r[u"y"] else self.cachedpos[1])}
                rel=(e[u"x"] - self.cachedpos[0],e[u"y"] - self.cachedpos[1])
                self.cachedpos=(e[u"x"],e[u"y"])
                if self.pitft.pigamerotr==90:
                    e={u"x":e[u"x"],u"y":240-e[u"y"]}
                    rel=(rel[0],240-rel[1])
                elif self.pitft.pigamerotr==270:
                    e={u"x":320-e[u"x"],u"y":e[u"y"]}
                    rel=(320-rel[0],rel[1])
                else:
                    raise(Exception(u"PiTft rotation is unsupported"))
                d={}
                t=MOUSEBUTTONUP if r[u"touch"]==0 else (MOUSEMOTION if self.pitft.button_down else MOUSEBUTTONDOWN)
                if self.invertx:
                    e={u"x":320-e[u"x"],u"y":e[u"y"]}
                    rel=(320-rel[0],rel[1])
                if self.inverty:
                    rel=(rel[0],240-rel[1])
                    e={u"y":240-e[u"y"],u"x":e[u"x"]}
                if self.swapxy:
                    rel=(rel[1],rel[0])
                    e={u"x":e[u"y"],u"y":e[u"x"]}
                if t==MOUSEBUTTONDOWN:
                    d[u"button"]=1
                    d[u"pos"]=(e[u"x"],e[u"y"])
                    self.pitft.button_down = True
                    pygame.mouse.set_pos(e[u"x"],e[u"y"])
                elif t==MOUSEBUTTONUP:
                    self.pitft.button_down = False
                    d[u"button"]=1
                    d[u"pos"]=(e[u"x"],e[u"y"])
                else:
                    d[u"buttons"]=(True,False,False)
                    d[u"rel"]=rel
                    d[u"pos"]=(e[u"x"],e[u"y"])
                    pygame.mouse.set_pos(e[u"x"],e[u"y"])
                pe=pygame.event.Event(t,d)
                pygame.event.post(pe)
    def __del__(self):
        u"""Cleaning up Touchscreen events and Threads when the Object destroyed."""
        self.pitft.stop()
        if self.use_gpio:
            GPIO.cleanup()
    def Button1Interrupt(self,callback=None,bouncetime=200):
        u"""Calls callback if Button1 pressed."""
        if self.__b1: 
            GPIO.add_event_detect(self.__pin1,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button2Interrupt(self,callback=None,bouncetime=200):
        u"""Calls callback if Button2 pressed."""
        if self.__b2: 
            GPIO.add_event_detect(self.__pin2,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button3Interrupt(self,callback=None,bouncetime=200):
        u"""Calls callback if Button3 pressed."""
        if self.__b3: 
            GPIO.add_event_detect(self.__pin3,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    def Button4Interrupt(self,callback=None,bouncetime=200):
        u"""Calls callback if Button4 pressed."""
        if self.__b4: 
            GPIO.add_event_detect(self.__pin4,GPIO.FALLING,callback=callback,bouncetime=bouncetime)
    @property
    def Button1(self):
        u"""Equals True if Button 1 is pressed."""
        if self.__b1:
            return not GPIO.input(self.__pin1)
    @property
    def Button2(self):
        u"""Equals True if Button 2 is pressed."""
        if self.__b2:
            return not GPIO.input(self.__pin2)
    @property
    def Button3(self):
        u"""Equals True if Button 3 is pressed."""
        if self.__b3:
            return not GPIO.input(self.__pin3)
    @property
    def Button4(self):
        u"""Equals True if Button 4 is pressed."""
        if self.__b4:
            return not GPIO.input(self.__pin4)
