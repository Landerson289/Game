import pygame
import math
import time
import button
import particles
import Levels
from IMAGES import sprites
from IMAGES import ui
import IMAGES
import random
from animate import animate


VEL=[0,0.2]

pygame.init()

screen=pygame.display.set_mode((800,600))

pygame.display.set_caption("Boomerang game")

SPRITES=sprites()
SPRITES.scale()

walk=animate(SPRITES.player_walk_imgs,0.1,screen)
walk2=animate(SPRITES.enemy_walk_imgs,0.1,screen)

BUTTONS=IMAGES.buttons()

#Create buttons
back_button=button.Button(10,10,BUTTONS.backimg,1)
resume_button=button.Button(350,125,BUTTONS.resumeimg,1)
levels_button=button.Button(350,250,BUTTONS.levelsimg,1)
quit_button=button.Button(350,375,BUTTONS.quitimg,1)
level_buttons=[button.Button(0,100,BUTTONS.levelimgs[0],1)]
for i in range(5):
  level_buttons.append(button.Button(75*i+100,100,BUTTONS.levelimgs[i+1],1))

UI=ui()
UI.scale()
UI.colour()
#Game states
game_state="start"#start,paused,over,play,win,cut,fin
menu_state="main"
level=0
deltapower=0.01
shake=[0,0]

def draw_text(text,text_col,size,x,y):
  font=pygame.font.Font("freesansbold.ttf",size)
  img = font.render(text,True,text_col)
  screen.blit(img,(x,y))
#Delta time
class my_time:
  def __init__(self,previous_frame_time):
    self.previous_frame_time=previous_frame_time
    
  def delta_t(self):
    self.current_frame_time=time.time()
    self.dt = self.current_frame_time - self.previous_frame_time
    self.dt *= 60
    self.previous_frame_time = time.time()
#Trace out points on an ellipse
def boundary(minx,miny,maxx,maxy):#Come back to this
  if player1.pos[0]<minx:
    player1.pos[0]=minx
  if player1.pos[0]+100>maxx:
    player1.pos[0]=maxx-100
  if player1.pos[1]<miny:
    player1.pos[1]=miny
  if player1.pos[1]+100>maxy:
    player1.pos[1]=maxy-100

def onscreen(x,y):
  if x<0 and y<0 and x+100>800 and y+100>600:
    return False
  else:
    return True
def ellipse(total,a,b,g,h):
  positions=[]
  for theta in range(total):
    y=a*math.cos(theta/total*2*math.pi)-100
    x=b*math.sin(theta/total*2*math.pi)
    positions.append([x,y])
  return positions 
  
#Adjust positions relative to player
def vector(mag,pos1,pos2):
  if pos1[1]<pos2[1]:
    theta=math.atan((pos1[0]-pos2[0])/(pos1[1]-pos2[1]))
    x=mag*math.sin(theta)
    y=mag*math.cos(theta)
  elif pos1[1]>pos2[1]:
    theta=math.atan((pos1[0]-pos2[0])/(pos1[1]-pos2[1]))
    x=-mag*math.sin(theta)
    y=-mag*math.cos(theta)
  else:
    x=mag
    y=0
  return [x,y]
def camera(x,y,x2,y2):
  #x and y are the object's coords and x1 and x2 and the player's coords
  #shake is a 2D array that controls screen shake
  X=x-x2+400+shake[0]
  Y=y-y2+300+shake[1]
  return X,Y
  
#Collision logic
class knockback:
  #x1,y1 is the thing that's not being knocked back
  def __init__(self):
    self.on=False
  def start(self,x1,x2,y1,y2,power):
    self.power=power
    self.count=0
    self.x=x2-x1
    self.y=y2-y1
    self.theta=math.atan(self.y/self.x)
    self.rad=math.sqrt(self.y**2+self.x**2)
    print(self.rad,self.x,self.y)
    if self.rad<=100:
      self.on=True
      self.newrad=self.power
      if x2>x1:
        self.newx=math.cos(self.theta)*self.newrad
        self.newy=math.sin(self.theta)*self.newrad
      else:
        self.newx=-math.cos(self.theta)*self.newrad
        self.newy=-math.sin(self.theta)*self.newrad
      print(self.newx,self.newy,(self.newx**2+self.newy**2)**0.5)
      return x1,y1
    else:
      self.newx=x2
      self.newy=y2
      return x2,y2
    #return newx,newy
  def update(self,x,y):
    if self.count<=self.power:
      print(self.count)
      returnX=self.newx/self.power+x
      returnY=self.newy/self.power+y
      print(returnX-x)
      self.count+=1
    else:
      returnX=self.newx+x
      returnY=self.newy+y
      self.on=False
    return returnX,returnY
