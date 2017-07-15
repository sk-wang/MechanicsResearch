'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''
#theCountoftiles
import random
import time
import tracery
import os
import copy
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *
global zelda_level,zelda_game,red,blue,green,now_zelda_game,scorelimit,rules,template,mapgenerator,nowlevel
global scoremaxlimit,redlimit,greenlimit,bluelimit,timelimit,damagelimit,widthlimit,initialrate,dosteplimit,brithlimit,deadlimit
#rulelimit
scoremaxlimit = range(5,21,1)
redlimit = range(2,10,1)
greenlimit = range(2,10,1)
bluelimit = range(2,10,1)
timelimit = range(50,100,1)
damagelimit = range(1,11,1)
widthlimit = range(16,25,2)
brithlimit = range(4,6,1)
deadlimit = range(4,6,1)
initialrate = range(3,6,1)
initialPos = [0,1,2,3,4,5,6,7,8,9,13,14,15,16,17,18,19,20,21,22,23,24,25,26,45,46,47,48,49,50,51,52,53]
key = 0
for rate in initialrate:
  initialrate[key] = float(rate)/10.
  key+=1
dosteplimit = range(1,7,1)
redcooldownlimit = range(1,6,1)
greencooldownlimit = range(1,6,1)
bluecooldownlimit = range(1,6,1)
scooldownlimit = range(1,6,1)
connectednesslimit = [0.5,0.6,0.7,0.8,0.9,0.95]
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
  def generateWithMetrics(self,connectedness = 0.8,openness = 0):
    level_list = []
    zelda_level = ""
    tryCount = 0
    while True:
      tryCount+=1
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
      emptytiles = []
      pos = 0
      for grid in level_list:
        if(grid == " "):
          emptytiles.append(pos)
          groundCount+=1
        pos+=1
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
      #print maxLength,groundCount,connectedareas
      #openness
      opennessCount = 0
      for empty in emptytiles:
        if empty % self.width != 0 and empty - 1 not in connectedarea and level_list[empty - 1] != " ":
          continue
        if empty % self.width != self.width - 1 and empty + 1 not in connectedarea and level_list[empty + 1] != " ":
          continue
        if empty >= self.width and empty - self.width not in connectedarea and level_list[empty - self.width] != " ":
          continue
        if empty < self.width * (self.width - 1) and empty + self.width not in connectedarea and level_list[empty + self.width] != " ":
          continue
        opennessCount+=1
      if float(opennessCount)/float(groundCount) >= openness and float(maxLength)/float(groundCount) >= connectedness:
        break
    #print tryCount
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
pos = random.choice(initialPos)
threadnumber = int(random.uniform(0,99999999999))
direction = 0
nowlevel = ""
red = 3
green = 2
blue = 1
#neuralnetworkForAgent
key = 0
rules = []
template = all_the_text = open(os.path.dirname(os.path.realpath(__file__))+'/template.py').read()
print template
random.seed(time.time())
for i in range(100):
  rules.append("")
moveType = ['Immovable','CounterClockwiseSprite','ClockwiseSprite','RandomNPC','Chaser stype=link']
interactionType = ['no','killSprite','killPartner','teleportPartner','teleportSprite','teleportBoth','killBoth']
#linkType = ['NNSprite israndom=0','ShootNNSprite stype=sword israndom=0','ShootNNSprite stype=bullet israndom=0','ShootNNSprite stype=wall israndom=0']
bulletlimit = ['killBoth','killSprite']
linkRule = {
    'link': '#agentType# stype=#stype# israndom=#israndom# ismove=#ismove#',
    'agentType': ['ShootNNSprite'],
    'stype': ['bullet'],
    'israndom': ['0'],
    'ismove':['1']
}
grammar = tracery.Grammar(linkRule)
#according to paper
score = [-1,0,1]
zelda_level = """
wwwwwwwwwwwwwwww
w              w
w              w
w              w
w   wwwwwwww   w
w              w
w              w
w       L      w
w              w
w              w
w   wwwwwwww   w
w              w
w              w
w              w
wwwwwwwwwwwwwwww
"""

