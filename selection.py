import numpy as np


def calc_distance(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	distance = 0
	for i in range(len(agent1.gens)):
		distance += np.fabs(agent1.gens[i] - agent2.gens[i])
	return distance 


def selection_outbreeding(population):
	first_idx = np.random.randint(0, len(population))
	distances = []
	sum_dist = 0
	for i in range(len(population)):
		if i == first_idx:
			continue
		distance = calc_distance(population.population[first_idx], population.population[i])
		sum_dist += distance
		distances.append(distance)
	probabilities = [d / sum_dist for d in distances]
	second_idx = np.random.choice(len(population) - 1, 1,
		p=probabilities)[0]
	if second_idx >= first_idx:
		second_idx += 1
	return [first_idx, second_idx]


def selection_inbreeding(population):
	first_idx = np.random.randint(0, len(population))
	distances = []
	sum_dist = 0
	for i in range(len(population)):
		if i == first_idx:
			continue
		distance = calc_distance(population.population[first_idx], population.population[i])
		sum_dist += distance
		distances.append(distance)
	probabilities = [d / sum_dist for d in distances]
	second_idx = np.random.choice(len(population) - 1, 1,
		p=probabilities)[0]
	if second_idx >= first_idx:
		second_idx += 1
	return [first_idx, second_idx]