def collide(type1,type2,x1,y1,x2,y2,**indexes):
  global game_state
  global level
  global shake
  global hitlist
  distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
  newx1,newx2,newy1,newy2=x1,x2,y1,y2
  if type1=="player":
    if type2=="boomer":
      distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
      i=indexes["boomer_index"]
      if distance<=140:
        if boomers[i].state=="throwing":
          if catching==True and boomers[i].throwstate=="arriving":
            boomers[i].state="ready"
            boomers[i].owner="player"
          elif boomers[i].throwstate=="arriving":
            draw_text("Catch",(0,0,0),15,300,200)
      elif boomers[i].owner=="player":
        boomers[i].throwstate="arriving"
      if distance>70:
        hitlist[-1][i]=False
      if distance<70:
        if boomers[i].state=="dropped":
          boomers[i].state="ready"
          boomers[i].owner="player"
        elif boomers[i].state=="throwing":
          if catching==False and boomers[i].throwstate=="arriving" and hitlist[-1][i]==False:
            player1.health-=30
            player1.pos[0],player1.pos[1]=player1.knock.start(x2,x1,y2,y1,10)
            shake[1]+=2.5
            if boomers[i].owner=="player":
              boomers[i].state="ready"
              boomers[i].throwstate=None
            else:
              hitlist[-1][i]=False
     
      if distance<200:
        if boomers[i].type=="bomb" and boomers[i].state=="exploding":
          player1.health-=70
          shake[1]+=2.5
          player1.knock.start(x2,x1,y2,y1,20)
    elif type2=="wall":
      if round(distance,1)<100:
        if y1>y2:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=math.sin(theta)*100+x2
          newy1=math.cos(theta)*100+y2
        elif y1<y2:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=-math.sin(math.pi-theta)*100+x2
          newy1=math.cos(math.pi-theta)*100+y2
        else:
          theta=math.pi/2
          if x1<x2:
            newx1=x2-100
            newy1=y2
          else:
            newx1=x2+100
            newy1=y2
        #shake[1]+=1  
    elif type2=="enemy":
      i=indexes["enemy_index"]
      if round(distance,1)<150:
        #print("goat")
        if y1>y2 and player1.attack1==True:
          enemys[i].health-=30
          print(enemys[i].health)
          shake[1]=2.5
          enemyX,enemyY=camera(enemys[i].pos[0],enemys[i].pos[1],player1.pos[0],player1.pos[1])
          enemys[i].BLOOD.start(enemyX+50,enemyY+50)
      if distance<100:
        if enemys[i].state=="alive":
          player1.health-=100
          shake[1]=2.5
    elif type2=="boost":
      if round(distance,1)<100:
        i=indexes["boost_index"]
        if boosts[i].state!="used":
          if player1.health!=100:
            player1.health+=50
            shake[1]+=2.5
            if player1.health>=100:
              player1.health=100
            boosts[i].state="used"
    elif type2=="goal":
      if round(distance,1)<100:
        game_state="win"
        level+=1
    else:
      print("ERROR: Unknown sprite: "+type2)
      print("Try swapping the sprites")
  elif type1=="boomer":
    i=indexes["boomer_index"]
    distance=math.sqrt((x1-x2-35)**2+(y1-y2-35)**2)
    if type2=="wall":
      j=indexes["wall_index"]
      if distance<=70:
        if boomers[i].state=="throwing":
          if boomers[i].type=="none":
            boomers[i].state="dropped"
            shake[1]+=1
            #boomers[i].positions.clear()
          elif boomers[i].type=="bomb":
            boomers[i].state="exploding"
            shake[1]+=2.5
      if distance<200:
        if boomers[i].type=="bomb" and boomers[i].state=="exploding":
          walls[j]=None
    elif type2=="enemy":
      j=indexes["enemy_index"]
      if distance<=70:
        if boomers[i].state=="throwing":
          if boomers[i].owner=="player":
            if enemys[j].state=="alive" and hitlist[j][i]==False:
              enemys[j].health-=30
              shake[1]+=2.5
              hitlist[j][i]=True
              enemyX,enemyY=camera(enemys[j].pos[0],enemys[j].pos[1],player1.pos[0],player1.pos[1])
              enemys[j].BLOOD.start(enemyX+50,enemyY+50)
              enemys[j].knock.start(x1,x2,y1,y2,10)  
        elif boomers[i].state=="dropped":
          if enemys[j].state=="alive":
            boomers[i].state="ready"
            boomers[i].owner=j
      else:
        hitlist[j][i]=False
      if distance<200:
        if boomers[i].type=="bomb" and boomers[i].state=="exploding":
          enemys[j].health-=70
          enemyX,enemyY=camera(enemys[j].pos[0],enemys[j].pos[1],player1.pos[0],player1.pos[1])
          enemys[j].BLOOD.start(enemyX+50,enemyY+50)
          #print(enemys[j].BLOOD.number)
      if boomers[i].state=="throwing" and boomers[i].owner==j:
        if distance<=140 and enemys[j].state=="alive":
          if boomers[i].throwstate=="arriving":
            boomers[i].state="ready"
            boomers[i].throwstate=None
            boomers[i].owner=j
        else:
          boomers[i].throwstate="arriving"
  elif type1=="wall":
    if round(distance,1)<100:
      if type2=="enemy":
        i=indexes["enemy_index"]
        if enemys[i].movement== "pacing":
          enemys[i].vel[0]*=-1
          enemys[i].vel[1]*=-1
        elif enemys[i].movement=="chasing":
          if y1>y2:
            theta=math.atan((x1-x2)/(y1-y2))
            newx2=-math.sin(theta)*100+x1
            newy2=math.cos(theta)*100+y1-200
          elif y1<y2:
            theta=math.atan((x1-x2)/(y1-y2))
            newx2=math.sin(math.pi-theta)*100+x1
            newy2=-math.cos(math.pi-theta)*100+y1#+200
          else:
            theta=math.pi/2
            if x1>=x2:
              newx2=-100+x1
            else:
              newx2=100+x1
            newy2=y1
      elif type2=="boost":
        if y1>y2:
          theta=math.atan((x1-x2)/(y1-y2))
          if x1<x2:
            newx2=round(math.sin(theta)*100+x1+200,2)
          elif x1>=x2:
            newx2=round(math.sin(theta)*100+x1,2)
          newy2=round(math.cos(theta)*100+y1-200,2)
        elif y1<y2:
          theta=math.atan((x1-x2)/(y1-y2))
          if x1<x2:
            newx2=round(-math.sin(theta)*100+x1+200,2)
          elif x1>=x2:
            newx2=round(-math.sin(theta)*100+x1,2)
          newy2=round(math.cos(math.pi-theta)*100+y1+200,2)
          
        else:
          theta=math.pi/2
          if x1>=x2:
            newx2=x1-100
          elif x1<x2:
            newx2=x1+100
          newy2=y1
      else:
        print("ERROR: Unknown sprite: "+type2)
        print("Try swapping the sprites")
  elif type1=="enemy":
    if round(distance,1)<100:
      if type2=="boost":
        pass
      else:
        print("ERROR: Unknown sprite: "+type2)
        print("Try swapping the sprites")
  else:
      print("ERROR: Unknown sprite: "+type1)
      print("Try swapping the sprites")
  return [newx1,newy1],[newx2,newy2]
  
