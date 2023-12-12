import math
import numpy as np

COLLISION_THRESHOLD = 5.0

#Point Class: Consider the cloth as a large grid. Point creates the points that
  #comprise the corners of each square in the cloth grid
  #INPUTS:
    # x: desired x-position of point
    # y: desired y-position of point

class Point:
  def __init__(self, x, y):
    #x and y position of point
    self.x, self.y = x, y

    #x and y position of point for velocity calculations
    self.lx, self.ly = x, y

    #determines if we can drag point
    self.pinned = False

    #determines if point is currently being dragged
    self.drag = False
  
  def update(self, ax = 0, ay = 0.5, max_a = 15):
    if self.pinned == False:
      #velocity of point
      vx, vy = min(self.x - self.lx, max_a), min(self.y - self.ly, max_a)
      
      #collision check for edge of screen
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
      
      #new x and y position after change from velocity
      nx, ny = self.x + vx + ax, self.y + vy + ay
      
      #update x and y accordingly after change from velocity
      self.lx, self.ly = self.x, self.y
      self.x, self.y = nx, ny


#Link Class: creates a line between two adjacent points that are 
  #horizontally or vertically adjacent
  #creates the lines for each sqaure on the cloth grid
  #INPUTS:
    # p1: point at start of link line
    # p2: point at end of link line
    # d: initial distance between p1 and p2 (length of link line)
    # t: distance between p1 and p2 that causes link to tear

class Link:
  def __init__(self, p1, p2, d, t):
    #place inputs into link 
    self.p1, self.p2, self.d, self.t = p1, p2, d, t

    #determines if link has been broken (cloth has been torn)
    self.broken = False
  
  #calculates if link should tear based on distance between p1 and p2
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

#Patch Class: creates a "patch" for each sqaure (four links in a sqaure) in the cloth grid
#INPUTS:
    # top: top link of patch
    # bottom: bottom link of patch
    # left: left link of patch
    # right: right link of patch
    # color_f: front color of the patch
    # color_b: back color of the patch

class Patch:
  def __init__(self, top, bottom, left, right, color_f=(255,255,255), color_b=(255,255,255)):
    #links that comprise the patch
    self.top, self.bottom, self.left, self.right = top, bottom, left, right

    #corner points that comprise the patch
    self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]

    #determines if patch is broken (cloth torn)
    self.broken = False

    #front color of patch
    self.colorf = color_f

    #back color of patch
    self.colorb = color_b

    #represents if patch is showing backside
    self.flipped = False
  
  def solve(self):
    #determine if patch is broken
    if self.top.broken == True or self.bottom.broken == True or self.left.broken == True or self.right.broken == True:
      self.broken = True
      return
    else:
      self.points = [self.top.p2, self.right.p2, self.bottom.p1, self.left.p1]
    pass
#--- Our edits end here ---

#Cloth Class: generates a cloth based on the initialized points, links, and patches.
  # can control the length, rotation, size and offset of the cloth of the screen
  # for each point in the cloth grid, creates a link between horizontally and vertically adjacent points
  # such that their movement is connected
  # creates patches from the squares created by each group of top, bottom, left,and right links
# INPUTS:
  # size: amount of points in width of cloth gird
  # l: length between each point
  # tear: distance between adjacent points that results in a tear
  # offset: pixel offset cloth should be drawn from the top left corner (0,0)
  # screen_size: size of pygame window screen
  # colors_f: array of colors of patches on front of cloth
  # colors_b: array of colors of patches on back of cloth

class Cloth:
  def __init__(self, size=15, l=10, tear=50, offset=(0,0), screen_size=(500,300), colors_f = [[(255,255,255) for i in range(15)] for j in range(15)], colors_b = [[(255,255,255) for i in range(15)] for j in range(15)]):
    global screen_w, screen_h
    screen_w, screen_h = screen_size
    
    #used to calculate z position for patches
    self.length = l

    #array of points in cloth gird
    self.points = [[Point(x*l+offset[0],y*l+offset[1]) for x in range(size)] for y in range(size)]
    
    #array of links in cloth grid
    self.links = []

    #array of patches in cloth grid
    self.patches = []

    #amount of patches in cloth
    self.patchesAmount = 0

    #counts how many patches are showing the backside
    self.patchesFlipped = 0
    
    #rotate cloth 2D 
    self.rotationAmount = math.pi / 6 #can mess with this number, should be in format math.pi / x where x is some int, nums far from zero (ex: 30 or -30) do interesting things

    #for each point in cloth, create links between and connect adjacent ones to each other
    for y, row in enumerate(self.points):
      for x, point in enumerate(row):
        if y == 0: #change to the following to see something cool: ((y == 0 and x == 0) or (y == 0 and x == len(row) - 1)):
          point.pinned = True

          #rotate top of cloth by rotationAmount
          # equation resource: https://danceswithcode.net/engineeringnotes/rotations_in_2d/rotations_in_2d.html 
          point.x = point.x*math.cos(self.rotationAmount) - point.y*math.sin(self.rotationAmount)
          point.y = point.x*math.sin(self.rotationAmount) + point.y*math.cos(self.rotationAmount)

        else:
          if x != 0:
            self.links.append(Link(point, row[x-1], l, tear))
          self.links.append(Link(point, self.points[y-1][x], l, tear))
    
    #--- Our edits start here ---
    #initialize patches, based on points and links
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

    #updated patchesAmount to store amount of patches
    self.patchesAmount = len(self.patches)
    #--- Our edits end here ---
    self.dragging = []
  
  def start_drag(self, pos, drag_radius=20):
    for points in self.points:
      for point in points:
        if point.pinned == False:
          #if a point is able to move, check if mouse is within drag_radius of point
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
      #if point is being dragged, update its position
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
          #don't show broken patches
          self.patches.remove(patch)
        else:
          patch.solve()
      #--- Our edits end here ---
    
    for points in self.points:
      for point in points:
        point.update()  