zelda_game = """
BasicGame
  SpriteSet  
    sword > Flicker limit=0.05 singleton=True color=BLACK
    bullet > Bullet
      leftbullet > orientation=LEFT speed=0.5  color=YELLOW
      rightbullet > orientation=RIGHT speed=0.5  color=YELLOW
      upbullet > orientation=UP speed=0.5  color=YELLOW
      downbullet > orientation=DOWN speed=0.5  color=YELLOW
    movable >        
      red  > {redmove} color=RED cooldown={redcooldown}
      green > {greenmove} color=GREEN cooldown={greencooldown}
      blue > {bluemove} color=BLUE cooldown={bluecooldown} 
      link  > {linkmove} color=WHITE scooldown={scooldown}
    boundary > Immovable color=BLACK
  LevelMapping
    R > red
    G > green
    B > blue
    L > link  
    x > boundary          
  InteractionSet
    movable wall  > stepBack
    movable boundary > stepBack
    red green > {redgreen} score=0
    red blue > {redblue} score=0 
    green blue > {greenblue} score=0
    red link > {redlink} score={redlinkScore}
    green link > {greenlink} score={greenlinkScore}
    blue link > {bluelink} score={bluelinkScore}
    sword red > killBoth score={swordredScore}
    sword blue > killBoth score={swordblueScore}
    sword green > killBoth score={swordgreenScore}
    sword wall > killBoth  
    bullet red > {bulletred} score={bulletredScore}
    bullet blue > {bulletblue} score={bulletblueScore}
    bullet green > {bulletgreen} score={bulletgreenScore}
    bullet wall > killBoth      
  TerminationSet
    LinkDead score=-1 win=False
    Timeout limit={timelimit} win=True
    Scoreout limit={scorelimit} win=True
"""
def evaluate(fnn,iteration=20,isScreen=False,without=0):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,mapgenerator,nowlevel
  global rules
  if __name__ == "__main__":
    from vgdl.core import VGDLParser
    TotalScore = 0.
    for i in range(iteration):
      redCount = 0
      greenCount = 0
      blueCount = 0
      thislevel = mapgenerator.generateWithMetrics(connectedness=rules[57])
      nowlevel = thislevel
      zelda_level_list = list(thislevel)
      #link
      for i in range(99999):
        if(thislevel.find(' ')):
          randIndex = int(random.uniform(0, len(zelda_level_list)))
          if(zelda_level_list[randIndex] == ' '):
            zelda_level_list[randIndex] = 'L'
            break
        else:
          break
      #red
      for i in range(99999):
        if(thislevel.find(' ')):
          randIndex = int(random.uniform(0, len(zelda_level_list)))
          if(zelda_level_list[randIndex] == ' '):
            zelda_level_list[randIndex] = 'R'
            redCount+=1
            if(redCount >= red):
              break
        else:
          break
      #green
      for i in range(99999):
        if(thislevel.find(' ')):
          randIndex = int(random.uniform(0, len(zelda_level_list)))
          if(zelda_level_list[randIndex] == ' '):
            zelda_level_list[randIndex] = 'G'
            greenCount+=1
            if(greenCount >= green):
              break
        else:
          break
      #blue
      for i in range(99999):
        if(thislevel.find(' ')):
          randIndex = int(random.uniform(0, len(zelda_level_list)))
          if(zelda_level_list[randIndex] == ' '):
            zelda_level_list[randIndex] = 'B'
            blueCount+=1
            if(blueCount >= blue):
              break
        else:
          break
      zelda_this_level = ''.join(zelda_level_list)
      #print zelda_this_level
      game = VGDLParser.playGame(now_zelda_game, zelda_this_level, fnn = fnn , isScreen=False)
      if(without == 0):
        TotalScore += (game.score/float(scorelimit))
      else:
        TotalScore += game.score
    return TotalScore/float(iteration)
