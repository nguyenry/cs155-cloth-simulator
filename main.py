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
  cloth_size = 50
  cloth_l = 500/cloth_size
  c_tear = 10000

  amog_img = cv2.imread('amogus.png')  
  amog_img = cv2.resize(amog_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  flag_img = cv2.imread('flag copy.png')  
  flag_img = cv2.resize(flag_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  india_img = cv2.imread('india.png')  
  india_img = cv2.resize(india_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  drag = False
  #2d array of colors
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
    
  cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear, offset=(100,20), screen_size=(screen_w,screen_h), colors_f = colors_amog, colors_b = colors_flag)

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
            cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear, offset=(100,20), screen_size=(screen_w,screen_h), colors_f = colors_amog, colors_b = colors_flag)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()

    #--- Our edits start here ---
    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth

    #change screen color based on what side of the cloth is showing
    #currently: goes from green to blue
    screenColor = (cloth.patchesFlipped / 1000 ) * 255 #can mess with the 1000 number, was trying to normalize by amount of patches
    screen.fill((25,50,screenColor)) #can mess with these numbers

    r,g,b = 100,150,200
    
  
    #for patch in cloth.patches:
    #    points = [(p.x,p.y) for p in patch.points]
    #    pygame.draw.polygon(screen, patch.color, points, 0)
    

    #for link in cloth.links:
    #  pygame.draw.line(screen, (100,100,100), (link.p1.x,link.p1.y), (link.p2.x,link.p2.y), 1)

    #for points in cloth.points:
    #  for point in points:
    #    pygame.draw.circle(screen, (255,255,255), (int(point.x),int(point.y)), 2)
    
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

      
      # double sided effect
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
  
    
    #--- Our edits end here ---
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()