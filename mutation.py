from random import gauss
import numpy as np


def mutation_michalewicz(agent, coef):
	def func(y):
		u2 = np.random.rand()
		return y * (1 - u2 ** ((1 - (coef)) ** 5))

	gens = agent.gens
	new_gens = []

	for gen in gens:
		if np.random.randint(0, 2):
			new_gens.append(gen + func(agent.maximum - gen))
		else:
			new_gens.append(gen - func(gen - agent.maximum))
	agent.gens = new_gens
	agent.limit()


def mutation_gauss(agent, coef):
	gens = agent.gens
	new_gens = []

	for gen in gens:
		new_gens.append(gen + gauss(0, coef))
	agent.gens = new_gens
	agent.limit()


def mutation_geometric_shift(agent, coef):
	gens = agent.gens
	new_gens = []

	for gen in gens:
		u = np.random.rand()
		new_gens.append(gen - gen * coef * (2 * u - 1))
	agent.limit()
