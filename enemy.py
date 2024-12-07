import pygame
from sprite import Sprite

class Enemy(Sprite):

    def __init__(self, pos, size, type, PLATFORM_SIZE):
      Sprite.__init__(self,pos,(600,600), "OPRun.png")
      self.state = "patrol"
      self.dead = False
      self.facing = "left"
      self.startpos = pos
      self.farthest_left = pos[0] - PLATFORM_SIZE[0] * 1.5
      self.farthest_right = pos[0] + PLATFORM_SIZE[0] * 1.5
      self.steps = 0
      self.animationChange("OP IDLE")
      self.frame_num = 0
      self.boundary_rect = self.get_mask_rect(self.mask, self.rect.topleft)
      offsety = self.boundary_rect.top - self.rect.top
      offsetx = self.boundary_rect.left - self.rect.left
      self.rect.top = self.rect.top - offsety - (self.boundary_rect.bottom - self.boundary_rect.top)
      self.rect.left = self.rect.left - offsetx
      print(self.rect.topleft)
    

    def draw(self, screen): #use speed to update farthest pos
        self.updateAnimNumber()

        #keep playing animation by indexing from animation list.
        self.surf = self.rightAnim if self.facing == "right" else self.leftAnim
        screen.blit(self.surf[self.frame_num], self.rect.topleft)

    def move(self, speed):
      self.boundary_rect = self.get_mask_rect(self.mask, self.rect.topleft)
      self.farthest_left 
      if self.boundary_rect.left <= self.farthest_left:
        self.facing = "right"
      if self.boundary_rect.right >= self.farthest_right:
        self.facing = "left"
      if self.state == "patrol":
        if self.facing == "right":
          self.rect.move_ip(1,0)
        elif self.facing == "left":
          self.rect.move_ip(-1,0)
