import random
from time import time

from mutation import *
from models import *
from crossing import *
from selection import *
from functions import *
from pick import *


CONFIG = {
	"dimension": 8,
	"maximum": 5,
	"function": sphere_function,
}

if __name__ == "__main__":
	random.seed(time)

	population = Population(Agent, 100, CONFIG)
	population.run()

