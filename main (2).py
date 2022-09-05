import pygame
import math
import time
import button
import particles
import Levels

VEL=[0,0.2]

pygame.init()

screen=pygame.display.set_mode((800,600))

pygame.display.set_caption("Boomerang game")


#Load images
playerimg=pygame.image.load("images/player.png")
enemyimg=pygame.image.load("images/spear enemy.png")
wallimg=pygame.image.load("images/wall.png")
boomerimg=pygame.image.load("images/boomerang.png")
boostimg=pygame.image.load("images/boost.png")
goalimg=pygame.image.load("images/goal.png")


#Scale images
enemyimg=pygame.transform.scale(enemyimg,(100,100))
playerimg=pygame.transform.scale(playerimg,(100,100))
wallimg=pygame.transform.scale(wallimg,(100,100))
boomerimg=pygame.transform.scale(boomerimg,(30,30))
boostimg=pygame.transform.scale(boostimg,(100,100))
goalimg=pygame.transform.scale(goalimg,(100,100))

#Load buttons images
backimg=pygame.image.load("buttons/back.png").convert_alpha()
quitimg=pygame.image.load("buttons/quit.png").convert_alpha()
resumeimg=pygame.image.load("buttons/resume.png").convert_alpha()
levelsimg=pygame.image.load("buttons/levels.png").convert_alpha()
levelimgs=[]
for i in range(5):
  levelimgs.append(pygame.image.load("buttons/level "+str(i+1)+".png"))

#Create buttons
back_button=button.Button(10,10,backimg,1)
resume_button=button.Button(350,125,resumeimg,1)
levels_button=button.Button(350,250,levelsimg,1)
quit_button=button.Button(350,375,quitimg,1)
level_buttons=[]
for i in range(5):
  level_buttons.append(button.Button(75*i+100,100,levelimgs[i],1))

#Load UI images
health_bg_img=pygame.image.load("images/square.png")
health_img=pygame.image.load("images/square.png")
dot_img=pygame.image.load("images/circle.png")
power_bg_img=pygame.image.load("images/square.png")
power_img=pygame.image.load("images/square.png")
shadow_img=pygame.image.load("images/circle.png")

#Scale UI images
health_bg_img=pygame.transform.scale(health_bg_img,(200,20))
dot_img=pygame.transform.scale(dot_img,(8,8))
power_bg_img=pygame.transform.scale(power_bg_img,(200,20))
shadow_img=pygame.transform.scale(shadow_img,(50,50))

#Change colours
var=pygame.PixelArray(health_bg_img)
var.replace((0,0,0),(50,50,50))
del var

var=pygame.PixelArray(health_img)
var.replace((0,0,0),(255,0,0))
del var

var=pygame.PixelArray(dot_img)
var.replace((0,0,0),(50,50,50))
del var

var=pygame.PixelArray(shadow_img)
var.replace((0,0,0),(50,50,50))
del var

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
    
  def calculate_deltatime(self,previous_frame_time):
    self.dt = time.time() - self.previous_frame_time
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
    y=mag*math.cos(theta)
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
  global throw_states
  global warning
  global game_state
  global level
  distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
  newx1,newx2,newy1,newy2=x1,x2,y1,y2
  if type1=="player" and type2=="boomer":
    i=indexes["boomer_index"]
    distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
    if boomers[i].state=="throwing":
      if distance<=140:
        
        #print(throw_states[i])
        if catching==True and throw_states[i]=="arriving":
            boomers[i].state="ready"
            #warnings[i]=0
        elif throw_states[i]=="arriving":
            draw_text("Catch",(0,0,0),15,300,200)
              #warnings[i]+=1
              #print(warnings)
      else:
        throw_states[i]="arriving"
  if round(distance,1)<100:
    if type1=="player":
      if type2=="boomer":
        distance=math.sqrt((x1-x2+35)**2+(y1-y2+35)**2)
        
        if distance<65:
          if boomers[i].state=="dropped":
            boomers[i].state="ready"
          elif boomers[i].state=="throwing":
            if catching==False and throw_states[i]=="arriving":
              print("hit")
              player1.health-=30
              boomers[i].state="ready"
              throw_states[i]=None
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
        if boomers[i].state=="throwing":
          if type2=="wall":
            boomers[i].state="dropped"
            boomers[i].positions.clear()
            #print(distance)
          elif type2=="enemy":
            #for i in range(enemynum):
            j=indexes["enemy_index"]
            if enemys[j].state=="alive":
              enemys[j].state="dead"
              #print(distance)
          elif type2=="boost":
            pass
              
    elif type1=="wall":
      if type2=="enemy":
        i=indexes["enemy_index"]
        
        if enemys[i].movement== "pacing":
          enemys[i].vel[0]*=-1
          enemys[i].vel[1]*=-1
        elif enemys[i].movement=="chasing":
          
          if y1>y2:
            print(distance)
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
        #print(indexes["wall_index"],[x1,y1],indexes["boost_index"],[x2,y2])
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
        print([newx2,newy2])
      else:
        print("ERROR: Unknown sprite: "+type2)
        print("Try swapping the sprites")
    elif type1=="enemy":
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
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]
    #print(self.vel)
  
