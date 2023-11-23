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
  c_tear = 1000

  map_img = cv2.imread('amogus.png')  
  map_img = cv2.resize(map_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  drag = False
  #2d array of colors
  colors = np.zeros((cloth_size,cloth_size,3))
  for i in range(cloth_size):
    for j in range(cloth_size):
      color = map_img[i][j]
      color = (color[2],color[1],color[0])
      colors[i][j] = color
    
  cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear, offset=(100,20), screen_size=(screen_w,screen_h), colors = colors)

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
          cloth = Cloth(size=cloth_size, l=cloth_l, tear=c_tear,offset=(100,20), screen_size=(screen_w,screen_h), colors = colors)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()
    
    screen.fill("white")

    #--- Our edits start here ---
    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth
    r,g,b = 100,150,200
    
  
    for patch in cloth.patches:
        points = [(p.x,p.y) for p in patch.points]
        pygame.draw.polygon(screen, patch.color, points, 0)
    

    for link in cloth.links:
      pygame.draw.line(screen, (100,100,100), (link.p1.x,link.p1.y), (link.p2.x,link.p2.y), 0)

    #for points in cloth.points:
    #  for point in points:
    #    pygame.draw.circle(screen, (255,255,255), (int(point.x),int(point.y)), 2)
    
    #double sided shenanigans
    # would recommend running on a smaller sized cloth (10 - 20)
    # effect is most apparent when lifting cloth from bottom or
    # grabbing the left or right edge and moving it far left or right
    # can uncomment to see effect, may need to comment out the patches lines (81-83) first
    
    '''
    for i in range(len(cloth.points)-1):
      for j in range(len(cloth.points[0])-1):
        v1 = (cloth.points[i][j].x, cloth.points[i][j].y)
        v2 = (cloth.points[i+1][j].x, cloth.points[i+1][j].y)
        v3 = (cloth.points[i+1][j+1].x, cloth.points[i+1][j+1].y)
        v4 = (cloth.points[i][j+1].x, cloth.points[i][j+1].y)

        #point A
        Ax = v1[0]
        Ay = v1[1]

        #point B
        Bx = v2[0]
        By = v2[1]

        #point C
        Cx = v4[0]
        Cy = v4[1]

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

        # vectors to compare angle difference to normal vector
        angleCompVectorX = [50, 0, 0]
        angleCompVectorY = [0, 500, 0]

        angleBetweenVectorsX = np.dot(normal, angleCompVectorX)
        angleBetweenVectorsY = np.dot(normal, angleCompVectorY)

        # double sided effect
        if angleBetweenVectorsX < 45 or angleBetweenVectorsY < 45: #can mess with these numbers if desired
          color = "red"  #back side color
        else:
          color = "blue" #front side color

        pygame.draw.polygon(screen, color, (v1,v2,v3,v4), 0)
    '''
    
    #--- Our edits end here ---
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()