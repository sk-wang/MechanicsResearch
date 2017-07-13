import random
import time
class generatedMap(object):
  width =64
  brithlimit = 4
  deadlimit = 4
  density = 0.4
  simulationtime = 6
  def __init__(self,width=64,brithlimit=4,deadlimit=4,density=0.4,simulationtime = 6):
    self.width = width
    self.brithlimit = brithlimit
    self.deadlimit = deadlimit
    self.density = density
    self.simulationtime = simulationtime
  def countAliveNeighbours(self,thismap, x, y):
      count = 0;
      for i in range(-1,2): 
          for j in range(-1,2):
            neighbour_x = x+i
            neighbour_y = y+j
            if(i == 0 and j == 0):
              count
            elif (neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= self.width or neighbour_y >= self.width):
                count = count + 1
            elif (thismap[neighbour_x + neighbour_y * self.width] == "w"):
                count = count + 1
      return count
  def doSimulationStep(self,oldMap):
      newMap = [0 for i in range(self.width * self.width)];
      for x in range(self.width): 
          for y in range(self.width):
              nbs = self.countAliveNeighbours(oldMap, x, y)
              if(oldMap[x + y * self.width] == "w"):
                  if(nbs < self.deadlimit):
                      newMap[x + y * self.width] = " "
                  else:
                      newMap[x + y * self.width] = "w"   
              else:
                  if(nbs > self.brithlimit):
                      newMap[x + y * self.width] = "w"
                  else:
                      newMap[x + y * self.width] = " "
      return newMap
  def generateWithConnectedness(self,connectedness):
    level_list = []
    zelda_level = ""
    while True:
      #init level
      level_list = []
      zelda_level = ""
      """
      for i in range(4096):
        if(i < 4096 * density):
          level_list.append('w')
        else:
          level_list.append(' ')
      random.shuffle(level_list)
      """
      for i in range(self.width * self.width):
        if(random.uniform(0,1) < self.density):
          level_list.append('w')
        else:
          level_list.append(' ')
      #connect
      for i in range(self.simulationtime):
          level_list = self.doSimulationStep(level_list)
      #count the total ground
      groundCount = 0
      for grid in level_list:
        if(grid == " "):
          groundCount+=1
      #find the connected area
      connectedareas = []
      #start finding
      while True:
        #find the flood initial point
        while True:
          chosengridPos = int(random.uniform(0,len(level_list)))
          chosengrid = level_list[chosengridPos]
          if(chosengrid == " "):
            exist = False
            for connectedarea in connectedareas:
              if chosengridPos in connectedarea:
                exist = True
            if(exist == False):
              break
        connectedareas.append(self.flood(chosengridPos,level_list))
        totalLength = 0
        for connectedarea in connectedareas:
          totalLength += len(connectedarea)
        if(totalLength >= groundCount):
          break
      maxLength = 0
      for connectedarea in connectedareas:
        if len(connectedarea) > maxLength:
          maxLength = len(connectedarea)
      print maxLength,groundCount,connectedareas
      if float(maxLength)/float(groundCount) >= connectedness:
        break
    for i in range(self.width+2):
      zelda_level = zelda_level + 'x'
    zelda_level = zelda_level + '\n'
    for i in range(self.width * self.width):
      if(i % self.width == 0):
        zelda_level = zelda_level + 'x'
      zelda_level = zelda_level + level_list[i]
      if(i % self.width == self.width - 1):
        zelda_level = zelda_level + 'x\n'
    for i in range(self.width+2):
      zelda_level = zelda_level + 'x'
    return zelda_level
  def flood(self,pos,level_list):
    connectedarea = [pos]
    while True:
      lastLen = len(connectedarea)
      for grid in connectedarea:
        if(grid % self.width != 0):
          #noleft
          if grid - 1 not in connectedarea and level_list[grid - 1] == " ":
            connectedarea.append(grid - 1)
        if(grid % self.width != self.width - 1):
          #noright
          if grid + 1 not in connectedarea and level_list[grid + 1] == " ":
            connectedarea.append(grid + 1)
        if(grid >= self.width):
          #notop
          if grid - self.width not in connectedarea and level_list[grid - self.width] == " ":
            connectedarea.append(grid - self.width)
        if(grid < self.width * (self.width - 1)):
          #nobottom
          if grid + self.width not in connectedarea and level_list[grid + self.width] == " ":
            connectedarea.append(grid + self.width)
      if lastLen == len(connectedarea):
        break
    return connectedarea
  def generate(self):
    #init level
    level_list = []
    zelda_level = ""
    """
    for i in range(4096):
      if(i < 4096 * density):
        level_list.append('w')
      else:
        level_list.append(' ')
    random.shuffle(level_list)
    """
    for i in range(self.width * self.width):
      if(random.uniform(0,1) < self.density):
        level_list.append('w')
      else:
        level_list.append(' ')
    #connect
    for i in range(self.simulationtime):
        level_list = self.doSimulationStep(level_list)
    for i in range(self.width+2):
      zelda_level = zelda_level + 'x'
    zelda_level = zelda_level + '\n'
    for i in range(self.width * self.width):
      if(i % self.width == 0):
        zelda_level = zelda_level + 'x'
      zelda_level = zelda_level + level_list[i]
      if(i % self.width == self.width - 1):
        zelda_level = zelda_level + 'x\n'
    for i in range(self.width+2):
      zelda_level = zelda_level + 'x'
    return zelda_level
random.seed(time.time())
mapgenerator = generatedMap(width=32,brithlimit=4,deadlimit=4,density=0.45,simulationtime=2)
zelda_game = """
BasicGame
  SpriteSet  
    link  > MovingAvatar
    boundary > Immovable color=BLACK
  LevelMapping
    L > link   
    x > boundary          
  InteractionSet
    link wall  > stepBack
    link boundary > stepBack     
  TerminationSet
    LinkDead score=-1 win=False
"""
if __name__ == "__main__":
  from vgdl.core import VGDLParser
  zelda_level = mapgenerator.generateWithConnectedness(1)
  zelda_level_list = list(zelda_level)
  for i in range(99999):
    if(zelda_level.find(' ')):
      randIndex = int(random.uniform(0, len(zelda_level)))
      if(zelda_level_list[randIndex] == ' '):
        zelda_level_list[randIndex] = 'L'
        break
    else:
      break
  zelda_this_level = ''.join(zelda_level_list)
  print zelda_this_level
  
  #VGDLParser.playGame(zelda_game,zelda_this_level, isScreen=True)