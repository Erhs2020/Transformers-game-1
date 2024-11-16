import pygame
from sprite import Sprite

class Enemy(Sprite):

    def __init__(self, pos):
      Sprite.__init__(self,pos,(600,600), "OPRun.png")
      self.state = "idle"
      self.dead = False
      self.facing = "right"
      self.startpos = pos
      self.farthest_left = pos[0] - 100 #set pos[0] - platform size * 1.5
      self.farest_right = pos[0] + 100 #set pos[0] - platform size * 1.5
      self.steps = 0

