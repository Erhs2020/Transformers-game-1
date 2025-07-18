import pygame
from sprite import Sprite
from blaster import Blaster
import time

MAX_AMMO = 1
GROUNDY = 650
HITBOX_OFFSET_LEFT = 195
HITBOX_OFFSET_TOP = 190
HITBOX_WIDTH = 50
HITBOX_HEIGHT = 220
class Player(Sprite):

    def __init__(self):
        Sprite.__init__(self,(0,180),(384, 384), "OPRun.png")
        self.animationChange("OP IDLE")
        self.mode = "robot"
        # self.size = (768,768)
        self.type = "player"

        #hitbox
        self.hitbox = pygame.Rect(self.boundary_rect.bottomleft, (HITBOX_WIDTH, HITBOX_HEIGHT))
        self.hitbox_mask = pygame.mask.Mask((self.hitbox.width, self.hitbox.height))
        self.hitbox_mask.fill()

        #jumping variables
        self.velocity_y = 0
        self.gravity = 2
        self.jump_height = 20
        self.on_ground = True
        self.start_y = self.rect.bottom

        #blaster stuffz
        self.blaster = Blaster()
        self.ammo = MAX_AMMO
        self.start_time = None
        self.reloadtime = 0.2
        self.stoptime = None

        #set up player clock
        self.clock = pygame.time.Clock()
        self.ticks = 0
       
        self.states = {
            "running": False,
            "idle": True,
            "jumping": False,
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
                if self.blaster.showing == False:
                    self.animationChange("OP IDLE") 
                else:
                    self.animationChange("OP BLASTER IDLE")
                    
            if self.mode == "car":
                self.states["driving"] = True 
                self.animationChange("OP DRIVE IDLE")
    
    # checks if player is colliding with the platform masks: returns true is player overlapping with platform masks, returns false if not
    def collidedWithPlatforms(self, platforms_list):
        for platform in platforms_list:
            # self.boundary_rect = self.get_mask_rect(self.mask,self.rect.topleft)
            offset = (platform.rect.x - self.hitbox.x, platform.rect.y - self.hitbox.y)
            collision_point = self.hitbox_mask.overlap(platform.mask, offset)

            if collision_point and self.hitbox.bottom > platform.boundary_rect.top + 10: #and (self.boundary_rect.bottom >= GROUNDY - 10) or self.boundary_rect.bottom >= platform.boundary_rect.top - 10):
                #collided on left side of the platform.
                if self.hitbox.left <= platform.boundary_rect.left:
                    return "left"
                #collided on right side of the plaform.
                if self.hitbox.right >= platform.boundary_rect.right:
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
        self.hitbox.center = (self.rect.left + HITBOX_OFFSET_LEFT, self.rect.top + HITBOX_OFFSET_TOP)
        
        #check for collision with the platforms using masks
        for platform in platforms_list.getTiles():
            #check for mask collision
            offset = (platform.rect.x - self.hitbox.x, platform.rect.y - self.hitbox.y)
            collision_point = self.hitbox_mask.overlap(platform.mask, offset)

            if collision_point:
                #player falling
                if self.velocity_y < 0 and self.hitbox.bottom <= platform.boundary_rect.top + 50:
                    offset_from_top = self.hitbox.bottom - self.rect.top
                    self.hitbox.bottom = platform.boundary_rect.top
                    self.rect.top = self.hitbox.bottom - offset_from_top
                    self.velocity_y = 0
                    self.on_ground = True
                    #platform.color = (0, 255, 0)

            # Check hitting head on bottom of platform
                elif self.velocity_y > 0 and self.hitbox.top >= platform.boundary_rect.bottom - 10:
                    offset_from_top = self.hitbox.top - self.rect.top
                    self.hitbox.top = platform.boundary_rect.bottom
                    self.rect.top = self.hitbox.top - offset_from_top
                    self.velocity_y = -1
                    #platform.color = (255, 0, 0)
                


        #Ensure the player doesn't fall through the ground
        if self.hitbox.bottom >= GROUNDY:
            downoffset = self.hitbox.bottom - self.rect.top
            self.hitbox.bottom = GROUNDY - 1
            self.rect.top = self.hitbox.bottom - downoffset
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

        #hitbox draw
        pygame.draw.rect(screen, (0,255,0), self.hitbox)


        #create mask from currently animation surface frame
        self.mask = pygame.mask.from_surface(self.surf[self.frame_num])
    

        #Find the bounding box of the opaque region 
        # if self.mask.count() > 0: #Ensure there are opaque pixels
        #     mask_surface = self.mask.to_surface(setcolor=(0,255,0,255), unsetcolor=(0,0,0,0))
        #     screen.blit(mask_surface, self.rect.topleft)

        #draw collision bordor for platforms
        # platform_tiles = platforms_list.getTiles()
        # for tile in platform_tiles:
            # tile.draw_collsion_box(screen)
            # pygame.draw.circle(screen, (0,0,255), tile.rect.center, 5)

        if self.states["transforming"] == True:
            if self.mode == "car" and self.frame_num > 7: self.states["transforming"] = False
            elif self.mode == "robot" and self.frame_num == 0: self.states["transforming"] = False

        if self.states["gettingBlaster"] == True:
            if self.frame_num > 1: 
                self.states["gettingBlaster"] = False
                self.blaster.showing = True
                self.resetStates()
               

        if self.states["blasterPutAway"] == True:
            if self.frame_num < 6: 
                self.states["blasterPutAway"] = False
        

        
        if self.states["jumping"] == True:
            if self.frame_num > 0: #change number later :)
                self.states["jumping"] = False
                self.states["running"] = False
                self.resetStates()
                print("running")
            
            

        # pygame.draw.rect(screen, (255, 0, 0), self.rect,2)
        
        # pygame.draw.rect(screen, (255, 0, 0), self.universeal_rect,2)

        # mask_rect = self.get_mask_rect(self.mask, self.rect.topleft)
        # pygame.draw.rect(screen,(0,255,0), mask_rect, 2)

        # start_pos = (self.rect.left + 82, self.rect.top + 70)
        # end_pos = (self.rect.left + 100, self.rect.top + 70)
        # pygame.draw.line(screen, (0,255,0), (0, GROUNDY), (500, GROUNDY), 6)

        
        #keep playing animation by indexing from animation list.
        self.surf = self.rightAnim if self.facing == "right" else self.leftAnim
        screen.blit(self.surf[self.frame_num], self.rect.topleft)

        #draw blaster
        mouse_pos = pygame.mouse.get_pos()
        self.blaster.draw(screen, self, mouse_pos)

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
                        if self.blaster.showing == False:
                            self.animationChange("OP RUN") 
                            print("d")
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
                        if self.blaster.showing == False:
                            self.animationChange("OP RUN") 
                        else:
                            self.animationChange("OP BLASTER RUN") 
                    elif self.mode == "car":
                        self.animationChange("OP DRIVE") 
                    self.states["running"] = True
            
            #transform
            if pressed_keys[pygame.K_s]:
                if not self.states["transforming"]:
                    self.states["transforming"] = True
                    self.states["running"] = False
                    self.animationChange("OP TRANSFORM")
                    if self.mode == "robot":
                        self.mode = "car"
                    else:
                        self.mode = "robot"
                        self.frame_num = 8
            # else:
            #     self.resetStates()
                        
            #jumping
            if pressed_keys[pygame.K_w] and self.on_ground and not self.states["transforming"] and self.mode == "robot":
                self.velocity_y = self.jump_height
                self.rect.move_ip((0,-self.velocity_y))
                self.on_ground = False
                self.states["jumping"] = True
                self.animationChange("OP JUMP")

            if pressed_keys[pygame.K_c]:
                if not self.states["gettingBlaster"] and self.blaster.showing == False:
                    self.states["gettingBlaster"] = True
                    self.blaster.showing = True
                   
                    # self.animationChange("OP GET BLASTER")
            elif not pressed_keys[pygame.K_c] and not self.states["blasterPutAway"] and self.blaster.showing:
                    self.states["blasterPutAway"] = True
                    self.blaster.showing = False
                    # self.animationChange("OP GET BLASTER")
                    self.frame_num = 6
            
            
            #shooting
            if pygame.mouse.get_pressed()[0]:
                self.start_time = time.time()
                if self.ammo > 0 and self.blaster.showing:
                    # make bullet at blaster 
                    self.blaster.shoot(pygame.mouse.get_pos())
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
                    
                
                   
            
                
            #idle
            pressingkey = True in pressed_keys
            if not pressingkey:
                self.resetStates()
            if pressed_keys[pygame.K_LSHIFT] and (not pressed_keys[pygame.K_a] and not pressed_keys[pygame.K_d]):
                self.resetStates()
            # if pressed_keys[pygame.K_w] and (not pressed_keys[pygame.K_a] and not pressed_keys[pygame.K_d])


             



    


        