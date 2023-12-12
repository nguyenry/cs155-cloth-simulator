import pygame
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb_to_hsv, hsv_to_rgb
import cv2


from simulation import Cloth


pygame.init()

flags = pygame.FULLSCREEN | pygame.DOUBLEBUF

screen = pygame.display.set_mode((0,0), flags, 16)

pygame.display.set_caption("Pygame Cloth Simulation")

screen_w, screen_h = screen.get_size()

screen.set_alpha(None)


def main():
  clock = pygame.time.Clock()
  
  pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN])

  #--- Our edits start here ---

  #CLOTH ATTRIBUTES AND IMAGE SET-UP

  #cloth attributes 1/2
  #used to determine how image maps onto cloth
  cloth_size = 20
  cloth_l = 500/cloth_size
  c_tear = 100

  #load in pre-included images
  #can change the front or back color of the cloth to any of the below
  amog_img = cv2.imread('amogus.png')  
  amog_img = cv2.resize(amog_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  flag_img = cv2.imread('flag copy.png')  
  flag_img = cv2.resize(flag_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  india_img = cv2.imread('india.png')  
  india_img = cv2.resize(india_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  sunset_img = cv2.imread('Sunset.png')  
  sunset_img = cv2.resize(sunset_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  space_img = cv2.imread('Space.png')  
  space_img = cv2.resize(space_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  drag = False

  #insert 2d array of colors for above images
  colors_amog = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = amog_img[i][j]
      color = (color[2],color[1],color[0])
      colors_amog[i][j] = color

  colors_flag = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = flag_img[i][j]
      color = (color[2],color[1],color[0])
      colors_flag[i][j] = color

  colors_ind = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = india_img[i][j]
      color = (color[2],color[1],color[0])
      colors_ind[i][j] = color

  colors_sunset = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = sunset_img[i][j]
      color = (color[2],color[1],color[0])
      colors_sunset[i][j] = color
  
  colors_space = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = space_img[i][j]
      color = (color[2],color[1],color[0])
      colors_space[i][j] = color

  #cloth attributes 2/2
  #used to determine the colors and offset of cloth
  frontColor = colors_sunset
  backColor = colors_space  
  cloth_offset = (100,20)

  cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear, offset=cloth_offset, screen_size=(screen_w,screen_h), colors_f = frontColor, colors_b = backColor)
  

  #--- Our edits end here ---
  while 1:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        break
      elif event.type == pygame.MOUSEBUTTONDOWN:
        drag = True
        drag_pos = pygame.mouse.get_pos()
        cloth.start_drag(drag_pos)
      elif event.type == pygame.MOUSEBUTTONUP:
        drag = False
        cloth.end_drag()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear, offset=cloth_offset, screen_size=(screen_w,screen_h), colors_f = frontColor, colors_b = backColor)
          
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()

    #--- Our edits start here ---
    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth

    #SCREEN BACKGROUND COLOR EFFECTS
    #change screen color based on what amount of backside of cloth is showing
    screenColor = (cloth.patchesFlipped / cloth.patchesAmount) * 255 
    screen.fill((50,25,screenColor)) #can mess with these numbers

    r,g,b = 100,150,200
    
    
    #for patch in cloth.patches:
    #    points = [(p.x,p.y) for p in patch.points]
    #    pygame.draw.polygon(screen, patch.color, points, 0)
    
    #2D SPHERE
    #"rotates" up or down based on how much of cloth is flipped
    #to make this optimized for the cloth
    #   need to find a way to make size dependent on the angle of normal vector
    #   of each patch 

    #2D sphere info
    sphereXpos = 2* screen_w / 3
    sphereYpos = screen_h / 3
    radius = 100
    clothFlippedRatio = cloth.patchesFlipped / cloth. patchesAmount
    size = (4 * ((clothFlippedRatio - 0.5) ** 2)) * (radius * 2) # size of oval = amount of rotation effect
    topColor = (241, 200, 151)
    bottomColor = (12, 192, 223)

    #2D sphere top half
    pygame.draw.circle(screen, 
                       topColor, 
                       (sphereXpos, sphereYpos), 
                       radius,
                       draw_top_left=True,
                       draw_top_right= True)
    
    #2D sphere bottom half
    pygame.draw.circle(screen, 
                       bottomColor, 
                       (sphereXpos, sphereYpos), 
                       radius,
                       draw_bottom_left=True,
                       draw_bottom_right= True)
    
    #2D sphere rectangle bounding the oval
    ovalBounding = pygame.Rect(sphereXpos - radius, 
                               sphereYpos - (size / 2), 
                               radius * 2, 
                               size)
    #2D sphere dynamic oval
    if clothFlippedRatio <= 0.5:
      #show more of top
      pygame.draw.ellipse(screen, 
                        topColor, 
                        ovalBounding)
    else:
      #show more of bottom
      pygame.draw.ellipse(screen, 
                        bottomColor, 
                        ovalBounding)

    #DOUBLE SIDED EFFECT
    # for double sided shenanigans:
    # would recommend running on a smaller sized cloth (10 - 20)
    
    for patch in cloth.patches:
      [v1, v2, v3, v4] = patch.points

      #point A
      Ax = v1.x
      Ay = v1.y

      #point B
      Bx = v2.x
      By = v2.y

      #point C
      Cx = v4.x
      Cy = v4.y

      magnitude = cloth.length

      # vector AB
      ABx = Bx - Ax
      ABy = By - Ay
      ABz = math.sqrt(abs(magnitude - (ABx * ABx) - (ABy * ABy)))

      vecAB = [ABx, ABy, ABz]

      # vector AC
      ACx = Cx - Ax
      ACy = Cy - Ay
      ACz = math.sqrt(abs(magnitude - (ACx * ACx) - (ACy * ACy)))

      vecAC = [ACx, ACy, ACz]

      normal = np.cross(vecAB, vecAC)

      # vector to compare angle difference to normal vector
      highlightVec = [0,0,50]
      angleBetweenHighlight = np.dot(normal, highlightVec)
      
      #attempts to change color based on individual patches "normal" vector
      #highlight = abs(angleBetweenHighlight)
      #color = (highlight, 0, 0)
    
      # double sided effect controller
      if angleBetweenHighlight < 70: #can mess with these numbers if desired
        color = patch.colorb  #back side color
        
        #recognize patch is flipped
        if patch.flipped == False:
          patch.flipped = True 
          cloth.patchesFlipped+=1 #increment patches flipped

      else:
        color = patch.colorf #front side color

        #if previously flipped, recongize it is no longer flipped
        if patch.flipped == True:
          patch.flipped = False 
          cloth.patchesFlipped-=1 #unincrement patches flipped 

      points = [(p.x,p.y) for p in patch.points]
      pygame.draw.polygon(screen, color, points, 0)
  

    #ADDITIONAL CLOTH EFFECTS (particle-ish effects)
    #can mess with all of the below numbers
    #uncomment the "pygame.draw..." lines under each effect
      #to see it on your screen when running the sim

    #used in sherbert effect to create a gradient color with adjancent spheres
    colShift = 0

    for points in cloth.points:
      for point in points:
        if int(point.y) > 300: #dipped effect, can remove or mess with this number or .x vs. .y
          for i in range(5): 
            
            #sherbert effect:
            #pygame.draw.circle(screen, (255, colShift, 255 - colShift), (int(point.x) + i*5,int(point.y) + i*3), 20)

            #puffy pepto puffer effect:
            #pygame.draw.circle(screen, (255,40*i,255), (int(point.x) + i*5,int(point.y) + i*3), 20)

            #purple puff effect:
            #pygame.draw.circle(screen, (30*i,20,255), (int(point.x) + i*3,int(point.y) + i*3), 40 - (i * 5))

            #sparkly effect:
            r = random.random()
            #pygame.draw.circle(screen, (255,255,255), (int(point.x) + i*5,int(point.y) + i*10 * r), 2 * r) 

            #control color shift for sherbert effect
            if colShift > 254:
              colShift = 0
            else:
              colShift+=1

    #--- Our edits end here ---
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()