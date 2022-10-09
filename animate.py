import pygame
import time

def mod(a,b):
  c=b*(a/b-a//b)
  return c
  
class animate:
  def __init__(self,sprites,step,surface,**list):
    self.sprites=sprites
    self.step=step# Either the amount of time per rotate or the number of times it will rotate
    self.total=len(sprites)
    self.surface=surface
    self.on=False
    if "list" in list:
      self.list=list["list"]
      self.noips=len(self.list)/len(self.sprites)#number of indexes per sprite
      
  def start(self):
    self.on=True
    
  def update(self,x,y):#Do the animation at a set speed
    if self.on:
      timer=mod(time.time(),self.total*self.step)
      for i in range(self.total):
        if i*self.step<=timer<(i+1)*self.step:
          self.surface.blit(self.sprites[i],(x,y))
          
  def update2(self,x,y,index): #Do the animation a set number of times
    if self.on:
      print(self.noips,index)
      for i in range(len(self.sprites)):
        if self.noips*i<=index<self.noips*(i+1):
          print(10-i)
          self.surface.blit(self.sprites[7-i],(x,y))
      
  def stop(self):
    self.on=False