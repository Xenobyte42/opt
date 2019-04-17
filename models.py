import random
import datetime
import numpy
import math
from multiprocessing import Manager, Process
from operator import itemgetter

from selection import *
from crossing import *
from mutation import *
from pick import *


class Agent:
	precision = 5

	def __init__(self, config, doinit=True):
		self.dimension = config['dimension']
		self.maximum = config['maximum']
		self.gens = []
		self.func = config['function']
		self.global_min = config['global_min']
		self.calculated = None

		if doinit:
			self._init()
			self.calculated = self.calc()

	def __str__(self):
		s = ''
		for i, gen in enumerate(self.gens):
			s += 'x' + str(i + 1) + ': ' + str(gen) + ';'
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

	def prec(self):
		deviation = 0
		for x in self.gens:
			deviation += math.fabs(x - self.global_min)
		return deviation / self.dimension

	def limit(self):
		for i in range(len(self.gens)):
			if self.gens[i] > self.maximum:
				self.gens[i] = self.maximum
			elif self.gens[i] < -self.maximum:
				self.gens[i] = -self.maximum


class Population:

	# agent - Agent cls
	def __init__(self, agent, population_size, agent_config, config, logfile):
		self._agent_cls = agent
		self._agent_config = agent_config

		self.population_size = config['population_size']
		self.stagnation_coef = config['stag_coef']
		self.max_stagnation_iter = config['max_stag_iter']
		self.max_iter = config['max_iter']
		self.multistart_cnt = config['multistart_cnt']
		self.core_cnt = config['core_cnt']

		self.population = []
		self.log = open(logfile, 'a+')
		self.log.write('[{}]'.format(str(datetime.datetime.now())))
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

	def _run(self):
		self.reinit()
		iter_with_stagnation = 0
		last_best = None
		last_best_idx = None
		iter_cnt = 0
		while iter_with_stagnation < self.max_stagnation_iter and iter_cnt < self.max_iter:
			new_population = []
			# crossing 
			for _ in range(int(self.population_size // 4)):
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

			# other for mutation
			for idx in range(len(self.population)):
				mutation_michalewicz(self.population[idx], iter_cnt / self.max_iter)
			self.population += new_population

			# pick new generation
			pick_tourney(self, 3)

			# get stat
			idx, result = self.best_result()
			if last_best is not None and math.fabs(last_best - result) < self.stagnation_coef:
				iter_with_stagnation += 1
			else:
				iter_with_stagnation = 0

			if last_best is None or result < last_best:
				last_best = result
				last_best_idx = idx
			iter_cnt += 1
		print('Result: ', last_best)
		print('Iter: ', iter_cnt)
		print('Genom: ', self.population[last_best_idx])
		return [last_best, iter_cnt, self.population[last_best_idx]]

	def _run_multi(self, l, cnt):
		for _ in range(cnt):
			l.append(self._run())

	def run(self):
		self.log.write('Function: ' + self._agent_config['function'].__name__ + '\n')
		self.log.write('Dimension: ' + str(self._agent_config['dimension']) + '\n')
		self.log.write('Maximum: ' + str(self._agent_config['maximum']) + '\n')

		best_results = []
		best_genoms = []
		iter_cnts = []
		with Manager() as manager:
			l = manager.list()
			processes = []
			for _ in range(self.core_cnt):
				p = Process(target=self._run_multi, args=(l, int(self.multistart_cnt / self.core_cnt)))
				processes.append(p)
				p.start()
			for p in processes:
				p.join()
			for res in l:
				best_results.append(res[0])
				iter_cnts.append(res[1])
				best_genoms.append(res[2])

		# report logging
		self.log.write('Min f* = {}\n'.format(min(best_results)))
		self.log.write('Mean f* = {}\n'.format(numpy.mean(best_results)))
		best_idx = min(enumerate(best_results), key=itemgetter(1))[0]
		self.log.write('x* = {}\n'.format(best_genoms[best_idx].prec()))
		precs = [gen.prec() for gen in best_genoms]
		self.log.write('Mean x* = {}\n'.format(numpy.mean(precs)))
		self.log.write('Mean t = {}\n'.format(numpy.mean(iter_cnts)))
		self.log.write('All t = {}\n'.format(sum(iter_cnts)))
		self.log.write('RMS f* = {}\n'.format(numpy.std(best_results)))
		self.log.write('RMS t = {}\n'.format(numpy.std(iter_cnts)))

	def reinit(self):
		self.population = []
		self._init()

	def deinit(self):
		self.log.close()
