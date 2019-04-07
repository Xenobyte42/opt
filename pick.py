import random


def pick_best(group):
	best_idx = None
	best_result = None
	for i, agent in enumerate(group):
		if best_result is None or agent.calc() < best_result:
			best_result = agent.calc()
			best_idx = i
	best_agent = group.pop(best_idx)
	return best_agent, group

def pick_tourney(population, n):
	agents = population.population

	new_agents = []
	# Пока есть агенты в списке
	for _ in range(population.population_size):
		# Создаем группу
		group = []
		# Заполняем ее
		for _ in range(n):
			if not agents:
				break
			group.append(agents.pop(random.randint(0, len(agents) - 1)))
		best_agent, group = pick_best(group)
		new_agents.append(best_agent)
		# Остатки выбираем снова( херовое место, надо порефакторить)
		agents += group
	population.population = new_agents
