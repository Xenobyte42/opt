import random
from time import time

from mutation import *
from models import *
from crossing import *
from selection import *
from functions import *
from pick import *


CONFIG = {
	"dimension": 32,
	"maximum": 5,
	"function": rozenbrock_function,
}

if __name__ == "__main__":
	random.seed(time)

	population = Population(Agent, 100, CONFIG, 'log.txt')
	population.run()
	population.deinit()
	# for _ in range(5):
	# 	population = Population(Agent, 100, CONFIG, 'log.txt')
	# 	population.run()
	# 	population.deinit()
	# 	CONFIG["dimension"] *= 2

