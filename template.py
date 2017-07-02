import random
import time
import tracery
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *
red = {red}
green = {green}
blue = {blue}
net = buildNetwork(60,10,8,hiddenclass=SigmoidLayer)
net._setParameters({net})
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
	VGDLParser.playGame(zelda_game, zelda_this_level, fnn = net , isScreen=True)