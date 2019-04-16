import random
import math


def crossing_arithmetical(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	new_gens1 = []
	new_gens2 = []
	for i in range(len(agent1.gens)):
		u = random.random()
		new_gens1.append(u * agent1.gens[i] + (1 - u) * agent2.gens[i])
		new_gens2.append(u * agent1.gens[i] - (1 - u) * agent2.gens[i])
	return [new_gens1, new_gens2]


def crossing_fuzzy(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	new_gens1 = []
	new_gens2 = []
	for i in range(len(agent1.gens)):
		delta = math.fabs(agent1.gens[i] - agent2.gens[i]) * 0.5
		new_gens1.append(random.triangular(agent1.gens[i] - delta, agent1.gens[i] + delta))
		new_gens2.append(random.triangular(agent2.gens[i] - delta, agent2.gens[i] + delta))
	return [new_gens1, new_gens2]


def crossing_x3linear(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	new_gens1 = []
	new_gens2 = []
	new_gens3 = []
	for i in range(len(agent1.gens)):
		new_gens1.append(0.5 * agent1.gens[i] + 0.5 * agent2.gens[i])
		new_gens2.append(1.5 * agent1.gens[i] - 0.5 * agent2.gens[i])
		new_gens3.append(-0.5 * agent1.gens[i] + 1.5 * agent2.gens[i])
	return [new_gens1, new_gens2, new_gens3]