def evaulateGame(without = 0,iteration= 20):
  global zelda_game,now_zelda_game,rules
  #buildNetWork
  net = buildNetwork(336,10,8,hiddenclass=SigmoidLayer)
  from pybrain.optimization import SNES
  from pybrain.optimization import OriginalNES
  from pybrain.optimization import GA
  from numpy import ndarray
  best = 0
  #SNES
  algo = SNES(lambda x: evaluate(x,iteration = iteration,without=without), net, verbose=True)
  episodesPerStep = 5
  for i in range(4):
    algo.learn(episodesPerStep)
    print net.params
    if isinstance(algo.bestEvaluable, ndarray):
      net._setParameters(algo.bestEvaluable)
    else:
      net = algo.bestEvaluable
    if algo.bestEvaluation > best:
      best = algo.bestEvaluation
      """
      if best < 0.1:
        #too hard
        return -1,net
      """
  #Standard NES
  """
  net = buildNetwork(108,10,8,hiddenclass=SigmoidLayer)
  algo = OriginalNES(lambda x: evaluate(x), net, verbose=True)
  episodesPerStep = 2
  for i in range(5):
    algo.learn(episodesPerStep)
    print net.params
    if isinstance(algo.bestEvaluable, ndarray):
      net._setParameters(algo.bestEvaluable)
    else:
      net = algo.bestEvaluable
    g = open(os.path.dirname(os.path.realpath(__file__))+"/stats"+str(threadnumber)+".txt", 'a+')
    print >> g,str(net.params) + '\n' + "Standard NES:" + str(algo.bestEvaluation) + '\n'
    g.close()
    if algo.bestEvaluation > best:
      best = algo.bestEvaluation
  """
  print now_zelda_game
  return best,net
def setRule(thisrules):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,rules,mapgenerator
  rules = thisrules
  #print thisrules
  now_zelda_game = zelda_game
  now_zelda_game = now_zelda_game.replace('{redmove}',thisrules[0])
  now_zelda_game = now_zelda_game.replace('{greenmove}',thisrules[1])
  now_zelda_game = now_zelda_game.replace('{bluemove}',thisrules[2])
  now_zelda_game = now_zelda_game.replace('{linkmove}',thisrules[3])
  #interaction
  now_zelda_game = now_zelda_game.replace('{redgreen}',thisrules[4])
  now_zelda_game = now_zelda_game.replace('{redblue}',thisrules[5])
  now_zelda_game = now_zelda_game.replace('{greenblue}',thisrules[6])
  now_zelda_game = now_zelda_game.replace('{redlink}',thisrules[7])
  now_zelda_game = now_zelda_game.replace('{bluelink}',thisrules[8])
  now_zelda_game = now_zelda_game.replace('{greenlink}',thisrules[9])
  #score
  now_zelda_game = now_zelda_game.replace('{redgreenScore}',thisrules[10])
  now_zelda_game = now_zelda_game.replace('{redblueScore}',thisrules[11])
  now_zelda_game = now_zelda_game.replace('{greenblueScore}',thisrules[12])
  now_zelda_game = now_zelda_game.replace('{redlinkScore}',thisrules[13])
  now_zelda_game = now_zelda_game.replace('{greenlinkScore}',thisrules[14])
  now_zelda_game = now_zelda_game.replace('{bluelinkScore}',thisrules[15])
  now_zelda_game = now_zelda_game.replace('{swordgreenScore}',thisrules[16])
  now_zelda_game = now_zelda_game.replace('{swordblueScore}',thisrules[17])
  now_zelda_game = now_zelda_game.replace('{swordredScore}',thisrules[18])
  now_zelda_game = now_zelda_game.replace('{bulletgreenScore}',thisrules[19])
  now_zelda_game = now_zelda_game.replace('{bulletblueScore}',thisrules[20])
  now_zelda_game = now_zelda_game.replace('{bulletredScore}',thisrules[21])
  #limit
  scorelimit = thisrules[22]
  red = thisrules[23]
  blue = thisrules[24]
  green = thisrules[25]
  now_zelda_game = now_zelda_game.replace('{timelimit}',thisrules[26])
  now_zelda_game = now_zelda_game.replace('{scorelimit}',str(scorelimit))
  #damage
  """
  now_zelda_game = now_zelda_game.replace('{redgreensdam}',thisrules[27])
  now_zelda_game = now_zelda_game.replace('{redgreenpdam}',thisrules[28])
  now_zelda_game = now_zelda_game.replace('{redbluesdam}',thisrules[29])
  now_zelda_game = now_zelda_game.replace('{redbluepdam}',thisrules[30])
  now_zelda_game = now_zelda_game.replace('{greenbluesdam}',thisrules[31])
  now_zelda_game = now_zelda_game.replace('{greenbluepdam}',thisrules[32])
  now_zelda_game = now_zelda_game.replace('{redlinksdam}',thisrules[33])
  now_zelda_game = now_zelda_game.replace('{redlinkpdam}',thisrules[34])
  now_zelda_game = now_zelda_game.replace('{greenlinksdam}',thisrules[35])
  now_zelda_game = now_zelda_game.replace('{greenlinkpdam}',thisrules[36])
  now_zelda_game = now_zelda_game.replace('{bluelinksdam}',thisrules[37])
  now_zelda_game = now_zelda_game.replace('{bluelinkpdam}',thisrules[38])
  now_zelda_game = now_zelda_game.replace('{swordredpdam}',thisrules[39])
  now_zelda_game = now_zelda_game.replace('{swordgreenpdam}',thisrules[40])
  now_zelda_game = now_zelda_game.replace('{swordbluepdam}',thisrules[41])
  now_zelda_game = now_zelda_game.replace('{bulletredpdam}',thisrules[42])
  now_zelda_game = now_zelda_game.replace('{bulletgreenpdam}',thisrules[43])
  now_zelda_game = now_zelda_game.replace('{bulletbluepdam}',thisrules[44])
  """
  mapgenerator = generatedMap(width=thisrules[45],brithlimit=thisrules[46],deadlimit=thisrules[47],density=thisrules[48],simulationtime=thisrules[49])
  now_zelda_game = now_zelda_game.replace('{redcooldown}',thisrules[50])
  now_zelda_game = now_zelda_game.replace('{greencooldown}',thisrules[51])
  now_zelda_game = now_zelda_game.replace('{bluecooldown}',thisrules[52])
  now_zelda_game = now_zelda_game.replace('{scooldown}',thisrules[53])
  now_zelda_game = now_zelda_game.replace('{bulletred}',thisrules[54])
  now_zelda_game = now_zelda_game.replace('{bulletblue}',thisrules[55])
  now_zelda_game = now_zelda_game.replace('{bulletgreen}',thisrules[56])
