import pygame
import math

pygame.init()

screen=pygame.display.set_mode((800,600))

playerimg=pygame.image.load("circle.png")
playerimg=pygame.transform.scale(playerimg,(100,100))
wallimg=pygame.image.load("circle.png")
wallimg=pygame.transform.scale(wallimg,(100,100))
testimg=pygame.image.load("square.png")
testimg=pygame.transform.scale(wallimg,(10,10))

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
    deltaPOS=self.vel
  def controls(self):
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_w:
          player1.vel=[0,-0.3]
        if event.key==pygame.K_a:
          player1.vel=[-0.3,0]
        if event.key==pygame.K_s:
          player1.vel=[0,0.3]
        if event.key==pygame.K_d:
          player1.vel=[0.3,0]
        #if event.key==pygame.K_space:
          #if boomer_state=="ready":
            #boomer1.pos=self.pos
            #boomer1.throw()
            #pass
      if event.type==pygame.KEYUP:
        player1.vel=[0,0]
  

class wall:
  def __init__(self,pos):
    self.pos=pos

  def collide(self,x,y,vel):
    distance=math.sqrt((self.pos[0]-x)**2+(self.pos[0]-y)**2)
    if distance<100:
      #vector shit
      theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
      newx=math.sin(theta)*100+self.pos[0]#+50
      newy=math.cos(theta)*100+self.pos[1]#+50
    else:
      theta=math.atan((x-self.pos[0])/(y-self.pos[1]))
      newx=x
      newy=y
    return newx,newy  
  
class boomerang:
  def __init__(self,pos,vel):
    self.pos=pos
    self.vel=vel
  def throw(self):
    #global boomer_state
    boomer_state="throwing"
    self.pos=player1.pos
class enemy:
  def __init__(self,pos,vel):
    self.pos=pos
    self.vel=vel
    
player1=player([200,200],[0,0],100)
wall1=wall([200,50])
boomer_state="ready"
#boomer1=boomerang([0,0],[0,0])
while True:
  screen.fill((100,100,100))

  deltaPOS=player1.controls()
  player1.move()

  player1.pos[0],player1.pos[1]=wall1.collide(player1.pos[0],player1.pos[1],deltaPOS)

 #Camera working but easier without it rn 
  #wall1X,wall1Y=camera(wall1.pos[0],wall1.pos[1],player1.pos[0],player1.pos[1])
  #player1X,player1Y=camera(player1.pos[0],player1.pos[1],player1.pos[0],player1.pos[1])

  
  #screen.blit(playerimg,(400,300))
  #screen.blit(wallimg,(wall1X,wall1Y))
  screen.blit(playerimg,(player1.pos[0],player1.pos[1]))
  screen.blit(wallimg,(wall1.pos[0],wall1.pos[1]))
  pygame.display.update()
