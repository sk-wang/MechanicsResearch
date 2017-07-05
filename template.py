import random
import time
import tracery
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *
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
    for i in range(self.width * self.width):
      zelda_level = zelda_level + level_list[i]
      if(i % self.width == self.width - 1):
        zelda_level = zelda_level + '\n'
    return zelda_level
red = {red}
green = {green}
blue = {blue}
net = buildNetwork(108,10,8,hiddenclass=SigmoidLayer)
net._setParameters({net})
mapgenerator = generatedMap(width={width},brithlimit={brith},deadlimit={dead},density={density},simulationtime={time})
zelda_level = mapgenerator.generate()
random.seed(time.time())
zelda_game="""
{game}
"""
if __name__ == "__main__":
	from vgdl.core import VGDLParser
	redCount = 0
	greenCount = 0
	blueCount = 0
	zelda_level_list = list(zelda_level)
	#link
	for i in range(99999):
		if(zelda_level.find(' ')):
		  randIndex = int(random.uniform(0, len(zelda_level)))
		  if(zelda_level_list[randIndex] == ' '):
		    zelda_level_list[randIndex] = 'L'
		    break
		else:
		  break
	#red
	for i in range(99999):
		if(zelda_level.find(' ')):
		  randIndex = int(random.uniform(0, len(zelda_level)))
		  if(zelda_level_list[randIndex] == ' '):
		    zelda_level_list[randIndex] = 'R'
		    redCount+=1
		    if(redCount >= red):
		      break
		else:
		  break
	#green
	for i in range(99999):
		if(zelda_level.find(' ')):
		  randIndex = int(random.uniform(0, len(zelda_level)))
		  if(zelda_level_list[randIndex] == ' '):
		    zelda_level_list[randIndex] = 'G'
		    greenCount+=1
		    if(greenCount >= green):
		      break
		else:
		  break
	#blue
	for i in range(99999):
		if(zelda_level.find(' ')):
		  randIndex = int(random.uniform(0, len(zelda_level)))
		  if(zelda_level_list[randIndex] == ' '):
		    zelda_level_list[randIndex] = 'B'
		    blueCount+=1
		    if(blueCount >= blue):
		      break
		else:
		  break
	zelda_this_level = ''.join(zelda_level_list)
	VGDLParser.playGame(zelda_game, zelda_this_level, fnn = net , isScreen=True)