class player:
  def __init__(self,pos,vel,health):
    self.pos=pos
    self.vel=vel
    self.health=health
    self.weapon=1
    self.attack1=False
    self.show_club=False
    self.coolDown=False
    self.DUST=particles.particles((50,50,50),10,7,"images/square",50,1)
    self.knock=knockback()
  def move(self):
    self.pos[0]+=self.vel[0]*TIME.dt
    self.pos[1]+=self.vel[1]*TIME.dt
  def update(self):
    self.move()
    boundary(-400,-400,400,400)
    if walk.on==False:
      screen.blit(SPRITES.playerimg,(400,300))
    else:
      walk.update(400,300)
      

    if self.show_club!=False:
      screen.blit(SPRITES.clubimg,(375,225))
      self.show_club+=1
      if self.show_club==20:
        self.show_club=False

    #print(self.DUST.on)
    if self.DUST.on:
      self.DUST.shrink(0,0)
      self.DUST.show(screen)

    if self.knock.on:
      self.pos[0],self.pos[1]=self.knock.update(self.pos[0],self.pos[1])

    if self.coolDown!=False:
      if time.time()-self.coolDown>5:
        self.coolDown=False
  def attack(self):
    self.attack1=True
    for i in range(len(enemys)):
      print("fish")
      collide("player","enemy",self.pos[0],self.pos[1],enemys[i].pos[0],enemys[i].pos[1],enemy_index=i)
    self.show_club=1
    #SPRITES.clubimg=pygame.transform.rotate(SPRITES.clubimg,-90)
    self.attack1=False
