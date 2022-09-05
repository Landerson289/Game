import pygame

class sprites:
  def __init__(self):
    self.playerimg=pygame.image.load("images/player.png")
    self.enemyimg=pygame.image.load("images/spear enemy.png")
    self.wallimg=pygame.image.load("images/wall.png")
    self.boomerimg=pygame.image.load("images/boomerang.png")
    self.boostimg=pygame.image.load("images/boost.png")
    self.goalimg=pygame.image.load("images/goal.png")

  def scale(self):
    #Scale images
    self.playerimg=pygame.transform.scale(self.playerimg,(100,100))
    self.enemyimg=pygame.transform.scale(self.enemyimg,(100,100))
    self.wallimg=pygame.transform.scale(self.wallimg,(100,100))
    self.boomerimg=pygame.transform.scale(self.boomerimg,(30,30))
    self.boostimg=pygame.transform.scale(self.boostimg,(100,100))
    self.goalimg=pygame.transform.scale(self.goalimg,(100,100))

class ui:
  def __init__(self):
    #Load UI images
    self.health_bg_img=pygame.image.load("images/square.png")
    self.health_img=pygame.image.load("images/square.png")
    self.dot_img=pygame.image.load("images/circle.png")
    self.power_bg_img=pygame.image.load("images/square.png")
    self.power_img=pygame.image.load("images/square.png")
    self.shadow_img=pygame.image.load("images/circle.png")

  def scale(self):
    #Scale UI images
    self.health_bg_img=pygame.transform.scale(self.health_bg_img,(200,20))
    self.dot_img=pygame.transform.scale(self.dot_img,(8,8))
    self.power_bg_img=pygame.transform.scale(self.power_bg_img,(200,20))
    self.shadow_img=pygame.transform.scale(self.shadow_img,(50,50))

  def colour(self):
    #Change colours
    var=pygame.PixelArray(self.health_bg_img)
    var.replace((0,0,0),(50,50,50))
    del var
    
    var=pygame.PixelArray(self.health_img)
    var.replace((0,0,0),(255,0,0))
    del var
    
    var=pygame.PixelArray(self.dot_img)
    var.replace((0,0,0),(50,50,50))
    del var
    
    var=pygame.PixelArray(self.shadow_img)
    var.replace((0,0,0),(50,50,50))
    del var

class buttons:
  def __init__(self):
    #Load buttons images
    self.backimg=pygame.image.load("buttons/back.png").convert_alpha()
    self.quitimg=pygame.image.load("buttons/quit.png").convert_alpha()
    self.resumeimg=pygame.image.load("buttons/resume.png").convert_alpha()
    self.levelsimg=pygame.image.load("buttons/levels.png").convert_alpha()
    self.levelimgs=[]
    for i in range(5):
      self.levelimgs.append(pygame.image.load("buttons/level "+str(i+1)+".png"))
