import pygame
import math
import random

from simulation import Cloth


pygame.init()

flags = pygame.FULLSCREEN | pygame.DOUBLEBUF

screen = pygame.display.set_mode((0,0), flags, 16)

pygame.display.set_caption("Pygame Cloth Simulation")

screen_w, screen_h = screen.get_size()

screen.set_alpha(None)

cloth_image = pygame.image.load("amogus.png")
cloth_image = pygame.transform.scale(cloth_image, (10, 10))  # Adjust the size as needed


def main():
  clock = pygame.time.Clock()
  
  pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN])
  
  cloth = Cloth(size=50, l=10, tear=1000, offset=(100,20), screen_size=(screen_w,screen_h))
  

  drag = False

  base_color = [random.random() for _ in range(3)]  # Random RGB values for the base color
  color_array = []
  for i in range(len(cloth.points)-1):
    variation = [(random.random() - 0.5) * 0.2 for _ in range(3)]  # Small random variation
    new_color = [min(1.0, max(0.0, base_color[j] + variation[j])) for j in range(3)]
    color_array.append(new_color)

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
          cloth = Cloth(size=50, l=10, tear=10000,offset=(100,20), screen_size=(screen_w,screen_h))
    
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()
    
    screen.fill("white")

    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth
    r,g,b = 100,150,200
    
    

 

    for i in range(len(cloth.points)-1):
      for j in range(len(cloth.points[0])-1):
        v1 = (cloth.points[i][j].x, cloth.points[i][j].y)
        v2 = (cloth.points[i+1][j].x, cloth.points[i+1][j].y)
        v3 = (cloth.points[i+1][j+1].x, cloth.points[i+1][j+1].y)
        v4 = (cloth.points[i][j+1].x, cloth.points[i][j+1].y)

        r = int(color_array[i][0] * 255)
        g = int(color_array[i][1] * 255)
        b = int(color_array[i][2] * 255)
        pygame.draw.polygon(screen, (r,g,b), (v1,v2,v3,v4), 0)
        
    
    for link in cloth.links:
      pygame.draw.line(screen, (255,255,255), (link.p1.x,link.p1.y), (link.p2.x,link.p2.y), 1)

    #for points in cloth.points:
    #  for point in points:
    #    pygame.draw.circle(screen, (255,255,255), (int(point.x),int(point.y)), 2)
    
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()