import pygame
from sprite import Sprite
import math
class Bullet(Sprite):

    def __init__(self, startpos, speed, color, size):
        # Sprite.__init__(self,startpos, size, "")
        self.pos = startpos
        self.speed = speed
        self.color = color
        self.size = size
        self.rect = pygame.Rect(startpos, size)
        self.mask = pygame.mask.Mask((self.rect.width, self.rect.height))
        self.mask.fill()
        self.dx = 0
        self.dy = 0

        self.center = pygame.Vector2(self.rect.center)
        self.vector = pygame.Vector2()
        self.angle = 0


    #shoots bullet to target
    def shoot(self, targetpos):
        #get x distance
        x_distance = targetpos[0] - self.rect.centerx

        #get y distance
        y_distance = targetpos[1] - self.rect.centery

        #get angle
        self.angle = math.atan2(y_distance, x_distance)
        self.angle = math.degrees(self.angle)
        self.vector.from_polar((1,self.angle))


    #checks for collision
    def collide(self):
        pass

    #draws square bullet on screen
    def draw(self, SCREEN):
        self.center += self.vector * self.speed
        self.rect.center = self.center

        pygame.draw.rect(SCREEN, self.color, self.rect)
        
