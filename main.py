import pygame
import math

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
  
  cloth = Cloth(size=50, l=10, tear=10000, offset=(100,20), screen_size=(screen_w,screen_h))
  
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
          cloth = Cloth(size=50, l=10, tear=10000,offset=(100,20), screen_size=(screen_w,screen_h))
    
    mouse_pos = pygame.mouse.get_pos()
    
    if drag == True:
      cloth.drag(mouse_pos[0]-drag_pos[0],mouse_pos[1]-drag_pos[1])
    
    cloth.update()
    
    screen.fill("sky blue")

    #https://www.pygame.org/docs/ref/draw.html#pygame.draw.polygon
    # ^ for drawing the cloth

    for i in range(len(cloth.points)-1):
      for j in range(len(cloth.points[0])-1):
        pygame.draw.polygon(screen, (cloth.points[i][j].x*255/2000,cloth.points[i+1][j+1].y*255/2000,0), [(cloth.points[i][j].x,cloth.points[i][j].y), (cloth.points[i+1][j].x,cloth.points[i+1][j].y), (cloth.points[i+1][j+1].x,cloth.points[i+1][j+1].y), (cloth.points[i][j+1].x,cloth.points[i][j+1].y)])
    
    for link in cloth.links:
      pygame.draw.line(screen, (255,255,255), (link.p1.x,link.p1.y), (link.p2.x,link.p2.y), 2)

    #for points in cloth.points:
    #  for point in points:
    #    pygame.draw.circle(screen, (255,255,255), (int(point.x),int(point.y)), 2)
    
    

      
    
    pygame.display.update()
    clock.tick(30)



if __name__ == "__main__":
  main()