import pygame
import math

animDictionary = {
    "OP RUN": {
        "numFrames": 8,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime walk.png"
    },
    "OP IDLE": {
        "numFrames": 1,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime idle.png"
    },
    "OP JUMP": {
        "numFrames": 4,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime jump3.png"
    },
    "OP TRANSFORM": {
        "numFrames": 9,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/OPTransform.png"
    },
     "OP DRIVE": {
        "numFrames": 1,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/OPDrive.png"

    },
    "OP DRIVE IDLE": {
        "numFrames": 1,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/OPDrive.png"

    },
    "OP GET BLASTER": {
        "numFrames": 7,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime walk No arm.png"

    },
    "OP BLASTER RUN": {
        "numFrames": 8,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime walk No arm.png"

    },
    "OP BLASTER IDLE": {
        "numFrames": 1,
        "numRows": 3,
        "numCols": 3,
        "allFramesImage": "Images/Optimus Prime idle.png"
    },
    
    
}

class Sprite(pygame.sprite.Sprite):
    

    def __init__(self,pos,size,image):
        pygame.sprite.Sprite.__init__(self)
        # self.surf = pygame.image.load("Images/"+image).convert_alpha()
        self.surf = pygame.image.load("Images/"+image)
        self.surf = pygame.transform.scale(self.surf,size)
        self.rect = self.surf.get_rect(topleft=pos)
        self.frame_num = 0
        self.facing = "right"
        self.size = size
        self.mask = pygame.mask.from_surface(self.surf)
        self.boundary_rect = self.get_mask_rect(self.mask,self.rect.topleft)
        
    
    def update_boundary_rect(self):
        self.boundary_rect.left = self.rect.left

    def change_surf_to(self, new_surf):
        self.surf = new_surf
        self.surf = pygame.transform.scale(self.surf, self.size)
        self.rect = self.surf.get_rect(topleft = self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.surf)
        self.boundary_rect = self.get_mask_rect(self.mask,self.rect.topleft)
    
    #draws red outline on sprite's mask border
    def draw_collsion_box(self, screen ):
        outline_points = self.mask.outline()
        ajusted_outline_points = [] #to be CONTINED DUN DUN DUNNNNNNNNNNNNNN
        for x,y in outline_points:
            adj_x = x + self.rect.left
            adj_y = y + self.rect.top
            ajusted_outline_points.append((adj_x, adj_y))

        if len(outline_points) > 1:
            pygame.draw.lines(screen, (255,0,0), True, ajusted_outline_points, 2)

    def draw(self,SCREEN):
        SCREEN.blit(self.surf,self.rect)

    def rotateSprite(self, angle):
        rotated_surf = pygame.transform.rotate(self.surf, angle)
        rotated_surface_rect = rotated_surf.get_rect(center = self.rect.center)
        return (rotated_surf, rotated_surface_rect)
    
    def rotateAroundPoint(self, angle, pivot, offset):
        rotated_image = pygame.transform.rotozoom(self.surf, -angle, 1) #Rotate image
        rotated_offset = offset.rotate(angle) #Rotate the offset vector
        rect = rotated_image.get_rect(center = pivot + rotated_offset)
        return rotated_image, rect 
    
    def calculateAngle(self, pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos1[1] - pos2[1]
        angle = math.atan2(dy,dx)
        angle = math.degrees(angle)
        return angle 

    
    def moveLeft(self,speed):
        self.rect.move_ip((-speed),0)
        self.facing = "left"
    
    def moveRight(self,speed):
        self.rect.move_ip((speed),0)
        self.facing = "right"
    
    
    def get_mask_rect(self, mask, offset):
        #extract the boundary points of mask
        boundary_points = mask.outline()
        
        if not boundary_points:
            #return none if there are no boundary points
            return None
    
        #offset boundary points by the provided offset
        rect_boundary_points = []

        for x,y in boundary_points:
            new_x = x + offset[0]
            new_y = y + offset[1]
            rect_boundary_points.append((new_x,new_y))
        
        #get the min and max x and y coordinates
        min_x = min(point[0] for point in rect_boundary_points)
        max_x = max(point[0] for point in rect_boundary_points)
        min_y = min(point[1] for point in rect_boundary_points)
        max_y = max(point[1] for point in rect_boundary_points)
        
        #create the mask rect
        mask_rect = pygame.Rect(min_x,min_y, max_x - min_x, max_y-min_y)

        return mask_rect
    
    def get_universal_hitbox(self, x, y):
        universal_rect = pygame.Rect(x,y,70,70)
        return universal_rect
        
        
    
    def getAnimFrameRegion(self, row, col):
        w = 384 / self.anim["numCols"]
        h = 384 / self.anim["numRows"]
        x = w * col
        y = h * row
        return (x, y, w, h)

    def updateAnimNumber(self):
        self.frame_num += 1
        if self.frame_num >= self.anim["numFrames"]:
            self.frame_num = 0

    def updateAnimNumberBackwards(self):
        self.frame_num -= 1
        if self.frame_num < 0:
            self.frame_num = self.anim["numFrames"] - 1
        

    def animationChange(self, anim):
        self.anim = animDictionary[anim]
        self.flipSprite()
        self.frame_num = 0
        self.surf = self.rightAnim


    def flipSprite(self):
        allFramesImg = pygame.image.load(
            self.anim["allFramesImage"])
        # .convert_alpha()
        # allFramesImg = pygame.transform.scale(allFramesImg, (384, 384))
        self.rightAnim = []
        self.leftAnim = []
        framesAdded = 0

        for row in range(self.anim["numRows"]):
            for col in range(self.anim["numCols"]):
                if framesAdded < self.anim["numFrames"]:
                    cropped_region = self.getAnimFrameRegion(row, col)
                    croppedSurface = allFramesImg.subsurface(cropped_region) 
                    

                    #scale the croppedSurface to given size
                    croppedSurface = pygame.transform.scale(croppedSurface, self.size)

                    self.rightAnim.append(croppedSurface)
                    flippedSurface = pygame.transform.flip(
                        croppedSurface, True, False)
                    self.leftAnim.append(flippedSurface)
                    framesAdded += 1

#platform1 = Sprite((1,1),(5,5),"OP Run.png")
#platform1.moveLeft(1)

