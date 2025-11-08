import pygame
from sprite import Sprite
import random
import time
from player import Player
from blaster import Blaster

ENEMY_HITBOX_OFFSET_LEFT = 195
ENEMY_HITBOX_OFFSET_TOP = 190
ENEMY_HITBOX_WIDTH = 50
ENEMY_HITBOX_HEIGHT = 220
class Enemy(Sprite):

    def __init__(self, pos, type, PLATFORM_SIZE, player):
      Sprite.__init__(self,pos,(600,600), "Enemies/Enemy Walk.png")
      self.blaster = Blaster()
      self.blaster.showing = True
      self.type = "enemy"

      self.state = "patrol"
      self.dead = False
      self.facing = "left"
      self.startpos = [pos[0], pos[1]]
      self.farthest_left = pos[0] - PLATFORM_SIZE[0] * 1.5
      self.farthest_right = pos[0] + PLATFORM_SIZE[0] * 1.5
      self.steps = 0
      self.animationChange("ENEMY IDLE")
      self.frame_num = 0
      self.boundary_rect = self.get_mask_rect(self.mask, self.rect.topleft)
      offsety = self.boundary_rect.top - self.rect.top
      offsetx = self.boundary_rect.left - self.rect.left
      self.rect.top = self.rect.top - offsety - (self.boundary_rect.bottom - self.boundary_rect.top)
      self.rect.left = self.rect.left - offsetx
      self.rect.centerx = pos[0]
      self.rect.centery = pos[1]
      self.enemyrangeX = 150
      self.enemyrangeY = 60
      self.speed = 0

      #time stuffz
      self.start_time = time.time()
      self.min_wait = 3
      self.max_wait = 5
      self.stoptime = self.start_time + random.uniform(self.min_wait,self.max_wait)

      #shoot stuffz
      self.shoot_start_time = time.time()
      self.shoot_min_wait = 0
      self.shoot_max_wait = 1
      self.shoot_stoptime = self.start_time + random.randint(self.shoot_min_wait,self.shoot_max_wait)

      #player
      self.player = player
      self.ticks = 0

      #hitbox STuffz
      self.enemy_hitbox_rect = pygame.Rect(self.boundary_rect.bottomleft, (ENEMY_HITBOX_WIDTH, ENEMY_HITBOX_HEIGHT))
      self.enemy_hitbox_mask = pygame.mask.Mask((self.enemy_hitbox_rect.width, self.enemy_hitbox_rect.height))
      self.enemy_hitbox_mask.fill()
    

      
    

    def draw(self, screen): #use speed to update farthest pos
        self.enemy_hitbox_rect.center = self.rect.center
        self.patrol()
        self.spotPlayer(self.player)
        if self.ticks % 10 == 0:
            self.updateAnimNumber()
        self.ticks +=1

        #shoot
        if self.state == "spotplayer" and time.time() > self.shoot_stoptime:
          self.shoot_start_time = time.time()
          self.shoot_stoptime = self.start_time + random.randint(self.shoot_min_wait * 1000,self.shoot_max_wait * 1000)
          self.blaster.shoot(self.player.boundary_rect.center)
          print("shoot")


        pygame.draw.line(screen, (149, 52, 235), (self.farthest_left, self.enemy_hitbox_rect.centery), (self.farthest_right, self.enemy_hitbox_rect.centery),5)

        #keep playing animation by indexing from animation list.
        self.surf = self.rightAnim if self.facing == "right" else self.leftAnim
        screen.blit(self.surf[self.frame_num], self.rect.topleft)
        
        #draw blaster
        self.blaster.draw(screen, self, (0,0))
        
        pygame.draw.rect(screen, (100, 100, 100), self.enemy_hitbox_rect)
        # pygame.draw.rect(screen, (10, 100, 2), self.rect)
        pygame.draw.circle(screen, (20, 20, 20), self.startpos, 20)

    def move(self, speed):
      self.farthest_left += speed
      self.farthest_right += speed
      self.speed = random.randint(1, 3)
      
      self.rect.move_ip(speed, 0) #make enemy follow background

    def patrol(self):
      # self.enemy_hitbox_rect = self.get_mask_rect(self.mask, self.rect.topleft)

      if self.state == "spotplayer":
        """
        todo:
        make sure to account for facing.
        keep moving in direction of facing until hit edge.
        """

        if self.facing == "left" and self.enemy_hitbox_rect.left > self.farthest_left:
          self.rect.move_ip(-self.speed, 0)
        if self.facing == "right" and self.enemy_hitbox_rect.right < self.farthest_right:
          self.rect.move_ip(self.speed, 0)

      if self.state == "patrol":
        if self.enemy_hitbox_rect.left <= self.farthest_left:
          self.facing = "right"
        if self.enemy_hitbox_rect.right >= self.farthest_right:
          self.facing = "left"
        if self.facing == "right":
          self.rect.move_ip(self.speed, 0)
        elif self.facing == "left":
          self.rect.move_ip(-self.speed, 0)
      
      
      if self.state == "patrol" and time.time() >= self.stoptime:
        self.state = "idle"
        self.start_time = time.time()
        self.stoptime = self.start_time + random.uniform(1,2)
      if self.state == "idle" and time.time() >= self.stoptime:
        self.state = "patrol"
        self.facing = random.choice(["right","left"])
        self.start_time = time.time()
        self.stoptime = self.start_time + random.uniform(self.min_wait,self.max_wait)

    def spotPlayer(self, player):
      if abs(player.boundary_rect.centerx - self.enemy_hitbox_rect.centerx) < self.enemyrangeX and abs(player.boundary_rect.centery - self.enemy_hitbox_rect.centery) < self.enemyrangeY:
        print("spotted")
        self.state = "spotplayer"
        if self.enemy_hitbox_rect.centerx < player.boundary_rect.centerx:
          self.facing = "right"
        else:
          self.facing = "left"
      else:
        self.state = "patrol"
      #check if state stays in spot player
      
        

      
      
          #current time in secords time.time()
          #random.choice(LIST) picks random element from list

          
