import math


class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y
    self.lx, self.ly = x, y
    self.pinned = False
    self.drag = False
  
  def update(self, ax = 0, ay = 0.5, max_a = 15):
    if self.pinned == False:
      vx, vy = min(self.x - self.lx, max_a), min(self.y - self.ly, max_a)
      
      if self.x > screen_w:
        self.x = screen_w
        vx *= -0.3
      elif self.x < 0:
        self.x = 0
        vx *= -0.3
      if self.y > screen_h:
        self.y = screen_h
        vy *= -0.3
      elif self.y < 0:
        self.y = 0
        vy *= -0.3
      
      nx, ny = self.x + vx + ax, self.y + vy + ay
      
      self.lx, self.ly = self.x, self.y
      self.x, self.y = nx, ny


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
  def __init__(self, top, bottom, left, right, color=(255,255,255)):
    self.top, self.bottom, self.left, self.right = top, bottom, left, right
    self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]
    self.broken = False
    self.color = color
  
  def solve(self):
    #determine if patch is broken
    if self.top.broken == True or self.bottom.broken == True or self.left.broken == True or self.right.broken == True:
      self.broken = True
      return
    else:
      self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]
    pass
#--- Our edits end here ---
class Cloth:
  def __init__(self, size=15, l=10, tear=50, offset=(0,0), screen_size=(500,300), colors = [[(255,255,255) for i in range(15)] for j in range(15)]):
    global screen_w, screen_h
    screen_w, screen_h = screen_size
    
    #used to calculate z position
    self.length = l

    self.points = [[Point(x*l+offset[0],y*l+offset[1]) for x in range(size)] for y in range(size)]
    
    self.links = []

    self.patches = []
    
    for y, row in enumerate(self.points):
      for x, point in enumerate(row):
        if y == 0:
          point.pinned = True
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
      self.patches.append(Patch(top, bottom, left, right, colors[0][i]))
    for i in range(1, size-1):
      for j in range(0, size-1):
        top = self.links[j*2+(i-1)*(2*(size-1)+1)+1]
        left = self.links[j*2+i*(2*(size-1)+1)]
        bottom = self.links[j*2+i*(2*(size-1)+1)+1]
        right = self.links[j*2+i*(2*(size-1)+1)+2]
        self.patches.append(Patch(top, bottom, left, right, colors[i][j]))
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
      #--- Our edits end here ---
    
    for points in self.points:
      for point in points:
        point.update()