class wall:
  def __init__(self,pos,vel):
    self.pos=pos
    self.vel=vel
  def update(self,i):
    self.move()
    player1.pos,self.pos=collide("player","wall",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1])
    wall1X,wall1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
    if onscreen(wall1X,wall1Y):
      screen.blit(wallimg,(wall1X,wall1Y))
  def move(self):
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]
class boomerang:
  def __init__(self,position,vel,power,state):
    self.position=position
    self.vel=vel
    self.power=power
    self.state=state
    self.hold=None
    self.positions=[]
  def throw(self):
    self.position=player1.pos
    self.hold=(self.position[0],self.position[1])
    self.state="throwing"
    self.positions=ellipse(int(round(400*self.power,0)),75*self.power,100*self.power,200,200)
    if len(self.positions)>0:
      self.bottom=self.positions[0]
      self.top=self.positions[len(self.positions)//2]
 
  def move1(self):
    if len(self.positions)>0:
      hold2=(player1.pos[0],player1.pos[1])
      adjust0=-(self.top[0]+self.bottom[0])/2 +self.top[0]
      adjust1=-(self.top[1]+self.bottom[1])/2 +self.top[1]+100
      #print(player1.pos)
      #print(hold2)
      self.position[0]=self.positions[0][0]+self.hold[0]+adjust0
      #print(player1.pos)
      self.position[1]=self.positions[0][1]+self.hold[1]+adjust1
      #print(player1.pos)
      self.positions.pop(0)
      #print(hold2)
      player1.pos=[hold2[0],hold2[1]]
      del hold2
    else:
      self.state="dropped"
      #print("Positions empty")

      
  def update(self,i):
    collide("player","boomer",player1.pos[0],player1.pos[1],boomers[i].position[0],boomers[i].position[1],boomer_index=i)    
    
    if self.state=="dropped":
      boomer1X,boomer1Y=camera(self.position[0],self.position[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(shadow_img,(boomer1X-10,boomer1Y-10))
        screen.blit(boomerimg,(boomer1X,boomer1Y))
        
    if self.state=="throwing":
      for j in range(numwalls):
        collide("boomer","wall",self.position[0],self.position[1],walls[j].pos[0],walls[j].pos[1],boomer_index=i)
      self.move1()
      boomer1X,boomer1Y=camera(self.position[0],self.position[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(boomerimg,(boomer1X,boomer1Y))
      for j in range(enemynum):
        collide("boomer","enemy",self.position[0],self.position[1],enemys[j].pos[0],enemys[j].pos[1],boomer_index=i,enemy_index=j)#Must go after boomer1.move1()
      
    if boomers[i].state=="ready":
      screen.blit(boomerimg,(100-50*i+10,550))
class enemy:
  def __init__(self,pos,vel,state,movement):
    self.pos=pos
    self.vel=vel
    self.state=state
    self.movement=movement#Pacing, chasing
    self.owner=owner
  def move(self):
    #print(self.vel)
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]

  def update(self,i):
    if self.state=="alive":
      if self.movement=="chasing":
        self.vel=vector(0.2,self.pos,player1.pos)
      collide("player","enemy",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1],enemy_index=i)
      for j in range(numwalls):
        walls[j].pos,self.pos=collide("wall","enemy",walls[j].pos[0],walls[j].pos[1],self.pos[0],self.pos[1],enemy_index=i)
      self.move()
      enemy1X,enemy1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if onscreen(enemy1X,enemy1Y):
        screen.blit(enemyimg,(enemy1X,enemy1Y))
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
        screen.blit(boostimg,(boost1X,boost1Y))
class goal:
  def __init__(self,pos):
    self.pos=pos
  def update(self):
    collide("player","goal",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1])
    goal1X,goal1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
    if onscreen(goal1X,goal1Y):
      screen.blit(goalimg,(goal1X,goal1Y))

object=Levels.levels()
levels=object.get()


#Define all the sprites   
player1=player([0,300],[0,0],100)
goal1=goal([0,0])

numwalls=len(levels[level]["wall_pos"])
walls=[]
for i in range(numwalls):
  walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))
  
