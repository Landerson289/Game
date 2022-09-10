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

VEL=[0,0.2]

pygame.init()

screen=pygame.display.set_mode((800,600))

pygame.display.set_caption("Boomerang game")

SPRITES=sprites()
SPRITES.scale()

BUTTONS=IMAGES.buttons()

#Create buttons
back_button=button.Button(10,10,BUTTONS.backimg,1)
resume_button=button.Button(350,125,BUTTONS.resumeimg,1)
levels_button=button.Button(350,250,BUTTONS.levelsimg,1)
quit_button=button.Button(350,375,BUTTONS.quitimg,1)
level_buttons=[]
for i in range(5):
  level_buttons.append(button.Button(75*i+100,100,BUTTONS.levelimgs[i],1))

UI=ui()
UI.scale()
UI.colour()

#Game states
game_state="start"#start,paused,over,play,win,cut
menu_state="main"
level=0
deltapower=0.01


def draw_text(text,text_col,size,x,y):
  font=pygame.font.Font("freesansbold.ttf",size)
  img = font.render(text,True,text_col)
  screen.blit(img,(x,y))
#Delta time (To be implemented)
class my_time:
  def __init__(self,previous_frame_time):
    self.previous_frame_time=previous_frame_time
    
  def delta_t(self):
    self.current_frame_time=time.time()
    self.dt = self.current_frame_time - self.previous_frame_time
    self.dt *= 60
    self.previous_frame_time = time.time()
#Trace out points on an ellipse
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
  X=x-x2+400
  Y=y-y2+300
  return X,Y
  
#Collision logic
def collide(type1,type2,x1,y1,x2,y2,**indexes):
  global warning
  global game_state
  global level
  distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
  newx1,newx2,newy1,newy2=x1,x2,y1,y2
  if type1=="player" and type2=="boomer":
    i=indexes["boomer_index"]
    print(boomers[i].hit)
    distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
    if boomers[i].state=="throwing":
      if distance<=140:
        if catching==True and boomers[i].throwstate=="arriving":
            boomers[i].state="ready"
            boomers[i].owner="player"
        elif boomers[i].throwstate=="arriving":
            draw_text("Catch",(0,0,0),15,300,200)
      elif boomers[i].owner=="player":
        boomers[i].throwstate="arriving"
      if distance>70:
        boomers[i].hit=False
  if type1=="boomer" and type2=="enemy":
    i=indexes["boomer_index"]
    j=indexes["enemy_index"]
    distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
    if boomers[i].state=="throwing" and boomers[i].owner==j:
      if distance<=140 and enemys[j].state=="alive":
        if boomers[i].throwstate=="arriving":
          boomers[i].state="ready"
          boomers[i].throwstate=None
          boomers[i].owner=j
      else:
        boomers[i].throwstate="arriving"
  
  if type1=="player":
    if round(distance,1)<100:
      if type2=="boomer":
        distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
        
        if distance<70:
          if boomers[i].state=="dropped":
            boomers[i].state="ready"
            boomers[i].owner="player"
          elif boomers[i].state=="throwing":
            if catching==False and boomers[i].throwstate=="arriving" and boomers[i].hit==False:
              #print("hit")
              player1.health-=30
              if boomers[i].owner=="player":
                boomers[i].state="ready"
                boomers[i].throwstate=None
              else:
                boomers[i].hit=True
              #warnings[i]=0
            
      elif type2=="wall":
        if y1>y2:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=math.sin(theta)*100+x2
          newy1=math.cos(theta)*100+y2
        else:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=-math.sin(math.pi-theta)*100+x2#+50
          newy1=math.cos(math.pi-theta)*100+y2#+50
          
      elif type2=="enemy":
        
        #for i in range(enemynum):
        i=indexes["enemy_index"]
        if enemys[i].state=="alive":
          player1.health-=100
          
      elif type2=="boost":
        i=indexes["boost_index"]
        #print(boosts[i].state!="used")
        if boosts[i].state!="used":
          if player1.health!=100:
            player1.health+=50
            if player1.health>=100:
              player1.health=100
            boosts[i].state="used"
      elif type2=="goal":
        game_state="win"
        #print("gfbvdrsf")
        level+=1
      else:
        print("ERROR: Unknown sprite: "+type2)
        print("Try swapping the sprites")
  elif type1=="boomer":
    i=indexes["boomer_index"]
    distance=math.sqrt((x1-x2-35)**2+(y1-y2-35)**2)
    if distance<=70:
      if type2=="wall":
        if boomers[i].state=="throwing":
          boomers[i].state="dropped"
          boomers[i].positions.clear()
      elif type2=="enemy":
        j=indexes["enemy_index"]
        if boomers[i].state=="throwing":
          if boomers[i].owner=="player":
            if enemys[j].state=="alive":
              enemys[j].state="dead"
        elif boomers[i].state=="dropped":
          if enemys[j].state=="alive":
            boomers[i].state="ready"
            boomers[i].owner=j
      elif type2=="boost":
        pass
              
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
            newy2=math.cos(math.pi-theta)*100+y1+200
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

  def move(self):
    self.pos[0]+=self.vel[0]*TIME.dt
    self.pos[1]+=self.vel[1]*TIME.dt
  
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
  def __init__(self,pos,vel,power,state,owner):
    self.pos=pos
    self.vel=vel
    self.power=power
    self.state=state
    self.hold=None
    self.positions=[]
    self.owner=owner
    self.hit=False
    self.throwstate=None
  def throw(self):
    if self.owner=="player":
      self.pos=player1.pos
    else:
      self.pos=enemys[self.owner].pos
    self.hold=(self.pos[0],self.pos[1])
    self.state="throwing"
    self.hit=False
    self.positions=ellipse(int(round(400*self.power,0)),75*self.power,100*self.power,200,200)
    if len(self.positions)>0:
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
      self.state="dropped"
      

      
  def update(self,i):
    collide("player","boomer",player1.pos[0],player1.pos[1],boomers[i].pos[0],boomers[i].pos[1],boomer_index=i)    
    
    if self.state=="dropped":
      boomer1X,boomer1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(UI.shadow_img,(boomer1X-10,boomer1Y-10))
        screen.blit(SPRITES.boomerimg,(boomer1X,boomer1Y))
        
    if self.state=="throwing":
      for j in range(numwalls):
        collide("boomer","wall",self.pos[0],self.pos[1],walls[j].pos[0],walls[j].pos[1],boomer_index=i)
      self.move()
      boomer1X,boomer1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(SPRITES.boomerimg,(boomer1X,boomer1Y))
      for j in range(enemynum):
        collide("boomer","enemy",self.pos[0],self.pos[1],enemys[j].pos[0],enemys[j].pos[1],boomer_index=i,enemy_index=j)#Must go after boomer1.move()

    count=0
    for a in range(numboomers):
      if boomers[a].owner=="player":
        count+=1
    if self.state=="ready" and self.owner=="player":
      screen.blit(SPRITES.boomerimg,((count-1)*50-50*i+10,550))