class wall:
  def __init__(self,pos,vel):
    self.pos=pos
    self.vel=vel
    
  def update(self,i):
    self.move()
    player1.pos,self.pos=collide("player","wall",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1])
    wall1X,wall1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
    if onscreen(wall1X,wall1Y):
      screen.blit(SPRITES.wallimg,(wall1X,wall1Y))
      
  def move(self):
    self.pos[0]+=self.vel[0]*TIME.dt
    self.pos[1]+=self.vel[1]*TIME.dt
    
class boomerang:
  def __init__(self,pos,vel,power,state,owner,type):
    self.pos=pos
    self.vel=vel
    self.power=power
    self.state=state
    self.hold=None
    self.positions=[]
    self.owner=owner
    self.throwstate=None
    self.type=type#bomb,none
  def throw(self):
    if self.owner=="player":
      self.pos=player1.pos
    else:
      self.pos=enemys[self.owner].pos
    self.hold=(self.pos[0],self.pos[1])
    self.state="throwing"
    self.positions=ellipse(int(round(400*self.power,0)),75*self.power,100*self.power,200,200)
    self.total=len(self.positions)
    if self.type=="none":
      self.spin=animate(SPRITES.boomer_imgs,0.1,screen,list=self.positions)
    elif self.type=="bomb":
      self.spin=animate(SPRITES.boomerBANG_imgs,0.1,screen,list=self.positions)
    self.spin.start()
    if self.total>0:
      self.bottom=self.positions[0]
      self.top=self.positions[len(self.positions)//2]
  def move(self):
    if len(self.positions)>0:
      if self.owner=="player":
        hold2=(player1.pos[0],player1.pos[1])

        adjust0=-(self.top[0]+self.bottom[0])/2 +self.top[0]
        adjust1=-(self.top[1]+self.bottom[1])/2 +self.top[1]+100

        self.pos[0]=self.positions[0][0]+self.hold[0]+adjust0
        self.pos[1]=self.positions[0][1]+self.hold[1]+adjust1
      else:
        hold2=(enemys[self.owner].pos[0],enemys[self.owner].pos[1])

        adjust0=-(self.top[0]+self.bottom[0])/2 +self.top[0]
        adjust1=-(self.top[1]+self.bottom[1])/2 +self.top[1]+100
        
        self.pos[0]=-self.positions[0][0]+self.hold[0]-adjust0
        self.pos[1]=-self.positions[0][1]+self.hold[1]-adjust1

      self.positions.pop(0)

      if self.owner=="player":
        player1.pos=[hold2[0],hold2[1]]
      else:
        enemys[self.owner].pos=[hold2[0],hold2[1]]
        
      del hold2
    else:
      if self.type=="none":
        self.state="dropped"
      elif self.type=="bomb":
        self.state="exploding"
        print("fish")
      

      
  def update(self,i):
    if self.state=="throwing":
      self.move()
      boomer1X,boomer1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        if self.type=="none":
          #SPRITES.boomerimg=pygame.transform.rotate(SPRITES.boomerimg,-15)
          if self.spin.on:
            self.spin.update(boomer1X,boomer1Y)#,len(self.positions))
          else:
            screen.blit(SPRITES.boomerimg,(boomer1X,boomer1Y))
        elif self.type=="bomb":
          if self.spin.on:
            self.spin.update(boomer1X,boomer1Y)
          else:
            screen.blit(SPRITES.boomerbangimg,(boomer1X,boomer1Y))
    player1.pos,self.pos=collide("player","boomer",player1.pos[0],player1.pos[1],boomers[i].pos[0],boomers[i].pos[1],boomer_index=i)   
    for j in range(enemynum):
      collide("boomer","enemy",self.pos[0],self.pos[1],enemys[j].pos[0],enemys[j].pos[1],boomer_index=i,enemy_index=j)
    for j in range(numwalls):
      if walls[j]!=None:
        collide("boomer","wall",self.pos[0],self.pos[1],walls[j].pos[0],walls[j].pos[1],boomer_index=i,wall_index=j)
    if self.state=="dropped":
      boomer1X,boomer1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(UI.shadow_img,(boomer1X-10,boomer1Y-10))
        screen.blit(SPRITES.boomerimg,(boomer1X,boomer1Y))
        
    
        

    if self.state=="exploding":
      self.state=None
    
class enemy:
  def __init__(self,pos,vel,state,movement):
    self.pos=pos
    self.vel=vel
    self.state=state
    self.health=50
    self.movement=movement#Pacing, chasing
    self.delay=False
    self.BLOOD=particles.particles((255,0,0),20,20,"images/circle",70,0)
    self.knock=knockback()
    self.healthbar_bg=UI.enemy_health_bg_img
    self.healthbar=UI.enemy_health_img
  def move(self):
    self.pos[0]+=self.vel[0]*TIME.dt
    self.pos[1]+=self.vel[1]*TIME.dt
  def update(self,i):
    if self.state=="alive":
      if self.movement=="chasing":
        self.vel=vector(0.2,self.pos,player1.pos)
      collide("player","enemy",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1],enemy_index=i)
      self.attack(player1)
      for j in range(numwalls):
        if walls[j]!=None:
          walls[j].pos,self.pos=collide("wall","enemy",walls[j].pos[0],walls[j].pos[1], self.pos[0],self.pos[1],enemy_index=i)
      self.move()
      if self.vel[0]!=0 or self.vel[1]!=0:
        walk2.start()
      else:
        walk2.stop()
      enemy1X,enemy1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(enemy1X,enemy1Y):
        if self.vel[0]==0 and self.vel[1]==0:
          screen.blit(SPRITES.enemyimg,(enemy1X,enemy1Y))
        else:
          walk2.update(enemy1X,enemy1Y)
        if self.health>0:
          screen.blit(self.healthbar_bg,(enemy1X,enemy1Y))
          self.healthbar=pygame.transform.scale(self.healthbar,(2*self.health,10))
          screen.blit(self.healthbar,(enemy1X,enemy1Y))
      if self.health<=0:
        self.state=0
      if self.knock.on:
        self.knock.update(self.pos[0],self.pos[1])
    if self.BLOOD.on:
      #print(player1.vel[0]*TIME.dt)
      self.BLOOD.shrink(player1.vel[0]*TIME.dt,player1.vel[1]*TIME.dt)#Add camera effect to x positions  
      self.BLOOD.show(screen)
  def attack(self,target):
    distance=math.sqrt((self.pos[0]-target.pos[0])**2+(self.pos[1]-target.pos[1])**2)
    if distance<300*boomers[0].power and self.delay==False:
      for a in range(len(levels[level]["owners"])):
        if boomers[a].owner==i:
          if boomers[a].state=="ready":
            rand=random.randint(0,1)
            if rand==0:
              boomers[a].throw()
            self.delay=1
            break
            
    if self.delay!=False:
      self.delay+=1
    if self.delay==50:
      self.delay=False
          