boomers=[]
for i in range(3):
  boomers.append(boomerang([0,0],[0,0],0,"ready"))
  
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
warnings=[0,0,0]


running=True
while running:
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
            
          boomers=[]
          for i in range(3):
            boomers.append(boomerang([0,0],[0,0],0,"ready"))
            
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
    screen.blit(playerimg,(400,300))
    
    boomersX=[]
    boomersY=[]
    
    for i in range(3):
      boomers[i].update(i)
      
    for i in range(numwalls):
      walls[i].update(i)       

    for i in range(enemynum):
      enemys[i].update(i)

    for i in range(boostnum):
      boosts[i].update(i)

    goal1.update()
    
    if player1.health<=0:
      game_state="over"

    
    #print()
    dummy_boomer=boomerang(player1.pos,[0,0],boomers[0].power,"ready")
    dummy_boomer.throw()
    if True:#Add conition so it only does it when you hold down the mouse. Or remove it
      for i in range(len(dummy_boomer.positions)):
        if i%20==0:
          adjust0=-(dummy_boomer.positions[len(dummy_boomer.positions)//2][0]+dummy_boomer.positions[0][0])/2 +dummy_boomer.positions[len(dummy_boomer.positions)//2][0]
          adjust1=-(dummy_boomer.positions[len(dummy_boomer.positions)//2][1]+dummy_boomer.positions[0][1])/2 +dummy_boomer.positions[len(dummy_boomer.positions)//2][1]+100
          x=dummy_boomer.positions[i][0]+dummy_boomer.position[0]+adjust0
          y=dummy_boomer.positions[i][1]+dummy_boomer.position[1]+adjust1
          x,y=camera(x,y,player1.pos[0],player1.pos[1])
          if onscreen(x,y):
            screen.blit(dot_img,(x,y))
    screen.blit(health_bg_img,(0,0))
    if player1.health>0:
      health_img=pygame.transform.scale(health_img,(2*player1.health,20))
    screen.blit(health_img,(0,0))

    for i in range(3):
      if boomers[i].power>2:
        deltapower=-0.01
      elif boomers[i].power<0.03:
        deltapower=0.01
      #print(boomers[i].power,deltapower)
      boomers[i].power+=deltapower
    #print(100*boomers[0].power/2)
    power_img2=pygame.transform.scale(power_img,(20,100*boomers[0].power/2))
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
      
    boomers=[]
    for i in range(3):
      boomers.append(boomerang([0,0],[0,0],0,"ready"))

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
    print(levels[level]["enemy_pos"])
    draw_text("GAME OVER",(0,0,0),100,150,250)
    draw_text("Click any button to play again",(0,0,0),30,150,375)
    #Define all the sprites   
    player1=player([0,300],[0,0],100)
    goal1=goal([0,0])
    
    numwalls=len(levels[level]["wall_pos"])
    walls=[]
    for i in range(numwalls):
      walls.append(wall(levels[level]["wall_pos"][i],levels[level]["wall_vel"][i]))
      
    boomers=[]
    for i in range(3):
      boomers.append(boomerang([0,0],[0,0],0,"ready"))
      
    enemynum=len(levels[level]["enemy_pos"])
    enemys=[]
    print(levels[level])
    print(levels[level]["enemy_mov"])
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
        if event.key==pygame.K_SPACE:
          pass
        if event.key==pygame.K_p:
          game_state="paused"
      if event.type==pygame.MOUSEBUTTONDOWN:
        if event.button==1:
          if game_state=="play":
            throw_states=[None,None,None]
            for i in range(3):
              if boomers[i].state=="ready":
                boomers[i].state="throwing"
                boomers[i].throw()
                throw_states[i]="leaving"
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

def hide():
  '''  
  playerimg=pygame.image.load("images/circle.png")
  playerimg=pygame.transform.scale(playerimg,(100,100))
  part=particles.particles((255,255,255),10,15,"square",100,100,100,100,100)
  clock=0
  while True:
    screen.fill((90,90,90))
    part.show(screen)
    part.shrink(clock)
    screen.blit(playerimg,(100,100))
    pygame.display.update()
    clock+=1
  '''
  '''
#rays=raycasting.raycasting(45,90,100,[400,300],[0,0],3)
rays=raycasting.raycasting(0,math.pi/2,100,[400,300],[0,0],3)
rays.lines()
rays.point()
while True:
  screen.fill((90,90,90))
  rays.show(screen)
  pygame.display.update()
  '''
  pass