import pygame
from sprite import Sprite
from bullet import Bullet
import math
import time

class Blaster(Sprite):
    
    def __init__(self):
        Sprite.__init__(self,(125,305), (384,384), "Optimus Prime Blaster NEW.png")
        self.angle = 0
        self.facing = "right"
        self.starting_pos = self.rect.bottomleft
        self.bullets = []
        self.showing = False
        self.pivot = [self.rect.left, self.rect.top]
        self.pivot_offset = pygame.math.Vector2(10, 0)
        self.shoot_pos = (0,0)
        # self.shoot_offset = pygame.math.Vector2(50, 0)

        #og size (26,13)


    #shoots bullet at target
    def shoot(self, pos):
        if self.showing:
            # make bullet at blaster
            rad = math.radians(self.angle)
            offset_x, offset_y = (200,0)
            rx = offset_x * math.cos(rad) - offset_y * math.sin(rad)
            ry = offset_x * math.sin(rad) - offset_y * math.cos(rad)
            tip_x = self.pivot[0] + rx
            tip_y = self.pivot[1] - ry
            self.shoot_pos = (tip_x, tip_y)
            bullet = Bullet(self.shoot_pos, 40, (252,109,0), (20,20))
            self.bullets.append(bullet)
            # make bullet go to mouse cursor/ pos
            bullet.shoot(self.angle)
            
    
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
        if owner.type == "player":
            px, py = owner.hitboxDict[owner.mode]["rect"].topleft
            if not owner.states["running"]:
                if self.facing == "right":
                    self.pivot = [px - 15,py + 35]
                else:
                    self.pivot = [px + 55,py + 35]
            elif owner.states["running"]:
                if self.facing == "right":
                    self.pivot = [px - 8,py + 35]
                else:
                    self.pivot = [px + 30,py + 35]
                if(owner.type == "player" and owner.states["running"]) or (owner.type == "enemy" and owner.state == "patrol"):
                    if owner.frame_num % 2 == 0:
                        self.pivot[0] += 10
                        self.pivot[1] -= 1
                    else:
                        self.pivot[0] += 10
                        self.pivot[1] -= 4


        # r_surf, r_rect = self.rotateSprite(self.angle)
        self.angle = self.calculateAngle(self.pivot, pos)
        r_surf, r_rect = self.rotateAroundPoint(-self.angle, self.pivot, self.pivot_offset)
        if owner.facing == "right": 
            # print(owner.facing, self.facing)
            if owner.facing != self.facing:
                self.flipBlaster()
                self.facing = "right"
                # self.rect.topleft = (125,305)
            # if self.angle > 90:
            #     self.angle = 90
            # if self.angle < -90:
            #     self.angle = -90
        else:
            if owner.facing != self.facing:
                self.flipBlaster()
                self.facing = "left"
                # self.rect.topleft = (100,305)
            # if 0 <= self.angle <= 89:
            #     self.angle = 90
            # elif -89 <= self.angle <= -0:
            #     self.angle = -90
    

        return r_surf, r_rect

    #draw blaster on screen
    def draw(self,SCREEN, owner, target_pos):
        for b in self.bullets: b.draw(SCREEN)
        if self.showing == True:
            r_surf, r_rect = self.rotate_towards(owner, target_pos)
            
            SCREEN.blit(r_surf, r_rect)
            pygame.draw.circle(SCREEN, (255, 230, 0), self.pivot, 10)
            pygame.draw.circle(SCREEN, (255, 100, 0), self.shoot_pos, 10)
            pygame.draw.line(SCREEN, (255, 10, 112), self.pivot, self.shoot_pos, 5)
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
