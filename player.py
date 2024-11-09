import pygame
from sprite import Sprite
from blaster import Blaster

class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self,(0,180),(600,600), "OPRun.png")
        self.blaster = Blaster()
        self.animationChange("OP IDLE")
        self.mode = "robot"
        self.blaster_visable = False
        self.size = (600,600)

        #jumping variables
        self.velocity_y = 0
        self.gravity = 1
        self.jump_height = 15
        self.on_ground = True
        self.start_y = self.rect.bottom

        #set up player clock
        self.clock = pygame.time.Clock()
        self.ticks = 0
       
        self.states = {
            "running": False,
            "idle": True,
            "transforming": False,
            "driving": False,
            "shooting": False,
            "gettingBlaster": False,
            "blasterPutAway": False,



        }
    
    #resets player state to idle 
    def resetStates(self):
        if self.states["transforming"] == False and self.states["gettingBlaster"] == False and self.states["blasterPutAway"] == False:
            for state in self.states:
                self.states[state] = False
            if self.mode == "robot":
                self.states["idle"] = True 
                if self.blaster_visable == False:
                    self.animationChange("OP IDLE") 
                else:
                    self.animationChange("OP BLASTER IDLE")
                    
            if self.mode == "car":
                self.states["driving"] = True 
                self.animationChange("OP DRIVE IDLE")
    
    # checks if player is colliding with the platform masks: returns true is player overlapping with platform masks, returns false if not
    def collidedWithPlatforms(self, platforms_list):
        for platform in platforms_list:
            collision_offset = pygame.sprite.collide_mask(self, platform)
            if collision_offset:
                collision_point = self.mask.overlap(platform.mask, collision_offset)
                boundary_rect = self.get_mask_rect(self.mask,self.rect.topleft)

                if collision_point and boundary_rect.top >= platform.rect.top:
                    #collided on left side of the platform.
                    if boundary_rect.left <= platform.rect.left + 10:
                        return "left"
                    #collided on right side of the plaform.
                    if boundary_rect.right >= platform.rect.right - 10:
                        return "right"
        return False
    

    def update(self,screen, platforms_list):
        self.handlekeypress()
        
        #apple some vertival movemnt
        self.rect.move_ip(0,-self.velocity_y)
        if self.on_ground == False:
            self.velocity_y -= self.gravity
        
        #reset the ground state
        self.on_ground = False 
        
        #check for collision with the platforms using masks
        for platform in platforms_list.getTiles():
            #check for mask collision
            offset = (platform.rect.x - self.rect.x, platform.rect.y - self.rect.y)
            collision_point = self.mask.overlap(platform.mask, offset)
            boundary_rect = self.get_mask_rect(self.mask,self.rect.topleft)
            self.universeal_rect = self.get_universal_hitbox(self.rect.left + 50, self.rect.top + 50)

            #check if there is a collision point
            # if platform.rect.collidepoint((self.rect.left + 82, self.rect.top + 70)):
            
            #player falling
            if collision_point and self.velocity_y < 0:
                if boundary_rect.bottom > platform.rect.top and (boundary_rect.right >= platform.rect.left + 10 and boundary_rect.left <= platform.rect.right - 10):
                    downoffset = boundary_rect.bottom - self.rect.top
                    boundary_rect.bottom = platform.rect.top
                    self.rect.top = boundary_rect.bottom - downoffset
                    self.on_ground = True
                    self.velocity_y = 0

            elif collision_point:
                #player hit roof of platform
                if self.velocity_y > 0:
                    if boundary_rect.top < platform.rect.bottom and (boundary_rect.right >= platform.rect.left + 10 and boundary_rect.left <= platform.rect.right - 10):
                        upoffset = boundary_rect.top - self.rect.top
                        boundary_rect.top = platform.rect.bottom
                        self.rect.top = boundary_rect.top - upoffset
                        self.velocity_y = 0
                


        #Ensure the player doesn't fall through the ground
        if self.rect.centery >= 519:
            self.rect.centery = 519
            self.on_ground = True
            self.velocity_y = 0

        # collided = self.collidedWithPlatforms(platforms_list.getTiles())
        # #handle jump
        # self.rect.move_ip((0,-self.velocity_y))
        # if not self.on_ground:
        #     if collided or self.rect.bottom >= self.start_y:
        #         self.on_ground = True
        #         self.velocity_y = 0
        #         print(self.rect.bottom, self.start_y)
        #     self.velocity_y -= self.gravity

        #draws collision bordor for player
        #create mask from currently animation surface frame
        self.mask = pygame.mask.from_surface(self.surf[self.frame_num])
    

        #Find the bounding box of the opaque region 
        # if self.mask.count() > 0: #Ensure there are opaque pixels
        #     mask_surface = self.mask.to_surface(setcolor=(0,255,0,255), unsetcolor=(0,0,0,0))
        #     screen.blit(mask_surface, self.rect.topleft)

        #draw collision bordor for platforms
        platform_tiles = platforms_list.getTiles()
        for tile in platform_tiles:
            tile.draw_collsion_box(screen)
            pygame.draw.circle(screen, (0,0,255), tile.rect.center, 5)

        if self.states["transforming"] == True:
            if self.mode == "car" and self.frame_num > 7: self.states["transforming"] = False
            elif self.mode == "robot" and self.frame_num == 0: self.states["transforming"] = False

        if self.states["gettingBlaster"] == True:
            if self.frame_num > 5: 
                self.states["gettingBlaster"] = False
                self.blaster_visable = True
                self.resetStates()
               

        if self.states["blasterPutAway"] == True:
            if self.frame_num < 1: 
                self.states["blasterPutAway"] = False
               
            
            

        pygame.draw.rect(screen, (255, 0, 0), self.rect,2)
        
        # pygame.draw.rect(screen, (255, 0, 0), self.universeal_rect,2)

        mask_rect = self.get_mask_rect(self.mask, self.rect.topleft)
        pygame.draw.rect(screen,(0,255,0), mask_rect, 2)

        # start_pos = (self.rect.left + 82, self.rect.top + 70)
        # end_pos = (self.rect.left + 100, self.rect.top + 70)
        # pygame.draw.line(screen, (0,255,0), start_pos,end_pos)

        
        #keep playing animation by indexing from animation list.
        self.surf = self.rightAnim if self.facing == "right" else self.leftAnim
        screen.blit(self.surf[self.frame_num], self.rect.topleft)

        if self.blaster_visable == True:
            self.blaster.draw(screen, self, self.states, self.frame_num, self.facing)

        #get time since game started in ms
        # t = self.clock.get_time() 
        # modified_t = int(t /100)

        #if modified time is divisible by 10
        if self.ticks % 10 == 0:
            if (self.mode == "robot" and self.states["transforming"]) or self.states["blasterPutAway"]:
                self.updateAnimNumberBackwards()
            else:
                self.updateAnimNumber()
        self.ticks +=1

        
    #handles key presses based on key pressed update player animation and trigger any side effects
    def handlekeypress(self):
        pressed_keys = pygame.key.get_pressed()

        #running
        if not self.states["transforming"] and not self.states["gettingBlaster"] and not self.states["blasterPutAway"]:
            #run right
            if pressed_keys[pygame.K_d]:
                self.facing = "right"
                if not self.states["running"]:
                    if self.mode == "robot":
                        if self.blaster_visable == False:
                            self.animationChange("OP RUN") 
                        else:
                            self.animationChange("OP BLASTER RUN")
                    elif self.mode == "car":
                        self.animationChange("OP DRIVE") 
                    self.states["running"] = True
                    

            #run left
            elif pressed_keys[pygame.K_a]:
                self.facing = "left"
                if not self.states["running"]:
                    if self.mode == "robot":
                        if self.blaster_visable == False:
                            self.animationChange("OP RUN") 
                        else:
                            self.animationChange("OP BLASTER RUN") 
                    elif self.mode == "car":
                        self.animationChange("OP DRIVE") 
                    self.states["running"] = True
            #transform
            elif pressed_keys[pygame.K_s]:
                if not self.states["transforming"]:
                    self.states["transforming"] = True
                    self.states["running"] = False
                    self.animationChange("OP TRANSFORM")
                    if self.mode == "robot":
                        self.mode = "car"
                    else:
                        self.mode = "robot"
                        self.frame_num = 8
            else:
                self.resetStates()
                        
            #jumping
            if pressed_keys[pygame.K_w] and self.on_ground and not self.states["transforming"] and self.mode == "robot":
                self.velocity_y = self.jump_height
                self.rect.move_ip((0,-self.velocity_y))
                self.on_ground = False

            if pressed_keys[pygame.K_LSHIFT]:
                if not self.states["gettingBlaster"] and self.blaster_visable == False:
                    self.states["gettingBlaster"] = True
                   
                    self.animationChange("OP GET BLASTER")
            elif not pressed_keys[pygame.K_LSHIFT] and not self.states["blasterPutAway"] and self.blaster_visable:
                    self.states["blasterPutAway"] = True
                    self.blaster_visable = False
                    self.animationChange("OP GET BLASTER")
                    self.frame_num = 6
                    
                
                   
            
                
        #idle
            elif not self.states["running"]:
                self.resetStates()


             



    


        