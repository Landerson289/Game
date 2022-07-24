import pygame
import math
import time

pygame.init()

screen=pygame.display.set_mode((800,600))

playerimg=pygame.image.load("circle.png")
playerimg=pygame.transform.scale(playerimg,(100,100))

enemyimg=pygame.image.load("spear enemy.png")
enemyimg=pygame.transform.scale(enemyimg,(100,100))

wallimg=pygame.image.load("wall.png")
wallimg=pygame.transform.scale(wallimg,(100,100))

boomerimg=pygame.image.load("boomerang.png")
boomerimg=pygame.transform.scale(boomerimg,(25,25))

def ellipse(t,total,b):
  #time is the fraction of the way it is around the curve
  a=1
  time=t/total
  rad=time*2*math.pi
  #print(rad)
  x=math.cos(rad)
  y=math.sqrt(b-b*x**2/a)
  x=x*20
  y=y*20
  return[x,y]
  
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
  def collide(self,x,y,type):
    distance=math.sqrt((self.pos[0]-x)**2+(self.pos[0]-y)**2)
    if distance<100:
      if type=="player":
        if y>self.pos[1]:
          theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
          newx=math.sin(theta)*100+self.pos[0]#+50
          newy=math.cos(theta)*100+self.pos[1]#+50
        else:
          theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
          newx=-math.sin(math.pi-theta)*100+self.pos[0]#+50
          newy=math.cos(math.pi-theta)*100+self.pos[1]#+50
      elif type=="boomer":
        pass
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
    #My code is bad so:
    #a must be 1
    #b is power
    self.pos=player1.pos
    self.hold=self.pos
    self.state="throwing"
    
    #print(self.hold)
    screen.blit(boomerimg,(self.pos[0],self.pos[1]))
    self.positions=[]
    for i in range(250):
      self.positions.append(ellipse(i,500,self.power))  
    for i in range(250):
      thing=ellipse(i,500,self.power)
      thing[0]=thing[0]*-1
      thing[1]=thing[1]*-1
      self.positions.append(thing) 
      
  def move(self):
    if len(self.positions)>0:
      self.pos[0]=self.positions[0][0]+self.hold[0]
      self.pos[1]=self.positions[0][1]+self.hold[1]
      #print(self.hold)
      self.positions.pop(0)
    else:
      self.state="ready"
      
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
enemy1=enemy([0,0],[0,0],"dead")


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
          boomer1.power=10
    if event.type==pygame.KEYUP:
      if event.key==pygame.K_w or event.key==pygame.K_s:
        player1.vel[1]=0
      elif event.key==pygame.K_a or event.key==pygame.K_d:
        player1.vel[0]=0
      elif event.key==pygame.K_SPACE:
        if boomer1.state=="ready":
          print("esvdv")
          boomer1.throw()
        
  player1.move()
  #player1X,player1Y=camera(player1.pos[0],player1.pos[1],player1.pos[0],player1.pos[1])  
  #screen.blit(playerimg,(400,300))
  screen.blit(playerimg,(player1.pos[0],player1.pos[1]))
  
  player1.pos[0],player1.pos[1]=wall1.collide(player1.pos[0],player1.pos[1],"player")
  #wall1X,wall1Y=camera(wall1.pos[0],wall1.pos[1],player1.pos[0],player1.pos[1])
  wall1X=wall1.pos[0]
  wall1Y=wall1.pos[1]
  screen.blit(wallimg,(wall1X,wall1Y))

  
  
  if boomer1.state=="throwing":
    #boomer1X,boomer1Y=camera(boomer1.pos[0],boomer1.pos[1],player1.pos[0],player1.pos[1])
    boomer1X=boomer1.pos[0]
    boomer1Y=boomer1.pos[1]
    screen.blit(boomerimg,(boomer1X,boomer1Y))
    boomer1.move()
    if enemy1.state=="alive":
      enemy1.collide(boomer1.pos[0],boomer1.pos[1],"boomer")
    
    
  if enemy1.state=="alive":
    enemy1.collide(player1.pos[0],player1.pos[1],"player")
    #enemy1X,enemy1Y=camera(enemy1.pos[0],enemy1.pos[1],player1.pos[0],player1.pos[1])
    enemy1X=enemy1.pos[0]
    enemy1Y=enemy1.pos[1]
    screen.blit(enemyimg,(enemy1X,enemy1Y))
  time.sleep(0.01)
  pygame.display.update()
