import pygame
from sprite import Sprite

class Enemy(Sprite):

    def __init__(self, pos, size, type):
      Sprite.__init__(self,pos,(600,600), "OPRun.png")
      self.state = "idle"
      self.dead = False
      self.facing = "left"
      self.startpos = pos
      self.farthest_left = pos[0] - 100 #set pos[0] - platform size * 1.5
      self.farest_right = pos[0] + 100 #set pos[0] - platform size * 1.5
      self.steps = 0
      self.animationChange("OP IDLE")
      self.frame_num = 0

    

    def draw(self, screen):
        self.updateAnimNumber()

        #keep playing animation by indexing from animation list.
        self.surf = self.rightAnim if self.facing == "right" else self.leftAnim
        screen.blit(self.surf[self.frame_num], self.rect.topleft)