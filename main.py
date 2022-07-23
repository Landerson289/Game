import pygame
import math

pygame.init()

screen=pygame.display.set_mode((800,600))

playerimg=pygame.image.load("circle.png")
playerimg=pygame.transform.scale(playerimg,(100,100))
enemyimg=pygame.image.load("spear enemy.png")
enemyimg=pygame.transform.scale(enemyimg,(100,100))
wallimg=pygame.image.load("wall.png")
wallimg=pygame.transform.scale(wallimg,(100,100))

def camera(x,y,x2,y2):
  #x and y are the object's coords and x1 and x2 and the player's coords
  X=x-x2+400
  Y=y-y2+300
  return X,Y
class player:
  def __init__(self,pos,vel,health):
    self.pos=pos
    self.vel=vel
    self.health=health

  def move(self):
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]
  
class wall:
  def __init__(self,pos):
    self.pos=pos
  def collide(self,x,y):
    distance=math.sqrt((self.pos[0]-x)**2+(self.pos[0]-y)**2)
    if distance<100:
      if y>self.pos[1]:
        theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
        newx=math.sin(theta)*100+self.pos[0]#+50
        newy=math.cos(theta)*100+self.pos[1]#+50
      else:
        theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
        newx=-math.sin(math.pi-theta)*100+self.pos[0]#+50
        newy=math.cos(math.pi-theta)*100+self.pos[1]#+50
    else:
      theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
      newx=x
      newy=y
    return newx,newy  
  
class boomerang:
  def __init__(self,pos,vel,power,state):
    self.pos=pos
    self.vel=vel
    self.power=power
    self.state=state
  def throw(self):
    #a is major axis (y direction)
    #b is minor axis (x direction)
    #Eccentricity is power
    #or set eccentricity and a is power
    #Or combiniation

    
    pass
    
class enemy:
  def __init__(self,pos,vel,state):
    self.pos=pos
    self.vel=vel
    self.state=state
  def collide(self,x,y,type):
    global running
    distance=math.sqrt((self.pos[0]-x)**2+(self.pos[0]-y)**2)
    if distance<=100:
      if type=="player":
        running=False
      elif type=="boomer":
        self.state="dead"
    
player1=player([200,200],[0,0],100)
wall1=wall([100,100])
boomer1=boomerang([0,0],[0,0],0,"ready")
enemy1=enemy([0,0],[0,0],"alive")

running=True
while running:
  screen.fill((100,100,100))

  for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_w:
        player1.vel[1]=-0.3
      if event.key==pygame.K_a:
        player1.vel[0]=-0.3
      if event.key==pygame.K_s:
        player1.vel[1]=0.3
      if event.key==pygame.K_d:
        player1.vel[0]=0.3
      if event.key==pygame.K_SPACE:
        if boomer1.state=="ready":
          boomer1.power+=1
    if event.type==pygame.KEYUP:
      if event.key==pygame.K_w or event.key==pygame.K_s:
        player1.vel[1]=0
      elif event.key==pygame.K_a or event.key==pygame.K_d:
        player1.vel[0]=0
      elif event.key==pygame.K_SPACE:
        if boomer1.state=="ready":
          boomer1.state="throwing"
          boomer1.throw()
        
  player1.move()

  player1.pos[0],player1.pos[1]=wall1.collide(player1.pos[0],player1.pos[1])

  if enemy1.state=="alive":
    enemy1.collide(player1.pos[0],player1.pos[1],"player")
    enemy1X,enemy1Y=camera(enemy1.pos[0],enemy1.pos[1],player1.pos[0],player1.pos[1])
    screen.blit(enemyimg,(enemy1X,enemy1Y))

  player1X,player1Y=camera(player1.pos[0],player1.pos[1],player1.pos[0],player1.pos[1])  
  screen.blit(playerimg,(400,300))

  wall1X,wall1Y=camera(wall1.pos[0],wall1.pos[1],player1.pos[0],player1.pos[1])
  screen.blit(wallimg,(wall1X,wall1Y))
  
  pygame.display.update()
