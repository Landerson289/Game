import pygame
import math
import time
import button
import particles
import raycasting

pygame.init()

screen=pygame.display.set_mode((800,600))

pygame.display.set_caption("Boomerang game")


#Load images
playerimg=pygame.image.load("images/circle.png")
enemyimg=pygame.image.load("images/spear enemy.png")
wallimg=pygame.image.load("images/wall.png")
boomerimg=pygame.image.load("images/boomerang.png")
boostimg=pygame.image.load("images/boost.png")
goalimg=pygame.image.load("images/square.png")

#Scale images
enemyimg=pygame.transform.scale(enemyimg,(100,100))
playerimg=pygame.transform.scale(playerimg,(100,100))
wallimg=pygame.transform.scale(wallimg,(100,100))
boomerimg=pygame.transform.scale(boomerimg,(25,25))
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


#Scale UI images
health_bg_img=pygame.transform.scale(health_bg_img,(200,20))
dot_img=pygame.transform.scale(dot_img,(8,8))
power_bg_img=pygame.transform.scale(power_bg_img,(200,20))


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

#Game states
game_paused=True
game_over=False
game_won=False
menu_state="main"
level=1
deltapower=0.03

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
def camera(x,y,x2,y2):
  #x and y are the object's coords and x1 and x2 and the player's coords
  X=x-x2+400
  Y=y-y2+300
  return X,Y
  
#Collision logic
def collide(type1,type2,x1,y1,x2,y2,**indexes):
  global throw_states
  global warning
  global game_over
  global game_won
  global level
  distance=math.sqrt((x1-x2)**2+(y1-y2)**2)
  newx1,newx2,newy1,newy2=x1,x2,y1,y2
  if distance<=100:
    if type1=="player":
      if type2=="boomer":
        i=indexes["boomer_index"]
        if boomers[i].state=="dropped":
          if distance<=20:
            boomers[i].state="ready"
            
        elif boomers[i].state=="throwing":
          if catching==True and distance<=60 and throw_states[i]=="arriving":
            boomers[i].state="ready"
            warnings[i]=0
          elif distance<=60 and throw_states[i]=="arriving":
            draw_text("Catch",(0,0,0),15,300,200)
            warnings[i]+=1
          if distance>=60:
            throw_states[i]="arriving"
          if warnings[i]>=39 and catching==False and throw_states[i]=="arriving":
            player1.health-=30
            boomers[i].state="ready"
            warnings[i]=0
      elif type2=="wall":
        if y1>y2:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=math.sin(theta)*100+x2
          newy1=math.cos(theta)*100+y2
        else:
          theta=math.atan((x1-x2)/(y1-y2))
          newx1=-math.sin(math.pi-theta)*100+x2
          newy1=math.cos(math.pi-theta)*100+y2
         
      elif type2=="enemy":
        i=indexes["enemy_index"]
        if enemys[i].state=="alive":
          player1.health-=100
          
      elif type2=="boost":
        i=indexes["boost_index"]
        if boosts[i].state!="used":
          if player1.health!=100:
            player1.health+=50
            if player1.health>=100:
              player1.health=100
            boosts[i].state="used"
      elif type2=="goal":
        game_won=True
        level+=1
      else:
        print("ERROR: Unknown sprite: "+type2)
        print("Try swapping the sprites")
    elif type1=="boomer":
      for i in range(3):
        if boomers[i].state=="throwing":
          if type2=="wall":
            boomers[i].state="dropped"
            boomers[i].positions.clear()
          elif type2=="enemy":
            j=indexes["enemy_index"]
            if enemys[j].state=="alive":
              enemys[j].state="dead"
          elif type2=="boost":
            pass
          else:
            print("ERROR: Unknown sprite: "+type2)
            print("Try swapping the sprites")
    elif type1=="wall":
      if type2=="enemy":
        i=indexes["enemy_index"]
        enemys[i].vel[0]*=-1
        enemys[i].vel[1]*=-1
      elif type2=="boost":
          pass
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
  
