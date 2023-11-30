import math
import numpy as np

COLLISION_THRESHOLD = 100
class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y
    self.lx, self.ly = x, y
    self.vx, self.vy = 0, 0
    self.z = 0
    self.pinned = False
    self.drag = False
  
  def update(self, ax = 0, ay = 0.5, max_a = 15):
    if self.pinned == False:
      self.vx, self.vy = min(self.x - self.lx, max_a), min(self.y - self.ly, max_a)
      
      if self.x > screen_w:
        self.x = screen_w
        self.vx *= -0.3
      elif self.x < 0:
        self.x = 0
        self.vx *= -0.3
      if self.y > screen_h:
        self.y = screen_h
        self.vy *= -0.3
      elif self.y < 0:
        self.y = 0
        self.vy *= -0.3
      
      nx, ny = self.x + self.vx + ax, self.y + self.vy + ay
      
      self.lx, self.ly = self.x, self.y
      self.x, self.y = nx, ny
      
      length = math.dist((self.x,self.y), (self.lx,self.ly))
      self.z = (self.x**2 + self.y**2) / (length+1)


class Link:
  def __init__(self, p1, p2, d, t):
    self.p1, self.p2, self.d, self.t = p1, p2, d, t
    self.broken = False
  
  def solve(self):
    dist_x = self.p1.x - self.p2.x
    dist_y = self.p1.y - self.p2.y
    
    dist = math.dist((self.p1.x,self.p1.y), (self.p2.x,self.p2.y))
    
    if dist > self.t:
      self.broken = True
    else:
      diff = (self.d - dist)/max(dist,0.1)
      
      dx = dist_x * 0.5 * diff
      dy = dist_y * 0.5 * diff
      
      if self.p1.pinned == False and self.p1.drag == False:
        self.p1.x += dx
        self.p1.y += dy
      if self.p2.pinned == False and self.p1.drag == False:
        self.p2.x -= dx
        self.p2.y -= dy
      
#--- Our edits start here ---
class Patch:
  def __init__(self, top, bottom, left, right, color_f=(255,255,255), color_b=(255,255,255)):
    self.top, self.bottom, self.left, self.right = top, bottom, left, right
    self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]
    self.broken = False
    self.colorf = color_f
    self.colorb = color_b
    self.z = (self.top.p1.z + self.top.p2.z + self.bottom.p1.z + self.bottom.p2.z)/4
    #represents if patch is showing backside
    self.flipped = False
  
  def solve(self):
    #determine if patch is broken
    if self.top.broken == True or self.bottom.broken == True or self.left.broken == True or self.right.broken == True:
      self.broken = True
      return
    else:
      self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]   
      self.z = (self.top.p1.z + self.top.p2.z + self.bottom.p1.z + self.bottom.p2.z)/4
    pass
#--- Our edits end here ---
class Cloth:
  def __init__(self, size=15, l=10, tear=50, offset=(0,0), screen_size=(500,300), colors_f = [[(255,255,255) for i in range(15)] for j in range(15)], colors_b = [[(255,255,255) for i in range(15)] for j in range(15)]):
    global screen_w, screen_h
    screen_w, screen_h = screen_size
    
    #used to calculate z position
    self.length = l

    self.points = [[Point(x*l+offset[0],y*l+offset[1]) for x in range(size)] for y in range(size)]
    
    self.links = []

    self.patches = []

    #counts how many patches are showing the backside
    self.patchesFlipped = 0
    
    #rotate cloth 2D 
    self.rotationAmount = 0*math.pi / 6 #can mess with this number, nums far from zero (ex: 30 or -30) do interesting things

    for y, row in enumerate(self.points):
      for x, point in enumerate(row):
        if y == 0: #change to the following to see something cool: ((y == 0 and x == 0) or (y == 0 and x == len(row) - 1)):
          point.pinned = True

          #rotate cloth by rotationAmount
          # equation resource: https://danceswithcode.net/engineeringnotes/rotations_in_2d/rotations_in_2d.html 
          point.x = point.x*math.cos(self.rotationAmount) - point.y*math.sin(self.rotationAmount)
          point.y = point.x*math.sin(self.rotationAmount) + point.y*math.cos(self.rotationAmount)

        else:
          if x != 0:
            self.links.append(Link(point, row[x-1], l, tear))
          self.links.append(Link(point, self.points[y-1][x], l, tear))
    #--- Our edits start here ---
    #initialize patches
    for i in range(size-1):
      link = Link(self.points[0][i+1], self.points[0][i], l, tear)
      top = link
      left = self.links[i*2]
      right = self.links[(i+1)*2]
      bottom = self.links[i*2+1]
      self.patches.append(Patch(top, bottom, left, right, colors_f[0][i], colors_b[0][i]))
    for i in range(1, size-1):
      for j in range(0, size-1):
        top = self.links[j*2+(i-1)*(2*(size-1)+1)+1]
        left = self.links[j*2+i*(2*(size-1)+1)]
        bottom = self.links[j*2+i*(2*(size-1)+1)+1]
        right = self.links[j*2+i*(2*(size-1)+1)+2]
        self.patches.append(Patch(top, bottom, left, right, colors_f[i][j], colors_b[i][j]))
    #--- Our edits end here ---
    self.dragging = []
  
  def start_drag(self, pos, drag_radius=20):
    for points in self.points:
      for point in points:
        if point.pinned == False:
          if math.dist((point.x,point.y), pos) < drag_radius:
            point.drag = True
            point.drag_pos = (point.x, point.y)
            
            self.dragging.append(point)
  
  def end_drag(self):
    for point in self.dragging:
      point.drag = False
    
    self.dragging.clear()
  
  def drag(self, dx, dy):
    for point in self.dragging:
      if point.drag == True:
        point.x = point.drag_pos[0] + dx
        point.y = point.drag_pos[1] + dy
  
  def update(self, iterations=3):
    for _ in range(iterations):
      for link in self.links:
        if link.broken == True:
          self.links.remove(link)
        else:
          link.solve()
      #--- Our edits start here ---
      for patch in self.patches:
        if patch.broken == True:
          self.patches.remove(patch)
        else:
          patch.solve()  
      for patch1 in self.patches:
        for patch2 in self.patches:
          if patch1 != patch2:
            if abs(patch1.z- patch2.z) < COLLISION_THRESHOLD:
              temp1 = patch1.points.copy()
              temp2 = patch2.points.copy()
              patch1.points[0].vx = temp2[0].vx
              patch1.points[0].vy = temp2[0].vy
              patch1.points[1].vx = temp2[1].vx
              patch1.points[1].vy = temp2[1].vy
              patch1.points[2].vx = temp2[2].vx
              patch1.points[2].vy = temp2[2].vy
              patch1.points[3].vx = temp2[3].vx
              patch1.points[3].vy = temp2[3].vy
              patch2.points[0].vx = temp1[0].vx
              patch2.points[0].vy = temp1[0].vy
              patch2.points[1].vx = temp1[1].vx
              patch2.points[1].vy = temp1[1].vy
              patch2.points[2].vx = temp1[2].vx
              patch2.points[2].vy = temp1[2].vy
              patch2.points[3].vx = temp1[3].vx
              patch2.points[3].vy = temp1[3].vy

      #--- Our edits end here ---
    
    for points in self.points:
      for point in points:
        point.update()  