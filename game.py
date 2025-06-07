import pygame
from player import Player
from platforms import Platforms

class Game:
    def __init__(self,SCREEN, WIDTH, HEIGHT, PLATFORMS_LIST):
        self.SCREEN = SCREEN
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.level = 0  #0 = hubworld
        self.scene = "hubworld"
        self.scroll_speed = 2
        self.running_scroll_speed = 4
        self.vehicle_scroll_speed = 6
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
        
        #LEVELZ Creation

        #to be moved later ~ testing
        E = -1 #used to specify enemy in level
        level_1 = Platforms(
            pos =(0,-250),
            structure = [
                # [0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                # [0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0,0,3,1,1,3,0,0,3,1,1,3,0],
                [0,0,0,0,0,0,0,3,1,1,1,1,2,2,1,1,0,1,2,2,1,0]
            ],
            platforms_list = PLATFORMS_LIST,
            player = self.player,
            screen = self.SCREEN
        )
        self.LEVELS = [level_1]





    
    def scroll(self,scrollDirection):

    

        speed = self.scroll_speed
        floor_speed_mult = 2
        pressed_keys = pygame.key.get_pressed()
        if self.player.states["running"] and pressed_keys[pygame.K_LSHIFT]:
            speed = self.running_scroll_speed
        
            
       
        "If scroll direction is right"
        "floor1 = leader"
        "floor2 = follower"


        "if leader topleft is at edge"
        "leader topright go to follower topleft"
        "leader = follower"
        "follower = leader"


        
        if scrollDirection == "right": #looks like player moving right
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
            self.LEVELS[self.level].move_enemies((-speed)*floor_speed_mult)

            
        if scrollDirection == "left": #looks like player moving left 
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
            self.LEVELS[self.level].move_enemies((speed)*floor_speed_mult)

       
        
            
            
    def checkcollision(self):
        #tools:
        
        #to get platforms --> self.LEVELS[self.level].getTiles()
        #to get enemies --> self.LEVELS[self.level].getEnemeis()
        platforms_list = self.LEVELS[self.level].getTiles()
        self.enemies = self.LEVELS[self.level].getEnemies()
        
        #to get player --> self.player
        #to get blaster (player blaster) --> self.player.blaster
        #to check for collision --> the blaster object contains the hit methord


        #check for collision between player and enemy bullets and platform
        for platform in platforms_list:
            plaforms_boundary_rect = platform.get_mask_rect(platform.mask, platform.rect.topleft)
            if self.player.blaster.hit(platform) == True:
                print("player hit platform")
            # if enemy.blaster.hit(platform) == True:
            #     print("enemy hit platform")

        #check for collision between player bullets and enemies and player
        for enemy in self.enemies:
            if self.player.blaster.hit(enemy) == True:
                print("player hit enemy")
            # if enemy.blaster.hit(self.player) == True:
            #     print("enemy hit player")




    def PLAY_DA_GAME(self):
        #Scroll away from wall
        platforms_list = self.LEVELS[self.level].getTiles()
        pressed_keys = pygame.key.get_pressed() #returns list of certain booleans of what keys are pressed.
        
        collided = self.player.collidedWithPlatforms(platforms_list)
        self.checkcollision()
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



        