def initial():
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,rules
  global scorelimit,redlimit,greenlimit,bluelimit,timelimit,damagelimit,widthlimit,initialrate,dosteplimit,brithlimit,deadlimit
  #initial
  rules[0] = random.choice(moveType)
  rules[1] = random.choice(moveType)
  rules[2] = random.choice(moveType)
  rules[3] = grammar.flatten("#link#")
  rules[4] = random.choice(interactionType)
  rules[5] = random.choice(interactionType)
  rules[6] = random.choice(interactionType)
  rules[7] = random.choice(interactionType)
  rules[8] = random.choice(interactionType)
  rules[9] = random.choice(interactionType)
  if(rules[4] == "no"):
    rules[10] = '0'
  else:
    rules[10] = str(random.choice(score))
  if(rules[5] == "no"):
    rules[11] = '0'
  else:
    rules[11] = str(random.choice(score))
  if(rules[6] == "no"):
    rules[12] = '0'
  else:
    rules[12] = str(random.choice(score))
  if(rules[7] == "no"):
    rules[13] = '0'
  else:
    rules[13] = str(random.choice(score))
  if(rules[8] == "no"):
    rules[14] = '0'
  else:
    rules[14] = str(random.choice(score))
  if(rules[9] == "no"):
    rules[15] = '0'
  else:
    rules[15] = str(random.choice(score))
  rules[16] = str(random.choice(score))
  rules[17] = str(random.choice(score))
  rules[18] = str(random.choice(score))
  rules[19] = str(random.choice(score))
  rules[20] = str(random.choice(score))
  rules[21] = str(random.choice(score))
  #score limit from paper
  rules[22] = random.choice(scoremaxlimit)
  #red green blue from my own experience
  rules[23] = random.choice(redlimit)
  rules[24] = random.choice(greenlimit)
  rules[25] = random.choice(bluelimit)
  #timelimit accoring to my own experience
  rules[26] = str(random.choice(timelimit))

  """
  #damage from my own experience
  rules[27]= str(random.choice(damagelimit))
  rules[28]= str(random.choice(damagelimit))
  rules[29]= str(random.choice(damagelimit))
  rules[30]= str(random.choice(damagelimit))
  rules[31]= str(random.choice(damagelimit))
  rules[32]= str(random.choice(damagelimit))
  rules[33]= str(random.choice(damagelimit))
  rules[34]= str(random.choice(damagelimit))
  rules[35]= str(random.choice(damagelimit))
  rules[36]= str(random.choice(damagelimit))
  rules[37]= str(random.choice(damagelimit))
  rules[38]= str(random.choice(damagelimit))
  rules[39]= str(random.choice(damagelimit))
  rules[40]= str(random.choice(damagelimit))
  rules[41]= str(random.choice(damagelimit))
  rules[42]= str(random.choice(damagelimit))
  rules[43]= str(random.choice(damagelimit))
  rules[44]= str(random.choice(damagelimit))
  """
  #level from page https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664
  rules[45]= random.choice(widthlimit)
  rules[46]= random.choice(brithlimit)
  rules[47]= random.choice(deadlimit)
  rules[48]= random.choice(initialrate)
  rules[49]= random.choice(dosteplimit)
  rules[50]= str(random.choice(redcooldownlimit))
  rules[51]= str(random.choice(greencooldownlimit))
  rules[52]= str(random.choice(bluecooldownlimit))
  rules[53]= str(random.choice(scooldownlimit))
  rules[54]= random.choice(bulletlimit)
  rules[55]= random.choice(bulletlimit)
  rules[56]= random.choice(bulletlimit)
  rules[57]= random.choice(connectednesslimit)
  setRule(rules)
  #randomGame

