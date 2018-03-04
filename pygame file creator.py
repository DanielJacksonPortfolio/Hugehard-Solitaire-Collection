##deafault pygame file creator
name=str(input("name: "))
f=open(name+".py","w")
f.write("import pygame, sys, math, time, os, random\nfrom pygame.locals import *\nscreenW=1000\nscreenH=1000\nscreen=pygame.display.set_mode((screenW,screenH))\npygame.display.set_caption('"+name+"')\npygame.init()\nwhile 1:\n   screen.fill((255,255,255))\n   pygame.draw.circle(screen,(0,255,0),(500,500),100,0)\n   for event in pygame.event.get():\n       if event.type==QUIT:\n          pygame.quit()\n          sys.exit()\n   pygame.display.update()\n   pygame.display.flip()")
f.close()
