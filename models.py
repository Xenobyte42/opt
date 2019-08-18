import datetime
import numpy as np


class EvolutionAlgorithm:

	class EvolutionAlgorithmException(RuntimeError):

		"""Evolution algorithm class exception"""
		pass

	class EvolveOutput:
		"""Class for output. Just for fun"""

		def	__init__(self, value, vector, iter_cnt):
			self.value = value
			self.vector = vector
			self.iter_cnt = iter_cnt

	"""Mutation functions"""

	def mutation_michalewicz(self, vec_x, temp_iter=0):
		"""
		Parameters:
		-----------
		vec_x: iterable
			Vector for mutation
		temp_iter: int, optional
			Сurrent iteration step

		Returns:
    	-----------
		new_x: iterable
			Mutated vector same size as vec_x
		"""
		def func(val):
			coef = 0.8 + 0.2 * temp_iter / self.__max_iter
			u = np.random.random()
			return val * (1 - u ** ((1 - (coef)) ** 5))

		new_x = []

		for x in vec_x:
			if np.random.randint(0, 2):
				new_x.append(x + func(self.__bounds[1] - x))
			else:
				new_x.append(x - func(x - self.__bounds[1]))
		for i, x in enumerate(new_x):
			new_x[i] = self._limit(x)
		return np.array(new_x)
	
	def mutation_gauss(self, vec_x, temp_iter=0):
		"""
		Parameters:
		-----------
		vec_x: iterable
			Vector for mutation
		temp_iter: int, optional
			Сurrent iteration step

		Returns:
    	-----------
		new_x: iterable
			Mutated vector same size as vec_x
		"""
		new_x = []

		for x in vec_x:
			new_x.append(x + np.random.normal(0, 0.1 * temp_iter / self.__max_iter))
		for i, x in enumerate(new_x):
			new_x[i] = self._limit(x)
		return np.array(new_x)

	def mutation_geometric_shift(self, vec_x, temp_iter=0):
		"""
		Parameters:
		-----------
		vec_x: iterable
			Vector for mutation
		temp_iter: int, optional
			Сurrent iteration step

		Returns:
    	-----------
		new_x: iterable
			Mutated vector same size as vec_x
		"""
		new_x = []
		coef = temp_iter / self.__max_iter
		for x in vec_x:
			u = np.random.random()
			new_x.append(x - x * coef * (2 * u - 1))
		for i, x in enumerate(new_x):
			new_x[i] = self._limit(x)
		return np.array(new_x)

	mutation_funcs = {
		"michalewicz": mutation_michalewicz,
		"gauss": mutation_gauss,
		"geometric_shift": mutation_geometric_shift,
	}

	"""Crossing functions"""

	def crossing_arithmetical(self, vec_x1, vec_x2):
		"""
		Parameters:
		-----------
		vec_x1: iterable
			First vector for crossing
		vec_x2: iterable
			Second vector for crossing

		Returns:
    	-----------
		result: iterable
			Vector (1, 2) which contains crossed vectors
		"""
		new_vec1 = []
		new_vec2 = []
		for i in range(len(vec_x1)):
			u = np.random.random()
			new_vec1.append(u * vec_x1[i] + (1 - u) * vec_x2[i])
			new_vec2.append(u * vec_x1[i] - (1 - u) * vec_x2[i])
		return [np.array(new_vec1), np.array(new_vec2)]
	
	def crossing_fuzzy(self, vec_x1, vec_x2):
		"""
		Parameters:
		-----------
		vec_x1: iterable
			First vector for crossing
		vec_x2: iterable
			Second vector for crossing

		Returns:
    	-----------
		result: iterable
			Vector (1, 2) which contains crossed vectors
		"""
		new_vec1 = []
		new_vec2 = []
		for i in range(len(vec_x1)):
			delta = np.fabs(vec_x1[i] - vec_x2[i]) * 0.5 + 0.001
			new_vec1.append(np.random.triangular(vec_x1[i] - delta, vec_x1[i], vec_x1[i] + delta))
			new_vec2.append(np.random.triangular(vec_x2[i] - delta, vec_x2[i], vec_x2[i] + delta))
		return [np.array(new_vec1), np.array(new_vec2)]

	def crossing_x3linear(vec_x1, vec_x2):
		"""
		Parameters:
		-----------
		vec_x1: iterable
			First vector for crossing
		vec_x2: iterable
			Second vector for crossing
		vec_x3: iterable
			Third vector for crossing

		Returns:
    	-----------
		result: iterable
			Vector (1, 3) which contains crossed vectors
		"""
		new_vec1 = []
		new_vec2 = []
		new_vec3 = []
		for i in range(len(vec_x1)):
			new_vec1.append(0.5 * vec_x1[i] + 0.5 * vec_x2[i])
			new_vec2.append(1.5 * vec_x1[i] - 0.5 * vec_x2[i])
			new_vec3.append(-0.5 * vec_x1[i] + 1.5 * vec_x2[i])
		return [np.array(new_vec1), np.array(new_vec2), np.array(new_vec3)]

	crossing_funcs = {
		"arithmetical": crossing_arithmetical,
		"fuzzy": crossing_fuzzy,
		"x3linear": crossing_x3linear,
	}

	"""Selection functions"""

	def __calc_distance(self, vec_x1, vec_x2):
		"""
		Parameters:
		-----------
		vec_x1: iterable
			First vector for calculating
		vec_x2: iterable
			Second vector for calculating

		Returns:
    	-----------
		distance: float32
			Distance between two vectors
		"""
		distance = 0
		for i in range(len(vec_x1)):
			distance += np.fabs(vec_x1[i] - vec_x2[i])
		return distance 

	def breeding_wrapper(func):
		"""
		Function wrapper for outbreeding and inbreeding
		Returns:
    	-----------
		result: callable
			Function-wrapper
		"""
		def wrapped(self):
			"""
			Select 2 indexes for crossing
			Returns:
			-----------
			result: iterable
				List with two sample indexes for crossing
			"""
			first_idx = np.random.randint(0, len(self.__population))
			distances = []
			sum_dist = 0
			for i in range(len(self.__population)):
				if i == first_idx:
					continue
				distance = self.__calc_distance(self.__population[first_idx], self.__population[i])
				sum_dist += distance
				distances.append(distance)
			probabilities = [d / sum_dist for d in distances]
			probabilities = func(self, distances, sum_dist)
			second_idx = np.random.choice(len(self.__population) - 1, 1,
				p=probabilities)[0]
			if second_idx >= first_idx:
				second_idx += 1
			return [first_idx, second_idx]
		return wrapped

	@breeding_wrapper
	def selection_outbreeding(self, distances, sum_dist):
		"""
		Parameters:
		-----------
		distances: iterable
			List of distances between two vectors
		sum_dist: float32
			Sum distance between all vectors

		Returns:
    	-----------
		result: iterable
			List of probabilities for selection picking
		"""
		return [d / sum_dist for d in distances]

	@breeding_wrapper
	def selection_inbreeding(self, distances, sum_dist):
		"""
		Parameters:
		-----------
		distances: iterable
			List of distances between two vectors
		sum_dist: float32
			Sum distance between all vectors

		Returns:
    	-----------
		result: iterable
			List of probabilities for selection picking
		"""
		return [1.0 - d / sum_dist for d in distances]
	
	selection_funcs = {
		"outbreeding": selection_outbreeding,
		"inbreeding": selection_inbreeding,
	}

	"""Pick functions"""

	def pick_tourney(self, mixed_population, mixed_values, n):
		"""
		Parameters:
		-----------
		mixed_population: iterable
			List of vectors which contains old and new populations
		mixed_population: 
			List of vectors which contains calculated values
		n: int
			Count samples in each group

		Returns:
    	-----------
		result: iterable
			Tuple with new populations vector and new values vector
		"""
		new_population = []
		for _ in range(self.__popsize):
			group_idxs = []
			for _ in range(n):
				group_idxs.append(np.random.randint(0, len(mixed_population)))
			best_idx = min(group_idxs, key=lambda idx: mixed_values[idx])
			new_population.append(mixed_population.pop(best_idx))
			mixed_values.pop(best_idx)
		return (np.array(new_population), np.array(mixed_values))

	pick_funcs = {
		"tourney": pick_tourney,
	}

	def __init__(self, func, dimension, bounds, max_iter=1000, 
				 stagnation_coef=0.01, popsize=10, mutation_func="michalewicz",
				 crossing_func="arithmetical", selection_func="outbreeding", pick_func="tourney"):
		"""
		Parameters:
		-----------
		func: callable
			Function to be minimized. Must accept 'x' vector and return 'float32' result
		dimension: int
			Dimension of vector 'x'. Must be in range [2; +inf)
		bounds: sequence or int
			If 'bounds' is iterable:
				- 'bounds' length must be equals 2;
				- 'bounds[0]' < 'bounds[1]';
			If 'bounds' is 'float32':
				- 'bounds' must be > 0;
		max_iter: int, optional
			Max count of iterations. Must be > 0
		stagnation_coef: float32
			Coeficient of stagnation. Work when last 10% of iterations dont give difference. Must be >= 0 and < 1
		popsize: int
			Size of the population. Must be > 0
		mutation_func: callable
			Function which implements mutation. Must accept 'x' vector and 'coef' and return new vector same size
			Implemented:
			- michalewicz
			- gauss
			- geometric_shift
		crossing_func:
			Function which implements crossing. Must accept 2 'x' vectors and return new 2
			Implemented:
			- arithmetical
			- fuzzy
			- x3linear
		selection_func:
			Function which implements selection. Must return 2 sample indexes for crossing
			Implemented:
			- outbreeding
			- inbreeding
		pick_func:
			Function which implements pick logic. Must accept mixed population and return new population
			Implemented:
			- tourney
		"""
		self.__func = func
		self.__mutation_func = self.mutation_funcs[mutation_func]
		self.__crossing_func = self.crossing_funcs[crossing_func]
		self.__selection_func = self.selection_funcs[selection_func]
		self.__pick_func = self.pick_funcs[pick_func]
		if dimension < 2:
			raise self.EvolutionAlgorithmException("dimension must be >= 2")
		self.__dim = dimension

		if hasattr(bounds, "__iter__") and len(bounds) == 2:
			if bounds[0] >= bounds[1]:
				raise self.EvolutionAlgorithmException("min bound must be < max bound")
			self.__bounds = np.array(bounds)
		else:
			if bounds <= 0:
				raise self.EvolutionAlgorithmException("bound must be > 0")
			self.__bounds = np.array([-bounds, bounds])

		if max_iter <= 0:
			raise self.EvolutionAlgorithmException("max count of iterations must be > 0")
		self.__max_iter = max_iter

		if stagnation_coef < 0 and stagnation_coef >= 1:
			raise self.EvolutionAlgorithmException("stagnation coef must be >= 0 and < 1")
		self.__stag_coef = stagnation_coef

		if popsize < 1:
			raise self.EvolutionAlgorithmException("population size must be > 0")
		self.__popsize = popsize
		self._init_population()

	def _init_population(self):
		"""Generate population matrix, where row count = popsize and calculate function values"""
		self.__population = (self.__bounds[1] - self.__bounds[0]) * \
							np.random.random_sample((self.__popsize, self.__dim)) + self.__bounds[0]
		self.__values = np.array([self.__func(vec_x) for vec_x in self.__population])
		self.__mutated_population = np.array([self.__mutation_func(self, vec_x) for vec_x in self.__population])
		self.__mutated_values = np.array([self.__func(vec_x) for vec_x in self.__mutated_population])
		self.__Q = np.arange(0.1, 0.1 * (self.__max_iter + 1), 0.1)[::-1]
	
	def _limit(self, x):
		"""Limit x values in interval (-bound; bound)"""
		if x >= self.__bounds[0] and x <= self.__bounds[1]:
			return x
		if x < self.__bounds[0]:
			return self.__bounds[0]
		if x > self.__bounds[1]:
			return self.__bounds[1]

	def evolve(self):
		"""Evolve function. Implement evolve cycle with mutation and crossing"""
		min_val = None
		min_vec = None

		temp_iter = 0
		iter_with_stagnation = 0
		max_iter_with_stagnation = int(self.__max_iter * 0.1)
		while temp_iter < self.__max_iter and iter_with_stagnation < max_iter_with_stagnation:
			self.__mutate(temp_iter)
			self.__cross()

			temp_min_idx = self.__values.argmin()
			if min_val is None or self.__values[temp_min_idx] < min_val:
				min_val = self.__values[temp_min_idx]
				min_vec = self.__population[temp_min_idx]
			if self.__values[temp_min_idx] - min_val < 0.001:
				iter_with_stagnation += 1
			else:
				iter_with_stagnation = 0
			temp_iter += 1
		return self.EvolveOutput(min_val, min_vec, temp_iter)
	
	def __mutate(self, temp_iter):
		"""Mutate population. Implements an annealing simulation algorithm"""
		def accept_mutation(temp_iter):
			if self.__mutated_values[i] < self.__values[i]:
				return True
			p = np.exp(-(self.__mutated_values[i] - self.__values[i]) / self.__Q[temp_iter])
			if np.random.binomial(1, p):
				return True
			return False

		self.__mutated_population = np.array([self.__mutation_func(self, vec_x, temp_iter) 
											  for vec_x in self.__population])
		self.__mutated_values = np.array([self.__func(vec_x) for vec_x in self.__mutated_population])

		for i in range(self.__population.shape[0]):
			if accept_mutation(temp_iter):
				self.__population[i] = self.__mutated_population[i]
				self.__values[i] = self.__mutated_values[i]

	def __cross(self):
		"""Generate new population. Implement selection, crossing and pick algorithms"""
		new_population = []
		for _ in range(int(self.__popsize / 2)):
			first_idx, second_idx = self.__selection_func(self)
			new_population += self.__crossing_func(self, self.__population[first_idx], self.__population[second_idx])
		mixed_population = list(self.__population) + new_population
		mixed_values = [self.__func(vec_x) for vec_x in mixed_population]
		self.__population, self.__values = self.__pick_func(self, mixed_population, mixed_values, 3)

