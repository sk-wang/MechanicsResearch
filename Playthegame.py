'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''
#theCountoftiles
import random
import time
import tracery
import os
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *
global zelda_level,zelda_game,red,blue,green,now_zelda_game,scorelimit,rules,template,mapgenerator,nowlevel
global scorelimit,redlimit,greenlimit,bluelimit,timelimit,damagelimit,widthlimit,initialrate,dosteplimit,brithlimit,deadlimit
global redcooldownlimit,bluecooldownlimit,scooldownlimit
#rulelimit
scorelimit = range(5,21,1)
redlimit = range(2,10,1)
greenlimit = range(2,10,1)
bluelimit = range(2,10,1)
timelimit = range(100,200,1)
damagelimit = range(-5,11,1)
widthlimit = range(16,25,1)
brithlimit = range(4,6,1)
deadlimit = range(4,6,1)
initialrate = range(3,6,1)
key = 0
for rate in initialrate:
  initialrate[key] = float(rate)/10.
  key+=1
dosteplimit = range(1,7,1)
redcooldownlimit = range(1,5,1)
greencooldownlimit = range(1,5,1)
bluecooldownlimit = range(1,5,1)
scooldownlimit = range(1,5,1)
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
initPos = int(random.uniform(0,49))
direction = int(random.uniform(0,1))
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
moveType = ['Immovable','CounterClockwiseSprite','ClockwiseSprite','RandomNPC']
interactionType = ['no','killSprite','killPartner','teleportPartner','teleportSprite','teleportBoth','killBoth']
#linkType = ['NNSprite israndom=0','ShootNNSprite stype=sword israndom=0','ShootNNSprite stype=bullet israndom=0','ShootNNSprite stype=wall israndom=0']
linkRule = {
    'link': '#agentType# stype=#stype# israndom=#israndom# ismove=#ismove#',
    'agentType': ['NNAvatar'],
    'stype': ['bullet'],
    'israndom': ['0'],
    'ismove':['1']
}
grammar = tracery.Grammar(linkRule)
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
    bullet red > killBoth score={bulletredScore}
    bullet blue > killBoth score={bulletblueScore} 
    bullet green > killBoth score={bulletgreenScore}
    bullet wall > killBoth      
  TerminationSet
    LinkDead score=-1 win=False
    Timeout limit={timelimit} win=True
    Scoreout limit={scorelimit} win=True
"""
def evaluate(fnn,iteration=5,isScreen=False):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,mapgenerator,nowlevel
  if __name__ == "__main__":
    from vgdl.core import VGDLParser
    TotalScore = 0.
    for i in range(iteration):
      redCount = 0
      greenCount = 0
      blueCount = 0
      thislevel = mapgenerator.generate()
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
      print now_zelda_game
      os.system('read')
      game = VGDLParser.playGame(now_zelda_game, zelda_this_level, fnn = fnn , isScreen=True)
      TotalScore += (game.score/float(scorelimit))
    return TotalScore/float(iteration)

def evaulateGame():
  global zelda_game,now_zelda_game,rules
  #buildNetWork
  net = buildNetwork(108,10,8,hiddenclass=SigmoidLayer)
 
  #randomMove
  avg = 0
  oldlink = rules[3]
  rules[3] = rules[3].replace('random=0','random=1')
  print rules[3]
  setRule(rules)
  print "randomPlay"
  for i in range(10):
    avg += evaluate(net)
  """
  rules[3] = 'ShootNNSprite stype=sword israndom=1'
  setRule(rules)
  print "randomShootNNSprite"
  for i in range(20):
    avg += evaluate(net)
  rules[3] = 'ShootNNSprite stype=bullet israndom=1'
  setRule(rules)
  print "randomShootNNSprite"
  for i in range(20):
    avg += evaluate(net)
  """
  if(avg / 10.0 > 0.3):
    return -1,net

  from pybrain.optimization import SNES
  from pybrain.optimization import OriginalNES
  from pybrain.optimization import GA
  from numpy import ndarray

  rules[3] = oldlink
  setRule(rules)
  best = 0
  algo = SNES(lambda x: evaluate(x), net, verbose=True, desiredEvaluation=0.85)
  #algo = GA(lambda x: evaluate(x), net, verbose=True)
  #algo = OriginalNES(lambda x: evaluate(x), net, verbose=True, desiredEvaluation=0.85)
  episodesPerStep = 2
  for i in range(5):
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
  print now_zelda_game
  return best,net
def setRule(thisrules):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,rules,mapgenerator
  global scorelimit,redlimit,greenlimit,bluelimit,timelimit,damagelimit,widthlimit,initialrate,dosteplimit,brithlimit,deadlimit
  rules = thisrules
  print thisrules
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
  mapgenerator = generatedMap(width=thisrules[45],brithlimit=thisrules[46],deadlimit=thisrules[47],density=thisrules[48],simulationtime=thisrules[49])
  now_zelda_game = now_zelda_game.replace('{redcooldown}',thisrules[50])
  now_zelda_game = now_zelda_game.replace('{greencooldown}',thisrules[51])
  now_zelda_game = now_zelda_game.replace('{bluecooldown}',thisrules[52])
  now_zelda_game = now_zelda_game.replace('{scooldown}',thisrules[53])
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
  rules[22] = random.choice(scorelimit)
  #red green blue from my own experience
  rules[23] = random.choice(redlimit)
  rules[24] = random.choice(greenlimit)
  rules[25] = random.choice(bluelimit)
  #timelimit accoring to my own experience
  rules[26] = str(random.choice(timelimit))

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
  setRule(rules)
  #randomGame
  
#start
initial()
eva,net = evaulateGame()
#f = open('/Users/skwang/Desktop/stats', 'a+')
#print >> f,now_zelda_game,net,net.params,eva,red,blue,green
"""
nowgame = template
nowgame = nowgame.replace('{red}',str(red))
nowgame = nowgame.replace('{blue}',str(blue))
nowgame = nowgame.replace('{green}',str(green))
nowgame = nowgame.replace('{game}',now_zelda_game)
netStr = '['
for weigh in net.params:
  netStr = netStr + str(weigh) + ','
