import pygame
from sprite import Sprite

class Blaster(Sprite):
    
    def __init__(self):
        Sprite.__init__(self,(125,305), (26,13), "OPBlaster.png")
        self.angle = 0
        self.facing = "right"
        self.starting_pos = self.rect.bottomleft
      

    def draw(self,SCREEN, player):

        r_surf, r_rect = self.rotateSprite(self.angle)
        SCREEN.blit(r_surf, r_rect)
        mouse_pos = pygame.mouse.get_pos()
        self.angle = self.calculateAngle(self.rect.topleft, mouse_pos)
        if player.facing == "right": 
            if player.facing != self.facing:
                self.flipBlaster()
                self.facing = "right"
                self.rect.topleft = (125,305)
            if self.angle > 90:
                self.angle = 90
            if self.angle < -90:
                self.angle = -90
        else:
            if player.facing != self.facing:
                self.flipBlaster()
                self.facing = "left"
                self.rect.topleft = (100,305)
            if 0 <= self.angle <= 89:
                self.angle = 90
            elif -89 <= self.angle <= -0:
                self.angle = -90
           
       
        px, py = player.boundary_rect.center
        if self.facing == "right":
            self.rect.topleft = (px,py - 7)
        else:
            self.rect.topright = (px,py - 7)
        if player.states["running"]:
            if player.frame_num % 2 == 0:
                self.rect.centery += 1
            else:
                self.rect.centery -= 4

    def flipBlaster(self):
        self.surf = pygame.transform.flip(self.surf, False, True)
