import pygame
from player import Player

class Game:
    def __init__(self,SCREEN, WIDTH, HEIGHT, LEVELS):
        self.SCREEN = SCREEN
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.LEVELS = LEVELS

        self.level = 0  #0 = hubworld
        self.scene = "hubworld"
        self.scroll_speed = 1
        self.running_scroll_speed = 3
        self.direction = "right"


        #background objects setup
        self.bg_surf1 = pygame.image.load("Images/Background_objects.png").convert_alpha()
        self.bg_surf1 = pygame.transform.scale(self.bg_surf1, (self.WIDTH, self.HEIGHT))
        self.bg_rect1 = self.bg_surf1.get_rect(topleft=(0,5))
        self.bg_surf2 = self.bg_surf1.copy()
        self.bg_rect2 = self.bg_rect1.copy()
        self.bg_rect2.left = self.WIDTH

        #ground setup
        self.floor_surf1 = pygame.image.load("Images/FLOOR.png").convert_alpha()
        self.floor_surf1 = pygame.transform.scale(self.floor_surf1, (self.WIDTH, self.HEIGHT))
        self.floor_rect1 = self.floor_surf1.get_rect(topleft=(0,0))
        self.floor_surf2 = self.floor_surf1.copy()
        self.floor_rect2 = self.floor_rect1.copy()
        self.floor_rect2.left = self.WIDTH
        
        self.floor_leader = self.floor_rect1
        self.floor_follower = self.floor_rect2
        self.bg_leader = self.bg_rect1
        self.bg_follower = self.bg_rect2

        #player stuff
        self.player = Player()

    
    def scroll(self,scrollDirection):

    

        speed = self.scroll_speed
        floor_speed_mult = 2
        
        if self.player.states["running"] and self.player.mode == "car":
            speed = self.running_scroll_speed
            
       
        "If scroll direction is right"
        "floor1 = leader"
        "floor2 = follower"


        "if leader topleft is at edge"
        "leader topright go to follower topleft"
        "leader = follower"
        "follower = leader"

        
        
    

        
        if scrollDirection == "right":
            if self.bg_rect1.right <= 0:
                self.bg_rect1.left = self.bg_rect2.right
            if self.bg_rect2.right <= 0:
                self.bg_rect2.left = self.bg_rect1.right
            if self.floor_rect1.right <= 0:
                self.floor_rect1.left = self.floor_rect2.right
            if self.floor_rect2.right <= 0:
                self.floor_rect2.left = self.floor_rect1.right
            self.bg_rect1.move_ip((-speed),0)
            self.floor_rect1.move_ip((-speed)*floor_speed_mult,0)
            self.bg_rect2.move_ip((-speed),0)
            self.floor_rect2.move_ip((-speed)*floor_speed_mult,0)
            self.LEVELS[self.level].move_platforms((-speed)*floor_speed_mult)

                
            
            
           
            
        if scrollDirection == "left":
            if self.bg_rect1.left >= self.WIDTH:
                self.bg_rect1.right = self.bg_rect2.left
            if self.bg_rect2.left >= self.WIDTH:
                self.bg_rect2.right = self.bg_rect1.left
            if self.floor_rect1.left >= self.WIDTH:
                self.floor_rect1.right = self.floor_rect2.left
            if self.floor_rect2.left >= self.WIDTH:
                self.floor_rect2.right = self.floor_rect1.left
            self.bg_rect1.move_ip((speed),0)
            self.floor_rect1.move_ip((speed)*floor_speed_mult,0)
            self.bg_rect2.move_ip((speed),0)
            self.floor_rect2.move_ip((speed)*floor_speed_mult,0)
            self.LEVELS[self.level].move_platforms((speed)*floor_speed_mult)

       
        
            
            
           



    def PLAY_DA_GAME(self):
        

        #Scroll away from wall
        platforms_list = self.LEVELS[self.level].getTiles()
        pressed_keys = pygame.key.get_pressed() #returns list of certain booleans of what keys are pressed.
        
        collided = self.player.collidedWithPlatforms(platforms_list)
        if collided == "left":
            self.scroll("left")
        elif collided == "right":
            self.scroll("right")
        elif pressed_keys[pygame.K_a]: 
            self.scroll("left")
        elif pressed_keys[pygame.K_d]: 
            self.scroll("right")
        
        self.SCREEN.blit(self.floor_surf1,self.floor_rect1)
        self.SCREEN.blit(self.bg_surf1,self.bg_rect1)
        self.SCREEN.blit(self.floor_surf2,self.floor_rect2)
        self.SCREEN.blit(self.bg_surf2,self.bg_rect2)

        self.LEVELS[self.level].draw(self.SCREEN)
        
        
        self.player.update(self.SCREEN, self.LEVELS[self.level])


        