class boost:
  def __init__(self,pos,state):
    self.pos=pos
    self.state=state

  def update(self,i):
    collide("player","boost",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1],boost_index=i)
    for j in range(len(walls)):
      if walls[j]!=None:
        walls[j].pos,self.pos=collide("wall","boost",walls[j].pos[0],walls[j].pos[1],self.pos[0],self.pos[1],boost_index=i,wall_index=j)
    if self.state!="used":
      boost1X,boost1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(boost1X,boost1Y):
        screen.blit(SPRITES.boostimg,(boost1X,boost1Y))
class goal:
  def __init__(self,pos):
    self.pos=pos
  def update(self):
    collide("player","goal",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1])
    goal1X,goal1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
    if onscreen(goal1X,goal1Y):
      screen.blit(SPRITES.goalimg,(goal1X,goal1Y))

object=Levels.levels()
levels=object.get()

def RESET(level):
  global player1
  global goal1
  global numwalls
  global walls
  global numboomers
  global boomers
  global enemynum
  global enemys
  global boostnum
  global boosts
  global hitlist
  #Define all the sprites  
  if level!=len(levels):
    player1=player([0,300],[0,0],100)
    
    goal1=goal([0,0])
    
    numwalls=len(levels[level]["wall_pos"])
    walls=[]
    for i in range(numwalls):
      walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))
      
    numboomers=len(levels[level]["owners"])
    boomers=[]
    for i in range(numboomers):
      boomers.append(boomerang([0,0],[0,0],0,"ready",levels[level]["owners"][i],levels[level]["type"][i]))
      
    enemynum=len(levels[level]["enemy_pos"])
    enemys=[]
    for i in range(enemynum):
      enemys.append(enemy(levels[level]["enemy_pos"][i],levels[level]["enemy_vel"][i],"alive",levels[level]["enemy_mov"][i]))
    
    boostnum=len(levels[level]["boost_pos"])
    boosts=[]
    for i in range(boostnum):
      boosts.append(boost(levels[level]["boost_pos"][i],"null"))
    
    hitlist=[]
    for i in range(enemynum+1):
      hitlist.append([])
      for i in range(numboomers):
        hitlist[-1].append(0)

  else:
    game_state="fin"
    level=0
