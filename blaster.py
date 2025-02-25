import pygame
from sprite import Sprite
from bullet import Bullet
import time

MAX_AMMO = 1
class Blaster(Sprite):
    
    def __init__(self):
        Sprite.__init__(self,(125,305), (26,13), "OPBlaster.png")
        self.angle = 0
        self.facing = "right"
        self.starting_pos = self.rect.bottomleft
        self.bullets = []
        self.ammo = MAX_AMMO
        self.showing = False

        #time stuff
        self.start_time = None
        self.reloadtime = 0.2
        self.stoptime = None

    #shoots bullet at target
    def shoot(self, pos):
        self.start_time = time.time()
        if self.ammo > 0 and self.showing:
            # make bullet at blaster 
            bullet = Bullet(self.rect.center, 10, (252,109,0), (10,10))
            self.bullets.append(bullet)
            # make bullet go to mouse cursor/ pos
            bullet.shoot(pos)
            self.ammo -= 1
            # Make bullet keep moving until hit edge
        else:
            #check if there's a start and stop time
            if self.start_time != None and self.stoptime != None:
                #check if 2 seconds have passed
                if time.time() > self.stoptime:
                    #reset ammo and timers
                    self.ammo = MAX_AMMO
                    self.start_time = None
                    self.stoptime = None
            else:
                #set timers aka start the reload
                self.start_time = time.time()
                self.stoptime = self.start_time + self.reloadtime

            

            


    
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

    #draw blaster on screen
    def draw(self,SCREEN, player):
        for b in self.bullets: b.draw(SCREEN)
        if self.showing == True:
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
