import pygame
from sprite import Sprite
from enemy import Enemy

WIDTH = 1400
HEIGHT = 800
E = -1 #used to specify enemy in level

class Platforms:
    def __init__(self, pos, structure, platforms_list, player, screen):
        self.pos = pos
        self.structure = structure
        self.platforms_list = platforms_list
        numRows = len(self.structure)
        numCols = len(self.structure[0])
        self.tiles = []
        self.tile_masks = []
        self.enemies = []
        self.player = player


        #set up platforms according to structure
        for row in range(numRows):
            for col in range(len(structure[row])):
                num = self.structure[row][col]
                w = 300
                h = 300
                xOffset, yOffset = self.pos
                x = xOffset + (col *  w)
                y = yOffset + (row * h)

                if num == E:
                    enemy = Enemy((x,y + h),"Regular",(w,h), self.player)
                    self.enemies.append(enemy)

                elif num != 0:
                    tile = Sprite((x,y), (w,h), "Platforms.png")
                    tile.change_surf_to(self.platforms_list[num - 1])
                    self.tiles.append(tile)

        print(len(self.tiles))

    def set_player(self, player):
        self.player = player

    def move_platforms(self, speed):
        for i in range(len(self.tiles)):
            self.tiles[i].rect.move_ip(speed,0)
    
    def move_enemies(self, speed):
        for i in range(len(self.enemies)):
            self.enemies[i].move(speed)

    def draw(self, screen):
        "if tile xpos in screenbox(min: 0, max: WIDTH)"
        for tile in self.tiles:
            if tile.rect.left < WIDTH and tile.rect.right > 0:
                tile.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
    
    #returns self.tiles
    def getTiles(self):
        return self.tiles
    
    def getEnemies(self):
        return self.enemies