RESET(level)

throw_state=None

TIME=my_time(time.time())
running=True
while running:
  TIME.delta_t()
  screen.fill((90,90,90))
  if game_state=="paused":
    if menu_state=="main":
      if resume_button.draw(screen):
        game_state="play"
      if levels_button.draw(screen):
        menu_state="levels"
      if quit_button.draw(screen):
        running=False
    elif menu_state=="levels":
      if back_button.draw(screen):
        menu_state="main"
      for i in range(5):
        if level_buttons[i].draw(screen):
          level=i
          RESET(level)
          for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
              game_state="play"
  elif game_state=="play":
    player1.update()
    for i in range(numboomers):
      boomers[i].update(i)
      
    for i in range(numwalls):
      if walls[i]!=None:
        walls[i].update(i)       

    for i in range(enemynum):
      enemys[i].update(i)

    for i in range(boostnum):
      boosts[i].update(i)

    
    goal1.update()
    
    if player1.health<=0:
      game_state="over"

    if player1.weapon!=3:
      dummy_boomer=boomerang(player1.pos,[0,0],boomers[0].power,"ready","player","none")
      dummy_boomer.throw()
      for i in range(len(dummy_boomer.positions)):
        if i%20==0:
          adjust0=-(dummy_boomer.positions[len(dummy_boomer.positions)//2][0]+dummy_boomer.positions[0][0])/2 +dummy_boomer.positions[len(dummy_boomer.positions)//2][0]
          adjust1=-(dummy_boomer.positions[len(dummy_boomer.positions)//2][1]+dummy_boomer.positions[0][1])/2 +dummy_boomer.positions[len(dummy_boomer.positions)//2][1]+100
          x=dummy_boomer.positions[i][0]+dummy_boomer.pos[0]+adjust0
          y=dummy_boomer.positions[i][1]+dummy_boomer.pos[1]+adjust1
          x,y=camera(x,y,player1.pos[0],player1.pos[1])
          if onscreen(x,y):
            screen.blit(UI.dot_img,(x,y))
            
    else:
      screen.blit(UI.club_range_img,(410,225))
    
    screen.blit(UI.health_bg_img,(0,0))
    if player1.health>0:
      UI.health_img=pygame.transform.scale(UI.health_img,(2*player1.health,20))
    screen.blit(UI.health_img,(0,0))

    counts=[0,0,1]
    for a in range(numboomers):
      if boomers[a].owner=="player" and boomers[a].state=="ready":
        if boomers[a].type=="none":
          counts[0]+=1
        elif boomers[a].type=="bomb":
          counts[1]+=1
          
    screen.blit(SPRITES.boomerimg,(10,540))
    screen.blit(SPRITES.boomerbangimg,(70,540))
    clubimg2=pygame.transform.scale(SPRITES.clubimg,(50,50))
    clubimg2=pygame.transform.rotate(clubimg2,45)
    screen.blit(clubimg2,(110,525))
    draw_text(str(counts[0]),(0,0,0),15,30,570)
    draw_text(str(counts[1]),(0,0,0),15,90,570)
    
    if counts[player1.weapon-1]==0:
      draw_text("WEAPON NOT AVAILABLE",(0,0,0),15,10,520)
    if player1.weapon==1:
      screen.blit(UI.select_img,(0,530))
    if player1.weapon==2:
      screen.blit(UI.select_img,(60,530))
    if player1.weapon==3:
      screen.blit(UI.select_img,(115,530))
    
    for i in range(numboomers):
      if boomers[i].power>2:
        deltapower=-0.01
      elif boomers[i].power<0.03:
        deltapower=0.01
      boomers[i].power+=deltapower*TIME.dt
      if boomers[i].power<0:
        boomers[i].power=0
    if player1.weapon!=3:
      power_img2=pygame.transform.scale(UI.power_img,(20,100*boomers[0].power/2))
      screen.blit(UI.power_bg_img,(500,300))
      screen.blit(power_img2,(500,400-100*boomers[0].power/2))
    else:
      if player1.coolDown!=False:
        CD=time.time()-player1.coolDown
        print(CD)
        if CD<=5:
          cooldown_img2=pygame.transform.scale(UI.cooldown_img,(20,100*(5-CD)/5))
          screen.blit(UI.power_bg_img,(500,300))
          screen.blit(cooldown_img2,(500,400-100*(5-CD)/5))
    if shake[1]!=0:
      sign=shake[1]/abs(shake[1])
      newshake=abs(shake[1])-0.2
      shake[1]=newshake*sign*-1

    
    
  elif game_state=="win":
    draw_text("YOU WIN",(0,0,0),100,150,250)
    draw_text("Click any button to continue",(0,0,0),30,150,375)
    #Define all the sprites  
    if level<len(levels):
      RESET(level)
    else:
      game_state="fin"

    
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
  elif game_state=="over":
    draw_text("GAME OVER",(0,0,0),100,150,250)
    draw_text("Click any button to play again",(0,0,0),30,150,375)
    RESET(level)

    
    
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
      

  elif game_state=="start":
    level=0
    draw_text("WELCOME",(0,0,0),100,150,250)
    draw_text("Click any button to start",(0,0,0),30,150,375)
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
  elif game_state=="fin":
    draw_text("YOU WIN",(0,0,0),100,150,250)
    draw_text("Click any button to start again",(0,0,0),30,150,375)
    level=0
    RESET(level)

    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="start"  
  catching=False
  for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_w or event.key==pygame.K_UP:
        player1.vel[1]=-0.6
        walk.start()
        player1.DUST.start(450,400)
      if event.key==pygame.K_a or event.key==pygame.K_LEFT:
        player1.vel[0]=-0.6
        walk.start()
        player1.DUST.start(450,400)
      if event.key==pygame.K_s or event.key==pygame.K_DOWN:
        player1.vel[1]=0.6
        walk.start()
        player1.DUST.start(450,400)
      if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
        player1.vel[0]=0.6
        walk.start()
        player1.DUST.start(450,400)
      if event.key==pygame.K_SPACE:#Bomberang
        for i in boomers:
          if i.state=="throwing" and i.type=="bomb":
            i.state="exploding"
            break
      if event.key==pygame.K_p:
        game_state="paused"
      if event.key==pygame.K_1:
        player1.weapon=1
      if event.key==pygame.K_2:
        player1.weapon=2
      if event.key==pygame.K_3:
        player1.weapon=3
        
      if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
        player1.vel[0]*=2
        player1.vel[1]*=2
    if event.type==pygame.MOUSEBUTTONDOWN:
        if event.button==1:
          if game_state=="play":
            for i in range(numboomers):
              if boomers[i].owner=="player":
                if boomers[i].state=="ready":
                  if player1.weapon==1 and boomers[i].type=="none":
                    boomers[i].state="throwing"
                    boomers[i].throw()
                    boomers[i].throwstate="leaving"
                    break
                  if player1.weapon==2 and boomers[i].type=="bomb":
                    boomers[i].state="throwing"
                    boomers[i].throw()
                    boomers[i].throwstate="leaving"
                    break
                  if player1.weapon==3:
                    if player1.coolDown==False:
                      player1.attack()
                      player1.coolDown=time.time()
                    
            
        elif event.button==3:
          catching=True
          print("catch")
    if event.type==pygame.KEYUP:
      if event.key==pygame.K_w or event.key==pygame.K_UP or event.key==pygame.K_s or event.key==pygame.K_DOWN:
        player1.vel[1]=0
        if player1.vel[0]==0:
          walk.stop()
          player1.DUST.stop()
      if event.key==pygame.K_a or event.key==pygame.K_d or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
        player1.vel[0]=0
        if player1.vel[1]==0:
          walk.stop()
          player1.DUST.stop()
      if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
        player1.vel[0]/=2
        player1.vel[1]/=2
  pygame.display.update()
