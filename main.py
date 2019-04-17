import random
from time import time

from mutation import *
from models import *
from crossing import *
from selection import *
from functions import *
from pick import *


AGENT_CONFIG = {
	'dimension': 2,
	'maximum': 5.12,
	'function': sphere_function,
	'global_min': 0,
}

CONFIG = {
	'stag_coef': 0.00001,
	'max_stag_iter': 100,
	'max_iter': 10000,
	'multistart_cnt': 100,
	'core_cnt': 4,
	'population_size': 100,
}

if __name__ == '__main__':
	random.seed(time)

	now = time()
	for _ in range(5):
		population = Population(Agent, 100, AGENT_CONFIG, CONFIG, 'log.txt')
		population.run()
		population.deinit()
		AGENT_CONFIG['dimension'] *= 2
	print(time() - now)

