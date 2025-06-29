import pygame
import sys
from pygame.locals import QUIT
from game import Game
from platforms import Platforms

pygame.init()

WIDTH = 1400
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 10
E = -1 #used to specify enemy in level


#gererate platform surfaces
def splitSpritesheet(image, numRows, numCols, numFrames):
    allFramesImg = pygame.image.load(image)
    img_w, img_h = (100,100)
    allFramesImg = pygame.transform.scale(allFramesImg, (img_w,img_h))
    platforms_list = []
    framesAdded = 0
    for row in range(numRows):
        for col in range(numCols):
            if framesAdded < numFrames:
                w = img_w / numCols
                h = img_h / numRows
                x = w * col
                y = h * row
                cropped_region = (x,y,w,h)
                croppedSurface = allFramesImg.subsurface(cropped_region)

                #Create a mask from the cropped surface
                mask = pygame.mask.from_surface(croppedSurface)

                #Find the bounding box of the opaque region 
                if mask.count() > 0: #Ensure there are opaque pixels
                    rect = mask.get_bounding_rects()[0] #Get the first bounding rect
                    
                    opaqueSurface = pygame.Surface(rect.size, pygame.SRCALPHA)
                    opaqueSurface.blit(croppedSurface, (0,0), rect)
                    platforms_list.append(opaqueSurface)
                framesAdded += 1
    return platforms_list


def createPlatformsList(platform_images):
    platforms_list = []

    #create and append the mask surface of each platform image to the list
    for img in platform_images:
        platform_surf = pygame.image.load("Images/Platforms/"+img)
        platform_mask = pygame.mask.from_surface(platform_surf)
        platforms_list.append(platform_surf)


    return platforms_list

# PLATFORMS_LIST = splitSpritesheet("Images/Platforms.png", 3, 3, 3)
PLATFORMS_LIST = createPlatformsList(["Platform_1.png","Platform_2.png","Platform_6(Slab).png"])


# #to be moved later ~ testing
# level_1 = Platforms(
#     pos =(0,30),
#     structure = [
#         [0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,2,2,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
#         [0,0,0,2,2,0,0,0,E,0,0,1,2,2,2,0,0,2,2,2,2,0,0,0,0],
#         [0,0,0,2,2,0,1,2,2,2,2,2,2,2,2,2,0,2,2,2,2,0,0,0,0]
#     ],
#     platforms_list = PLATFORMS_LIST
# )
# LEVELS = [level_1]

game = Game(SCREEN, WIDTH, HEIGHT, PLATFORMS_LIST)

running = True
while running:


    #event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False



    #drawing on the screen
    SCREEN.fill((0,0,0))
    game.PLAY_DA_GAME()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()