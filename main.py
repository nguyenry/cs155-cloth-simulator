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
  
  cloth_size = 100
  cloth_l = 5
  cloth = Cloth(size=cloth_size, l=cloth_l, tear=5000, offset=(100,20), screen_size=(screen_w,screen_h))
  
  map_img = cv2.imread('amogus.png')  # Provide the correct path
  map_img = cv2.resize(map_img, (cloth_size, cloth_size))  # Resize image to match cloth size
  drag = False

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
          cloth = Cloth(size=50, l=10, tear=5000,offset=(100,20), screen_size=(screen_w,screen_h))
    
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()
    
    screen.fill("white")

    #--- Our edits start here ---
    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth
    r,g,b = 100,150,200

    #2d array of colors
    colors = np.zeros((len(cloth.points),len(cloth.points[0]),3))
    for i in range(len(cloth.points)):
      for j in range(len(cloth.points[0])):
        colors[i][j] = [i/len(cloth.points),j/len(cloth.points[0]),0.5]
    
    for i in range(len(cloth.points)-1):
      for j in range(len(cloth.points[0])-1):
        v1 = (cloth.points[i][j].x, cloth.points[i][j].y)
        v2 = (cloth.points[i+1][j].x, cloth.points[i+1][j].y)
        v3 = (cloth.points[i+1][j+1].x, cloth.points[i+1][j+1].y)
        v4 = (cloth.points[i][j+1].x, cloth.points[i][j+1].y)
        
        # chat gpt help for the following 2 lines
        img_i, img_j = int(i * map_img.shape[0] / len(cloth.points)), int(j * map_img.shape[1] / len(cloth.points[0]))
        color = map_img[img_i, img_j]

        points = [v1, v2, v3, v4]
        pygame.draw.polygon(screen, color, points, 0)

        
        
    
    for link in cloth.links:
      pygame.draw.line(screen, (255,255,255), (link.p1.x,link.p1.y), (link.p2.x,link.p2.y), 0)

    #for points in cloth.points:
    #  for point in points:
    #    pygame.draw.circle(screen, (255,255,255), (int(point.x),int(point.y)), 2)
    

    
    #--- Our edits end here ---
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()