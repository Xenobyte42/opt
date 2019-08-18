
from models import *
from functions import *

if __name__ == "__main__":
	algo = EvolutionAlgorithm(func=rozenbrock_function, dimension=32, bounds=5.12, max_iter=1000,
								mutation_func='geometric_shift', crossing_func='fuzzy')
	algo.evolve()