netStr = netStr[0:len(netStr)-2] + ']'
nowgame = nowgame.replace('{net}',netStr)
f = open('/Users/skwang/MechanicsResearch/'+str(int(time.time())) + '.py', 'w+')
print >> f,nowgame
print "written"
"""
lastEva = eva
lastrules = rules
nogame = 0
i = 0
while(i < 999999):
  i = i + 1
  thisrules = lastrules
  #mutate
  #print >> f,'Generation'+str(i)+':'
  if(int(random.uniform(1,27)) == 3):
    thisrules[0] = random.choice(moveType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[1] = random.choice(moveType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[2] = random.choice(moveType)
  if(int(random.uniform(1,27)) == 3):
    thisrules[3] = grammar.flatten("#link#")
  #interaction
  if(int(random.uniform(1,27)) == 3):
    thisrules[4] = random.choice(interactionType)
  if(int(random.uniform(1,27)) == 3):
    thisrules[5] = random.choice(interactionType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[6] = random.choice(interactionType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[7] = random.choice(interactionType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[8] = random.choice(interactionType)
  if(int(random.uniform(1,27)) == 3):  
    thisrules[9] = random.choice(interactionType)
  #score
  if(int(random.uniform(1,27)) == 3):
    thisrules[10] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[11] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[12] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[13] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[14] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[15] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[16] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[17] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[18] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[19] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[20] = str(random.choice(score))
  if(int(random.uniform(1,27)) == 3):
    thisrules[21] = str(random.choice(score))
  #limit
  if(int(random.uniform(1,27)) == 3):
    thisrules[22] = int(random.choice(scorelimit))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[23] = int(random.choice(redlimit))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[24] = int(random.choice(greenlimit))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[25] = int(random.choice(bluelimit))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[26] = str(random.choice(timelimit))
  #damage
  if(int(random.uniform(1,27)) == 3): 
    thisrules[27]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[28]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[29]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[30]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[31]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[32]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[33]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[34]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[35]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[36]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[37]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[38]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[39]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[40]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[41]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[42]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[43]= str(random.choice(damagelimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[44]= str(random.choice(damagelimit))
  #level
  if(int(random.uniform(1,27)) == 3): 
    thisrules[45]= int(random.choice(widthlimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[46]= int(random.choice(brithlimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[47]= int(random.choice(deadlimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[48]= random.choice(initialrate)
  if(int(random.uniform(1,27)) == 3): 
    thisrules[49]= int(random.choice(dosteplimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[50]= str(int(random.choice(redcooldownlimit)))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[51]= str(random.choice(greencooldownlimit))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[52]= str(int(random.choice(bluecooldownlimit)))
  if(int(random.uniform(1,27)) == 3): 
    thisrules[53]= str(int(random.choice(scooldownlimit)))
  setRule(thisrules)  
  eva,net = evaulateGame()
  if(eva > lastEva):
    lastEva = eva
    lastrules = thisrules
    #f = open('/Users/skwang/Desktop/stats', 'a+')
    #print >> f,now_zelda_game,net,net.params,eva,red,blue,green
    nowgame = template
    nowgame = nowgame.replace('{red}',str(red))
    nowgame = nowgame.replace('{blue}',str(blue))
    nowgame = nowgame.replace('{green}',str(green))
    nowgame = nowgame.replace('{game}',now_zelda_game)
    nowgame = nowgame.replace('{width}',str(thisrules[45]))
    nowgame = nowgame.replace('{brith}',str(thisrules[46]))
    nowgame = nowgame.replace('{dead}',str(thisrules[47]))
    nowgame = nowgame.replace('{density}',str(thisrules[48]))
    nowgame = nowgame.replace('{time}',str(thisrules[49]))
    netStr = '['
    for weigh in net.params:
      netStr = netStr + str(weigh) + ','
    netStr = netStr[0:len(netStr)-2] + ']'
    nowgame = nowgame.replace('{net}',netStr)
    g = open(os.path.dirname(os.path.realpath(__file__))+"/"+str(int(time.time())) + 'Generation'+str(i) + 'Eva' + str(eva)+'.py', 'w+')
    print >> g,nowgame
    print "written"
    g.close()
    nogame = 0
  else:
    setRule(lastrules)
    nogame=nogame+1
    if(nogame>=10):
      initial()
      nogame = 0
      eva,net = evaulateGame()
      #f = open('/Users/skwang/Desktop/stats', 'a+')
      #print >> f,"new generation",now_zelda_game,net,net.params,eva,red,blue,green
      lastEva = eva
      lastGame = now_zelda_game
      i = 0