class enemy:
  def __init__(self,pos,vel,state,movement):
    self.pos=pos
    self.vel=vel
    self.state=state
    self.movement=movement#Pacing, chasing
    self.delay=False
    
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
        walls[j].pos,self.pos=collide("wall","enemy",walls[j].pos[0],walls[j].pos[1],self.pos[0],self.pos[1],enemy_index=i)
      self.move()
      enemy1X,enemy1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(enemy1X,enemy1Y):
        screen.blit(SPRITES.enemyimg,(enemy1X,enemy1Y))
        
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


#Define all the sprites   
player1=player([0,300],[0,0],100)
goal1=goal([0,0])

numwalls=len(levels[level]["wall_pos"])
walls=[]
for i in range(numwalls):
  walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))
  
numboomers=len(levels[level]["owners"])
boomers=[]
for i in range(numboomers):
  boomers.append(boomerang([0,0],[0,0],0,"ready",levels[level]["owners"][i]))
  
enemynum=len(levels[level]["enemy_pos"])
enemys=[]
for i in range(enemynum):
  enemys.append(enemy(levels[level]["enemy_pos"][i],levels[level]["enemy_vel"][i],"alive",levels[level]["enemy_mov"][i]))

boostnum=len(levels[level]["boost_pos"])
boosts=[]
for i in range(boostnum):
  boosts.append(boost(levels[level]["boost_pos"][i],"null"))



#time1=my_time(time.time())

throw_state=None

