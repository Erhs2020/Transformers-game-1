import pygame
from sprite import Sprite
from bullet import Bullet
import time

class Blaster(Sprite):
    
    def __init__(self):
        Sprite.__init__(self,(125,305), (26,13), "OPBlaster.png")
        self.angle = 0
        self.facing = "right"
        self.starting_pos = self.rect.bottomleft
        self.bullets = []
        self.showing = False

        #og size (26,13)


    #shoots bullet at target
    def shoot(self, pos):
        if self.showing:
            # make bullet at blaster 
            bullet = Bullet(self.rect.center, 10, (252,109,0), (10,10))
            self.bullets.append(bullet)
            # make bullet go to mouse cursor/ pos
            bullet.shoot(pos)
            print(pos)
    
    #flip blaster on screen vertical
    def flipBlaster(self):
        self.surf = pygame.transform.flip(self.surf, False, True)


    #bullet hits somethings
    def hit(self, other):
        for bullet in self.bullets:
            #bullet collides with something
            offset = (other.rect.x - bullet.rect.x, other.rect.y - bullet.rect.y)
            collision_point = bullet.mask.overlap(other.mask, offset)
            if collision_point:
                self.bullets.remove(bullet)
                return True

    #rotate
    def rotate_towards(self, owner, pos):
        r_surf, r_rect = self.rotateSprite(self.angle)
        self.angle = self.calculateAngle(self.rect.topleft, pos)
        if owner.facing == "right": 
            if owner.facing != self.facing:
                self.flipBlaster()
                self.facing = "right"
                self.rect.topleft = (125,305)
            if self.angle > 90:
                self.angle = 90
            if self.angle < -90:
                self.angle = -90
        else:
            if owner.facing != self.facing:
                self.flipBlaster()
                self.facing = "left"
                self.rect.topleft = (100,305)
            if 0 <= self.angle <= 89:
                self.angle = 90
            elif -89 <= self.angle <= -0:
                self.angle = -90
        
    
        px, py = owner.hitbox.center
        if self.facing == "right":
            self.rect.topleft = (px,py - 7)
        else:
            self.rect.topright = (px,py - 7)
        if(owner.type == "player" and owner.states["running"]) or (owner.type == "enemy" and owner.state == "patrol"):
            if owner.frame_num % 2 == 0:
                self.rect.centery += 1
            else:
                self.rect.centery -= 4


        return r_surf, r_rect

    #draw blaster on screen
    def draw(self,SCREEN, owner, target_pos):
        for b in self.bullets: b.draw(SCREEN)
        if self.showing == True:
            r_surf, r_rect = self.rotate_towards(owner, target_pos)
            SCREEN.blit(r_surf, r_rect)
            # mouse_pos = pygame.mouse.get_pos()
            # self.angle = self.calculateAngle(self.rect.topleft, mouse_pos)
            # if player.facing == "right": 
            #     if player.facing != self.facing:
            #         self.flipBlaster()
            #         self.facing = "right"
            #         self.rect.topleft = (125,305)
            #     if self.angle > 90:
            #         self.angle = 90
            #     if self.angle < -90:
            #         self.angle = -90
            # else:
            #     if player.facing != self.facing:
            #         self.flipBlaster()
            #         self.facing = "left"
            #         self.rect.topleft = (100,305)
            #     if 0 <= self.angle <= 89:
            #         self.angle = 90
            #     elif -89 <= self.angle <= -0:
            #         self.angle = -90
            
        
            # px, py = player.boundary_rect.center
            # if self.facing == "right":
            #     self.rect.topleft = (px,py - 7)
            # else:
            #     self.rect.topright = (px,py - 7)
            # if player.states["running"]:
            #     if player.frame_num % 2 == 0:
            #         self.rect.centery += 1
            #     else:
            #         self.rect.centery -= 4
