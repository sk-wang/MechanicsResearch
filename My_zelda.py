'''
VGDL example: a simplified Zelda variant: Link has a sword, needs to get a key and open the door.

@author: Tom Schaul
'''
#theCountoftiles
import random
import time
import tracery
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *
global zelda_level,zelda_game,red,blue,green,now_zelda_game,scorelimit,rules
red = 3
green = 2
blue = 1
#neuralnetworkForAgent
key = 0
rules = []
random.seed(time.time())
for i in range(100):
  rules.append("")
moveType = ['Immovable','CounterClockwiseSprite','ClockwiseSprite','RandomNPC','RandomNPCHorizontal','RandomNPCVertical']
interactionType = ['none','killSprite','killPartner','teleportPartner','teleportSprite','teleportBoth','killBoth']
linkType = ['NNSprite israndom=0','ShootNNSprite stype=sword israndom=0','ShootNNSprite stype=bullet israndom=0','ShootNNSprite stype=wall israndom=0']
linkRule = {
    'link': '#agentType# stype=#stype# israndom=#israndom# ismove=#ismove#',
    'agentType': ['NNSprite', 'ShootNNSprite'],
    'stype': ['sword', 'wall', 'bullet'],
    'israndom': ['0','1'],
    'ismove':['0','1']
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
    sword > Flicker limit=5 singleton=True color=BLACK
    bullet > Bullet
      leftbullet > orientation=LEFT speed=0.5  color=YELLOW
      rightbullet > orientation=RIGHT speed=0.5  color=YELLOW
      upbullet > orientation=UP speed=0.5  color=YELLOW
      downbullet > orientation=DOWN speed=0.5  color=YELLOW
    movable >        
      red  > {redmove} color=RED
      green > {greenmove} color=GREEN
      blue > {bluemove} color=BLUE
      link  > {linkmove} color=WHITE scooldown=5
  LevelMapping
    R > red
    G > green
    B > blue
    L > link            
  InteractionSet
    movable wall  > stepBack
    red green > {redgreen} score={redgreenScore}
    red blue > {redblue} score={redblueScore}
    green blue > {greenblue} score={greenblueScore}
    red link > {redlink} score={redlinkScore}
    green link > {greenlink} score={greenlinkScore}
    blue link > {bluelink} score={bluelinkScore} 
    sword red > killBoth score={swordredScore} 
    sword blue > killBoth score={swordblueScore} 
    sword green > killBoth score={swordgreenScore}
    bullet red > killBoth score={bulletredScore} 
    bullet blue > killBoth score={bulletblueScore} 
    bullet green > killBoth score={bulletgreenScore}          
  TerminationSet
    LinkDead score=-1 win=False
    Timeout limit={timelimit} win=True
    Scoreout limit={scorelimit} win=True
"""
def evaluate(fnn,iteration=20,isScreen=False):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit
  if __name__ == "__main__":
    from vgdl.core import VGDLParser
    TotalScore = 0.
    for i in range(iteration):
      redCount = 0
      greenCount = 0
      blueCount = 0
      zelda_level_list = list(zelda_level)
      #red
      for i in range(99999):
        randIndex = int(random.uniform(0, len(zelda_level)))
        if(zelda_level_list[randIndex] == ' '):
          zelda_level_list[randIndex] = 'R'
          redCount+=1
          if(redCount >= red):
            break
      #green
      for i in range(99999):
        randIndex = int(random.uniform(0, len(zelda_level)))
        if(zelda_level_list[randIndex] == ' '):
          zelda_level_list[randIndex] = 'G'
          greenCount+=1
          if(greenCount >= green):
            break
      #blue
      for i in range(99999):
        randIndex = int(random.uniform(0, len(zelda_level)))
        if(zelda_level_list[randIndex] == ' '):
          zelda_level_list[randIndex] = 'B'
          blueCount+=1
          if(blueCount >= blue):
            break
      zelda_this_level = ''.join(zelda_level_list)
      game = VGDLParser.playGame(now_zelda_game, zelda_this_level, fnn = fnn , isScreen=False)
      TotalScore += (game.score/float(scorelimit))
    return TotalScore/float(iteration)

def evaulateGame():
  global zelda_game,now_zelda_game,rules
  #buildNetWork
  net = buildNetwork(60,10,8,hiddenclass=SigmoidLayer)
 
  #randomMove
  avg = 0
  oldlink = rules[3]
  rules[3] = 'NNSprite israndom=1'
  setRule(rules)
  print "randomNNSprite"
  for i in range(20):
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
  if(avg / 60.0 > 0.3):
    return -1,net
  """
  from pybrain.optimization import SNES
  from numpy import ndarray

  rules[3] = oldlink
  setRule(rules)
  best = 0
  algo = SNES(lambda x: evaluate(x), net, verbose=True, desiredEvaluation=0.85)
  episodesPerStep = 5
  for i in range(10):
    algo.learn(episodesPerStep)
    if isinstance(algo.bestEvaluable, ndarray):
      net._setParameters(algo.bestEvaluable)
    else:
      net = algo.bestEvaluable
    if algo.bestEvaluation > best:
      best = algo.bestEvaluation
  print now_zelda_game
  return best,net
def setRule(thisrules):
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,rules
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
def initial():
  global zelda_level,zelda_game,now_zelda_game,red,blue,green,scorelimit,rules
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
  rules[10] = str(random.choice(score))
  rules[11] = str(random.choice(score))
  rules[12] = str(random.choice(score))
  rules[13] = str(random.choice(score))
  rules[14] = str(random.choice(score))
  rules[15] = str(random.choice(score))
  rules[16] = str(random.choice(score))
  rules[17] = str(random.choice(score))
  rules[18] = str(random.choice(score))
  rules[19] = str(random.choice(score))
  rules[20] = str(random.choice(score))
  rules[21] = str(random.choice(score))
  rules[22] = int(random.uniform(1,10))
  rules[23] = int(random.uniform(0,20))
  rules[24] = int(random.uniform(0,20))
  rules[25] = int(random.uniform(0,20))
  rules[26] = str(int(random.uniform(1,100)))
  setRule(rules)
  #randomGame
  
#start
initial()
eva,net = evaulateGame()
f = open('/Users/skwang/Desktop/stats', 'a+')
print >> f,now_zelda_game,net,net.params,eva,red,blue,green
lastEva = eva
lastrules = rules
nogame = 0
i = 0
while(i < 999999):
  i = i + 1
  thisrules = lastrules
  #mutate
  print >> f,'Generation'+str(i)+':'
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
    thisrules[22] = int(random.uniform(1,10))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[23] = int(random.uniform(0,20))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[24] = int(random.uniform(0,20))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[25] = int(random.uniform(0,20))
  if(int(random.uniform(1,27)) == 3):  
    thisrules[26] = str(int(random.uniform(1,100)))
  setRule(thisrules)  
  eva,net = evaulateGame()
  if(eva > lastEva):
    lastEva = eva
    lastrules = thisrules
    f = open('/Users/skwang/Desktop/stats', 'a+')
    print >> f,now_zelda_game,net,net.params,eva,red,blue,green
    nogame = 0
  else:
    setRule(lastrules)
    nogame=nogame+1
    if(nogame>=10):
      initial()
      nogame = 0
      eva,net = evaulateGame()
      f = open('/Users/skwang/Desktop/stats', 'a+')
      print >> f,"new generation",now_zelda_game,net,net.params,eva,red,blue,green
      lastEva = eva
      lastGame = now_zelda_game
      i = 0