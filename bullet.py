import pygame
from sprite import Sprite
class Bullet(Sprite):

    def __init__(self, startpos, speed, color, size):
        self.pos = startpos
        self.speed = speed
        self.color = color
        self.size = size
        self.rect = pygame.Rect(startpos, size)

    #shoots bullet to target
    def shoot(self, targetpos):
        pass

    #checks for collision
    def collide(self):
        pass

    #draws square bullet on screen
    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        
