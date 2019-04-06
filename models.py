import random


class Population:

	# agent - Agent cls
	def __init__(self, agent, population_size, config):
		self._agent_cls = agent
		self.population_size = population_size
		self._agent_config = config

		self.pick = []
		self.selection = []
		self.mutation = []
		self.crossing = []

		self.population = []
		self._init()

	def __len__(self):
		return len(self.population)

	def _init(self):
		for _ in range(self.population_size):
			self.population.append(self._agent_cls(self._agent_config))

	def add_picks(self, *args):
		for func in args:
			self.pick.append(func)

	def add_selections(self, *args):
		for func in args:
			self.selection.append(func)

	def add_mutations(self, *args):
		for func in args:
			self.mutation.append(func)

	def add_crossings(self, *args):
		for func in args:
			self.crossing.append(func)

	def run(self):
		pass


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