def certainInitial():
  global rules
  rules[0] = "Chaser stype=link"
  rules[1] = "CounterClockwiseSprite"
  rules[2] = "ClockwiseSprite"
  rules[3] = "ShootNNSprite stype=bullet israndom=0 ismove=1"
  rules[4] = "teleportSprite"
  rules[5] = "teleportSprite"
  rules[6] = "teleportSprite"
  rules[7] = "teleportPartner"
  rules[8] = "teleportSprite"
  rules[9] = "killPartner"
  rules[10] = '0'
  rules[11] = '0'
  rules[12] = '0'
  rules[13] = '-1'
  rules[14] = '0'
  rules[15] = '0'
  rules[16] = '0'
  rules[17] = '-1'
  rules[18] = '-1'
  rules[19] = '1'
  rules[20] = '0'
  rules[21] = '0'
  #score limit from paper
  rules[22] = '5'
  #red green blue from my own experience
  rules[23] = 5
  rules[24] = 5
  rules[25] = 5
  #timelimit accoring to my own experience
  rules[26] = '100'

  #damage from my own experience
  rules[27]= 6
  rules[28]= 3
  rules[29]= 2
  rules[30]= 10
  rules[31]= 7
  rules[32]= 2
  rules[33]= 1
  rules[34]= 3
  rules[35]= 7
  rules[36]= 6
  rules[37]= 1
  rules[38]= 10
  rules[39]= 7
  rules[40]= 4
  rules[41]= 4
  rules[42]= 10
  rules[43]= 1
  rules[44]= 1
  rules[45]= 20
  rules[46]= 5
  rules[47]= 5
  rules[48]= 0.3
  rules[49]= 6
  rules[50]= '3'
  rules[51]= '3'
  rules[52]= '5'
  rules[53]= '2'
  rules[54]= 'killSprite'
  rules[55]= 'killSprite'
  rules[56]= 'killBoth'
  rules[57] = 0.8
  setRule(rules)
  #certainGame  
#start
certainInitial()
i = 1
while(i < 999999):
  eva,net = evaulateGame(iteration = i)
  #validate
  evaval = evaluate(net)
  g = open(os.path.dirname(os.path.realpath(__file__))+"/iteration.txt", 'a+')
  print >> g,'evaulation is ' + str(eva) + 'validation is ' + str(evaval) +' and iteration per game is '+str(i)+'\n'
  g.close()
  i+=1
