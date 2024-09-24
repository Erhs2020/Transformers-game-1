import pygame
from sprite import Sprite

class Blaster(Sprite):
    
    def __init__(self):
        Sprite.__init__(self,(125,305), (34,17), "OPBlaster.png")
        self.angle = 0
        self.facing = "right"
        self.starting_pos = self.rect.bottomleft
      

    def draw(self,SCREEN, player, player_state, player_frame_num, playerfacing):
        r_surf, r_rect = self.rotateSprite(self.angle)
        SCREEN.blit(r_surf, r_rect)
        mouse_pos = pygame.mouse.get_pos()
        self.angle = self.calculateAngle(self.rect.topleft, mouse_pos)
        if playerfacing == "right": 
            if playerfacing != self.facing:
                self.flipBlaster()
                self.facing = "right"
                self.rect.topleft = (125,305)
            if self.angle > 90:
                self.angle = 90
            if self.angle < -90:
                self.angle = -90
        else:
            if playerfacing != self.facing:
                self.flipBlaster()
                self.facing = "left"
                self.rect.topleft = (100,305)
            if 0 <= self.angle <= 89:
                self.angle = 90
            elif -89 <= self.angle <= -0:
                self.angle = -90
           
       

        if player_state["running"] == False:
            if self.facing == "right":
                if self.angle < 25:
                    self.rect.topleft = (self.rect.left,305)
                else:
                    self.rect.topleft = (self.rect.left,295)
            else:
                if 90 <= self.angle <= 155:
                    self.rect.topleft = (self.rect.left,295)
                else:
                    self.rect.topleft = (self.rect.left,305)
        
        if player_state["running"]:
            if player_frame_num % 2 == 0:
                self.rect.centery = player.rect.centery - 8
            else:
                self.rect.centery = player.rect.centery + 8
            print(self.rect.centery)
            

    def flipBlaster(self):
        self.surf = pygame.transform.flip(self.surf, False, True)