class wall:
  def __init__(self,pos):
    self.pos=pos
  def update(self,i):
    player1.pos,self.pos=collide("player","wall",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1])
    wall1X,wall1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
    if onscreen(wall1X,wall1Y):
      screen.blit(wallimg,(wall1X,wall1Y))
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
      self.position[0]=self.positions[0][0]+self.hold[0]+adjust0
      self.position[1]=self.positions[0][1]+self.hold[1]+adjust1
      self.positions.pop(0)
      player1.pos=[hold2[0],hold2[1]]
      del hold2
    else:
      self.state="dropped"

      
  def update(self,i):
    collide("player","boomer",player1.pos[0],player1.pos[1],boomers[i].position[0],boomers[i].position[1],boomer_index=i)    
    
    if self.state=="dropped":
      boomer1X,boomer1Y=camera(self.position[0],self.position[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(boomerimg,(boomer1X,boomer1Y))
        
    if self.state=="throwing":
      for j in range(numwalls):
        collide("boomer","wall",self.position[0],self.position[1],walls[j].pos[0],walls[j].pos[1])
      self.move1()
      boomer1X,boomer1Y=camera(self.position[0],self.position[1],player1.pos[0],player1.pos[1])
      if onscreen(boomer1X,boomer1Y):
        screen.blit(boomerimg,(boomer1X,boomer1Y))
      for j in range(enemynum):
        collide("boomer","enemy",self.position[0],self.position[1],enemys[j].pos[0],enemys[j].pos[1],enemy_index=j)#Must go after boomer1.move1()
      
    if boomers[i].state=="ready":
      screen.blit(boomerimg,(100-50*i+10,550))
class enemy:
  def __init__(self,pos,vel,state,movement):
    self.pos=pos
    self.vel=vel
    self.state=state
    self.movement=movement
  def move(self):
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]

  def update(self,i):
    if self.state=="alive":
      collide("player","enemy",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1],enemy_index=i)
      enemy1X,enemy1Y=camera(self.pos[0],self.pos[1],player1.pos[0],player1.pos[1])
      if self.movement=="pacing":
        for j in range(numwalls):
          collide("wall","enemy",walls[i].pos[0],walls[i].pos[1],self.pos[0],self.pos[1],enemy_index=i,wall_index=j)
      self.move()
      if onscreen(enemy1X,enemy1Y):
        screen.blit(enemyimg,(enemy1X,enemy1Y))
class boost:
  def __init__(self,pos,state):
    self.pos=pos
    self.state=state

  def update(self,i):
    collide("player","boost",player1.pos[0],player1.pos[1],self.pos[0],self.pos[1],boost_index=i)
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
levels=[
  {
  "wall_pos":[[-200,0],[-100,0],[100,0],[200,0]],
  "enemy_pos":[[-200,100],[0,100],[200,100]],
  "boost_pos":[[-100,100],[100,100]],
},
  {
  "wall_pos":[[-200,300],[200,300],[-200,200],[200,200],[-200,100],[200,100],[-200,0],[200,0],[-200,-300],[200,-300],[-200,-200],[200,-200],[-200,-100],[200,-100]],
  "enemy_pos":[[-100,100],[100,100]],
  "boost_pos":[[-100,0],[0,0],[100,0]]
}]

#Define all the sprites   
player1=player([0,300],[0,0],100)
goal1=goal([0,0])

numwalls=len(levels[0]["wall_pos"])
walls=[]
for i in range(numwalls):
  walls.append(wall(levels[0]["wall_pos"][i]))
  
boomers=[]
for i in range(3):
  boomers.append(boomerang([0,0],[0,0],0,"ready"))
  
enemynum=len(levels[0]["enemy_pos"])
enemys=[]
for i in range(enemynum):
  enemys.append(enemy(levels[0]["enemy_pos"][i],[0,0],"alive","pacing"))

boostnum=len(levels[0]["boost_pos"])
boosts=[]
for i in range(boostnum):
  boosts.append(boost(levels[0]["boost_pos"][i],"null"))

