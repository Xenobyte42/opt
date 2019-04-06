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
	population.add_picks(pick_tourney)
	population.add_selections(selection_outbreeding, selection_inbreeding)
	population.add_mutations(mutation_michalewicz, mutation_gauss, mutation_geometric_shift)
	population.add_crossings(crossing_arithmetical, crossing_fuzzy, crossing_x3linear)
	print("\n" * 2)
	print(len(population.population))
	for _ in range(len(population)):
		first, second = selection_inbreeding(population)
		new_agents = crossing_x3linear(population.population[first],
			population.population[second])
		population.population += new_agents
	print("\n" * 2)
	print(len(population.population))
	pick_tourney(population, 3)
	print("\n" * 2)
	print(len(population.population))

