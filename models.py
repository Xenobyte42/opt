import random

from selection import *
from crossing import *
from mutation import *
from pick import *


class Agent:
	precision = 5

	def __init__(self, config, doinit=True):
		self.dimension = config["dimension"]
		self.maximum = config["maximum"]
		self.gens = []
		self.func = config["function"]
		self.calculated = None

		if doinit:
			self._init()
			self.calculated = self.calc()

	def __str__(self):
		s = ""
		for i, gen in enumerate(self.gens):
			s += "x" + str(i) + ": " + str(gen) + ";"
		return s

	def __repr__():
		return self.__str__()

	def _init(self):
		for _ in range(self.dimension):
			self.gens.append(round(random.random() * 2 * self.maximum, 
				self.precision) - self.maximum)

	def calc(self):
		if not self.calculated:
			self.calculated = self.func(self.gens)
		return self.calculated

	def limit(self):
		for i in range(len(self.gens)):
			if self.gens[i] > self.maximum:
				self.gens[i] = self.maximum
			elif self.gens[i] < -self.maximum:
				self.gens[i] = -self.maximum


class Population:
	stagnation_coef = 0.0001
	max_stagnation_iter = 100
	max_iter = 10000

	# agent - Agent cls
	def __init__(self, agent, population_size, config):
		self._agent_cls = agent
		self.population_size = population_size
		self._agent_config = config

		self.population = []
		self._init()

	def __len__(self):
		return len(self.population)

	def _init(self):
		for _ in range(self.population_size):
			self.population.append(self._agent_cls(self._agent_config))

	def best_result(self):
		best = None
		best_idx = None
		for i, agent in enumerate(self.population):
			res = agent.calc()
			if best is None or res < best:
				best = res
				best_idx = i
		return best_idx, best

	def run(self):
		iter_with_stagnation = 0
		last_best = None
		last_best_idx = None
		iter_cnt = 0
		while iter_with_stagnation < self.max_stagnation_iter and iter_cnt < self.max_iter:
			new_population = []
			# 1 / 2 for crossing ("// 4" cuz pick 2)
			for _ in range(self.population_size // 2):
				if iter_cnt % 2:
					first, second = selection_outbreeding(self)
				else:
					first, second = selection_inbreeding(self)
				agent1 = self.population[first]
				agent2 = self.population[second]

				self.population.pop(first)
				if second > first:
					second = second - 1
				self.population.pop(second)

				new_population += [agent1, agent2]
				new_gens = crossing_arithmetical(agent1, agent2)
				new_agents = []
				for gen in new_gens:
					agent = Agent(self._agent_config, doinit=False)
					agent.gens = gen
					agent.limit()
					new_agents.append(agent)
				new_population += new_agents

			# # 1 / 4 for michalewicz
			# for _ in range(self.population_size // 4):
			# 	idx = random.randrange(0, len(self.population) - 1)
			# 	mutation_michalewicz(self.population[idx], iter_cnt / self.max_iter)
			# 	new_population.append(self.population.pop(idx))

			# # 1 / 4 for geometric shift
			# for idx in range(len(self.population)):
			# 	mutation_geometric_shift(self.population[idx], 1 - iter_cnt / self.max_iter)
			self.population += new_population

			# pick new generation
			pick_tourney(self, 10)

			idx, result = self.best_result()
			if last_best is not None and math.fabs(last_best - result) < self.stagnation_coef:
				iter_with_stagnation += 1

			if last_best is None or result < last_best:
				last_best = result
				last_best_idx = idx
			iter_cnt += 1
		print('Result: ', last_best)
		print('Iter: ', iter_cnt)
		print('Genom: ', self.population[last_best_idx])