TIME=my_time(time.time())
running=True
while running:
  TIME.delta_t()
  #print(TIME.dt)
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
          #print(i+1)
          level=i+1
          #print(level)
          #Define all the sprites   
          player1=player([0,300],[0,0],100)
          goal1=goal([0,0])
          
          numwalls=len(levels[level]["wall_pos"])
          walls=[]
          for i in range(numwalls):
            walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))
          numboomers=len(levels[level]["owners"])
          boomers=[]
          for i in range(numboomers):
            boomers.append(boomerang([0,0],[0,0],0,"ready",levels[level]["owners"][i]))
            
          enemynum=len(levels[level]["enemy_pos"])
          enemys=[]
          for i in range(enemynum):
            enemys.append(enemy(levels[level]["enemy_pos"][i],levels[level]["enemy_vel"][i],"alive",levels[level]["enemy_mov"][i]))
          
          boostnum=len(levels[level]["boost_pos"])
          boosts=[]
          for i in range(boostnum):
            boosts.append(boost(levels[level]["boost_pos"][i],"null"))
          for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
              game_state="play"
  elif game_state=="play":
    player1.move()
    screen.blit(SPRITES.playerimg,(400,300))
    
    boomersX=[]
    boomersY=[]
    
    for i in range(numboomers):
      boomers[i].update(i)
      print(boomers[i].state)
      print(boomers[i].owner)
      print("end")
    print("\n")
      
    for i in range(numwalls):
      walls[i].update(i)       

    for i in range(enemynum):
      enemys[i].update(i)

    for i in range(boostnum):
      boosts[i].update(i)

    
    goal1.update()
    
    if player1.health<=0:
      game_state="over"

    
    dummy_boomer=boomerang(player1.pos,[0,0],boomers[0].power,"ready","player")
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
    screen.blit(UI.health_bg_img,(0,0))
    if player1.health>0:
      UI.health_img=pygame.transform.scale(UI.health_img,(2*player1.health,20))
    screen.blit(UI.health_img,(0,0))

    
    for i in range(numboomers):
      if boomers[i].power>2:
        deltapower=-0.01
      elif boomers[i].power<0.03:
        deltapower=0.01
      #print(boomers[i].power,deltapower)
      boomers[i].power+=deltapower*TIME.dt
      if boomers[i].power<0:
        boomers[i].power=0
    #print(100*boomers[0].power/2)
    #print(boomers[3].power)
    power_img2=pygame.transform.scale(UI.power_img,(20,100*boomers[0].power/2))
    screen.blit(power_img2,(500,400-100*boomers[0].power/2))
        
        
  elif game_state=="win":
    draw_text("YOU WIN",(0,0,0),100,150,250)
    draw_text("Click any button to continue",(0,0,0),30,150,375)
    #Define all the sprites   
    player1=player([0,300],[0,0],100)
    goal1=goal([0,0])
    
    numwalls=len(levels[level]["wall_pos"])
    walls=[]
    for i in range(numwalls):
      walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))

    numboomers=len(levels[level]["owners"])
    boomers=[]
    for i in range(numboomers):
      boomers.append(boomerang([0,0],[0,0],0,"ready",levels[level]["owners"][i]))

    print(levels[level]["enemy_mov"])
    enemynum=len(levels[level]["enemy_pos"])
    enemys=[]
    for i in range(enemynum):
      enemys.append(enemy(levels[level]["enemy_pos"][i],levels[level]["enemy_vel"][i],"alive",levels[level]["enemy_mov"][i]))
    
    boostnum=len(levels[level]["boost_pos"])
    boosts=[]
    for i in range(boostnum):
      boosts.append(boost(levels[level]["boost_pos"][i],"null"))
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
  elif game_state=="over":
    #print(levels[level]["enemy_pos"])
    draw_text("GAME OVER",(0,0,0),100,150,250)
    draw_text("Click any button to play again",(0,0,0),30,150,375)
    #Define all the sprites   
    player1=player([0,300],[0,0],100)
    goal1=goal([0,0])
    
    numwalls=len(levels[level]["wall_pos"])
    walls=[]
    for i in range(numwalls):
      walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))

    numboomers=len(levels[level]["owners"])
    boomers=[]
    for i in range(numboomers):
      boomers.append(boomerang([0,0],[0,0],0,"ready",levels[level]["owners"][i]))
      
    enemynum=len(levels[level]["enemy_pos"])
    enemys=[]
    #print(levels[level])
    #print(levels[level]["enemy_mov"])
    for i in range(enemynum):
      enemys.append(enemy(levels[level]["enemy_pos"][i],levels[level]["enemy_vel"][i],"alive",levels[level]["enemy_mov"][i]))
    
    boostnum=len(levels[level]["boost_pos"])
    boosts=[]
    for i in range(boostnum):
      boosts.append(boost(levels[level]["boost_pos"][i],"null"))

    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
      

  elif game_state=="start":
    draw_text("WELCOME",(0,0,0),100,150,250)
    draw_text("Click any button to start",(0,0,0),30,150,375)
    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_state="play"
  catching=False
  for event in pygame.event.get():
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_w or event.key==pygame.K_UP:
          player1.vel[1]=-0.6
        if event.key==pygame.K_a or event.key==pygame.K_LEFT:
          player1.vel[0]=-0.6
        if event.key==pygame.K_s or event.key==pygame.K_DOWN:
          player1.vel[1]=0.6
        if event.key==pygame.K_d or event.key==pygame.K_RIGHT:
          player1.vel[0]=0.6
        if event.key==pygame.K_SPACE:#Bomberang
          pass
        if event.key==pygame.K_p:
          game_state="paused"
      if event.type==pygame.MOUSEBUTTONDOWN:
        if event.button==1:
          if game_state=="play":
            
            for i in range(numboomers):
              if boomers[i].owner=="player":
                if boomers[i].state=="ready":
                  boomers[i].state="throwing"
                  boomers[i].throw()
                  boomers[i].throwstate="leaving"
                  break
            
        elif event.button==3:
          catching=True
          print("catch")
      if event.type==pygame.KEYUP:
        if event.key==pygame.K_w or event.key==pygame.K_UP or event.key==pygame.K_s or event.key==pygame.K_DOWN:
          player1.vel[1]=0
        elif event.key==pygame.K_a or event.key==pygame.K_d or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
          player1.vel[0]=0
  #print("new")
  #print(levels[level]["enemy_pos"])
  pygame.display.update()