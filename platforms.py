import pygame
from sprite import Sprite

class Platforms:
    def __init__(self, pos, structure, platforms_list):
        self.pos = pos
        self.structure = structure
        self.platforms_list = platforms_list
        numRows = len(self.structure)
        numCols = len(self.structure[0])
        self.tiles = []
        self.tile_masks = []

        #set up platforms according to structure
        for row in range(numRows):
            for col in range(len(structure[row])):
                num = self.structure[row][col]
                w = 60
                h = 60
                xOffset, yOffset = self.pos

                

                if num != 0:
                    x = xOffset + (col *  w)
                    y = yOffset + (row * h)
                    tile = Sprite((x,y), (w,h), "Platforms.png")
                    tile.change_surf_to(self.platforms_list[num - 1])
                    self.tiles.append(tile)
    def move_platforms(self, speed):
        for i in range(len(self.tiles)):
            self.tiles[i].rect.move_ip(speed,0)

    def draw(self, screen):
        
        for tile in self.tiles:
            tile.draw(screen)
    
    #returns self.tiles
    def getTiles(self):
        return self.tiles