throw_state=None
warnings=[0,0,0]


running=True
while running:
  screen.fill((90,90,90))
  if game_over==False:
    if game_won==False:
      if game_paused==True:
        if menu_state=="main":
          if resume_button.draw(screen):
            game_paused=False
          if levels_button.draw(screen):
            menu_state="levels"
          if quit_button.draw(screen):
            running=False
        elif menu_state=="levels":
          if back_button.draw(screen):
            menu_state="main"
          for i in range(5):
            if level_buttons[i].draw(screen):
              level=i+1
              #Define all the sprites   
              player1=player([0,300],[0,0],100)
              numwalls=len(levels[level-1]["wall_pos"])
              walls=[]
              for i in range(numwalls):
                walls.append(wall(levels[level-1]["wall_pos"][i]))
              boomers=[]
              for i in range(3):
                boomers.append(boomerang([0,0],[0,0],0,"ready"))
              enemys=[]
              enemynum=len(levels[level-1]["enemy_pos"])
              for i in range(enemynum):
                enemys.append(enemy(levels[level-1]["enemy_pos"][i],[0,0],"alive","pacing"))
              boostnum=len(levels[level-1]["boost_pos"])
              boosts=[]
              for i in range(boostnum):
                boosts.append(boost(levels[level-1]["boost_pos"][i],"null"))
              for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                  game_won=False
      else:
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
          game_over=True
          
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
            deltapower=-0.03
          elif boomers[i].power<0.03:
            deltapower=0.03
          boomers[i].power+=deltapower
        power_img2=pygame.transform.scale(power_img,(20,100*boomers[0].power/2))
        screen.blit(power_img2,(550,400-100*boomers[0].power/2))
        
        
    else:
      draw_text("YOU WIN",(0,0,0),100,150,250)
      draw_text("Click any button to continue",(0,0,0),30,150,375)
      
      #Define all the sprites   
      player1=player([0,300],[0,0],100)
      numwalls=len(levels[level-1]["wall_pos"])
      walls=[]
      for i in range(numwalls):
        walls.append(wall(levels[level-1]["wall_pos"][i]))
      boomers=[]
      for i in range(3):
        boomers.append(boomerang([0,0],[0,0],0,"ready"))
      enemys=[]
      enemynum=len(levels[level-1]["enemy_pos"])
      for i in range(enemynum):
        enemys.append(enemy(levels[level-1]["enemy_pos"][i],[0,0],"alive","pacing"))
      boostnum=len(levels[level-1]["boost_pos"])
      boosts=[]
      for i in range(boostnum):
        boosts.append(boost(levels[level-1]["boost_pos"][i],"null"))
      for event in pygame.event.get():
        if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
          game_won=False
  else:
    draw_text("GAME OVER",(0,0,0),100,150,250)
    draw_text("Click any button to play again",(0,0,0),30,150,375)
    player1=player([0,300],[0,0],100)
    numwalls=len(levels[level-1]["wall_pos"])
    walls=[]
    for i in range(numwalls):
      walls.append(wall(levels[level-1]["wall_pos"][i]))
    boomers=[]
    for i in range(3):
      boomers.append(boomerang([0,0],[0,0],0,"ready"))
    enemys=[]
    enemynum=len(levels[level-1]["enemy_pos"])
    for i in range(enemynum):
      enemys.append(enemy(levels[level-1]["enemy_pos"][i],[0,0],"alive","pacing"))
    boostnum=len(levels[level-1]["boost_pos"])
    boosts=[]
    for i in range(boostnum):
      boosts.append(boost(levels[level-1]["boost_pos"][i],"null"))

    for event in pygame.event.get():
      if event.type==pygame.KEYDOWN or event.type==pygame.MOUSEBUTTONDOWN:
        game_over=False
      

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
          game_paused=True
      if event.type==pygame.MOUSEBUTTONDOWN:
        if event.button==1:
          if game_paused==False:
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
          player1.vel[0]=0f
  pygame.display.update()
