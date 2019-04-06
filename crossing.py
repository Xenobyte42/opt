import random

from models import Agent

def get_config(agent):
	return {
		"dimension": agent.dimension,
		"maximum": agent.maximum,
		"function": agent.func,
	}

def crossing_arithmetical(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	config = get_config(agent1)
	new_gens1 = []
	new_gens2 = []
	for i in range(len(agent1.gens)):
		u = random.random()
		new_gens1.append(u * agent1.gens[i] + (1 - u) * agent2.gens[i])
		new_gens2.append(u * agent1.gens[i] - (1 - u) * agent2.gens[i])
	new_agent1 = Agent(config, doinit=False)
	new_agent2 = Agent(config, doinit=False)

	new_agent1.gens = new_gens1
	new_agent2.gens = new_gens2
	new_agent1.limit()
	new_agent2.limit()
	return [new_agent1, new_agent2]

def crossing_fuzzy(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	config = get_config(agent1)
	new_gens1 = []
	new_gens2 = []
	for i in range(len(agent1.gens)):
		delta = math.fabs(agent1.gens[i] - agent2.gens[i]) * 0.5
		new_gens1.append(random.triangular(agent1.gens[i] - delta, agent1.gens[i] + delta))
		new_gens2.append(random.triangular(agent2.gens[i] - delta, agent2.gens[i] + delta))
	new_agent1 = Agent(config, doinit=False)
	new_agent2 = Agent(config, doinit=False)

	new_agent1.gens = new_gens1
	new_agent2.gens = new_gens2
	new_agent1.limit()
	new_agent2.limit()
	return [new_agent1, new_agent2]

def crossing_x3linear(agent1, agent2):
	if len(agent1.gens) != len(agent2.gens):
		raise RuntimeError
	config = get_config(agent1)
	new_gens1 = []
	new_gens2 = []
	new_gens3 = []
	for i in range(len(agent1.gens)):
		new_gens1.append(0.5 * agent1.gens[i] + 0.5 * agent2.gens[i])
		new_gens2.append(1.5 * agent1.gens[i] - 0.5 * agent2.gens[i])
		new_gens3.append(-0.5 * agent1.gens[i] + 1.5 * agent2.gens[i])
	new_agent1 = Agent(config, doinit=False)
	new_agent2 = Agent(config, doinit=False)
	new_agent3 = Agent(config, doinit=False)
	new_agent1.gens = new_gens1
	new_agent2.gens = new_gens2
	new_agent3.gens = new_gens3
	new_agent1.limit()
	new_agent2.limit()
	new_agent3.limit()
	return [new_agent1, new_agent2, new_agent3]
