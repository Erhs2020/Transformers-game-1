import pygame
from sprite import Sprite
class Bullet(Sprite):

    def __init__(self, startpos, speed, color, size):
        self.pos = startpos
        self.speed = speed
        self.color = color
        self.size = size
        self.rect = pygame.Rect(startpos, size)
        self.dx = 0
        self.dy = 0

    #shoots bullet to target
    def shoot(self, targetpos):
        
        #get x distance
        x_distance = targetpos[0] - self.rect.centerx
        self.dx = x_distance/self.speed

        #get y distance
        y_distance = targetpos[1] - self.rect.centery
        self.dy = y_distance/self.speed

    #checks for collision
    def collide(self):
        pass

    #draws square bullet on screen
    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        self.rect.move_ip((self.dx, self.dy))
        
