import logging

from models import *
from functions import *
from scipy import optimize
import time

"""
	Модуль расчетов. Требуется менять содержимое 2 словарей-конфигов:
		# TEST_FUNCS:
		Словарь с тестируемыми функциями. В случае добавления новой функции просто добавить ее
		в словарь аналогично существующим

		# CONFIG:
		Конфиг для тестов алгоритма:
			- log_path - путь до файла, в которые будут писаться логи;
			- start_cnt - кол-во мультистартов алгоритма;
			- test_func - тестируемая функция из словаря TEST_FUNCS;
			- dimension - целое число, кратное двум, обозначает размерность вектора 'x';
			- bounds - пределы исследования тестовой функции. Тут может быть два варианта задания:
				- число типа float. Будет рассматриваться интервал [-bounds; +bounds]
				- список из двух чисел, где первое меньше второго. Будет рассматриваться интервал,
				соответствующий интервалу, обозначенному в списке;
			- max_iter - максимальное число итераций алгоритма;
			- mutation_func - функция мутации. В данный момент в алгоритме реализованы следующие функции:
				- michalewicz
				- gauss
				- geometric_shift
			- crossing_func - функция скрещивания. В данный момент в алгоритме реализованы следующие функции:
				- arithmetical
				- fuzzy
				- x3linear
			- selection_func - функция селекции. В данный момент в алгоритме реализованы следующие функции:
				- outbreeding
				- inbreeding
			- pick_func - функция отбора. В данный момент в алгоритме реализованы следующие функции:
				- tourney
			- global_min - значение x составляющей вектора глобального минимума. В случае если вектор состоит из 
			одинаковых компонент достаточно просто указать число. Если в будущем появятся функции с более сложными
			векторами глобальных минимумов, нужно будет указывать список нужной размерности. Некоторая справка по
			глобальным минимумам реализованных функций:
				- Сферическая - вектор нужной размерности из 0;
				- Розенброк - вектор нужной размерности из 1;
				- Растригин - вектор нужной размерности из 0;
				- Шекель - вектор нужной размерности из 2;

"""

TEST_FUNCS = {
	"sphere": sphere_function,
	"rozenbrock": rozenbrock_function,
	"rastr": rastr_function,
	"shekell": shekell_function,
}

CONFIG = {
	"log_path": "log.txt",
	"start_cnt": 100,
	"test_func": TEST_FUNCS["sphere"],
	"dimension": 2,
	"bounds": 5.12,
	"max_iter": 1000,
	"mutation_func": "geometric_shift",
	"crossing_func": "fuzzy",
	"selection_func": "outbreeding",
	"pick_func": "tourney",
	"global_min": 0,
}

CONFIG["global_min"] = [CONFIG["global_min"]] * CONFIG["dimension"]

def setup_logging(log_file="log.txt"):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)

	file_handler = logging.FileHandler(log_file)
	file_formatter=logging.Formatter("[%(asctime)s]   %(message)s")
	file_handler.setFormatter(file_formatter)
	logger.addHandler(file_handler)
	return logger

def calc_disp(vec_x):
	disp = 0.0
	for i in range(CONFIG["dimension"]):
		disp += np.power(vec_x[i] - CONFIG["global_min"][i], 2)
	return disp / CONFIG["dimension"]

def start():
	logger = setup_logging(CONFIG["log_path"])
	logger.info("Function: " + CONFIG["test_func"].__name__)
	logger.info("Dimension: " + str(CONFIG["dimension"]))
	logger.info("Bound (0 +- val): " + str(CONFIG["bounds"]))
	logger.info("Mutaion func: " + CONFIG["mutation_func"])
	logger.info("Crossing func: " + CONFIG["crossing_func"])
	logger.info("Selection func: " + CONFIG["selection_func"])
	logger.info("Pick func: " + CONFIG["pick_func"] + "\n")

	best_results = []
	best_vectors = []
	iterations = []
	for _ in range(CONFIG["start_cnt"]):
		algo = EvolutionAlgorithm(func=CONFIG["test_func"], dimension=CONFIG["dimension"], 
								  bounds=CONFIG["bounds"], max_iter=CONFIG["max_iter"],
								  mutation_func=CONFIG["mutation_func"], crossing_func=CONFIG["crossing_func"],
								  pick_func=CONFIG["pick_func"])
		out = algo.evolve()
		best_results.append(out.value)
		best_vectors.append(out.vector)
		iterations.append(out.iter_cnt)
	best_results = np.array(best_results)
	best_vectors = np.array(best_vectors)
	iterations = np.array(iterations)

	min_idx = best_results.argmin()
	best_disp = calc_disp(best_vectors[min_idx])
	dispersions = [calc_disp(vec_x) for vec_x in best_vectors]
	logger.info("Min f* = {}".format(np.amin(best_results)))
	logger.info("Min vec x: {}".format(str(best_vectors[min_idx])))
	logger.info("Dispersion best x by x = {}".format(best_disp))
	logger.info("Mean dispersion x by x = {}".format(np.mean(dispersions)))
	logger.info("Mean f* = {}".format(np.mean(best_results)))
	logger.info("Mean t = {}".format(np.mean(iterations)))
	logger.info("All t = {}".format(np.sum(iterations)))
	logger.info("RMS f* = {}".format(np.std(best_results)))
	logger.info("RMS t = {}\n".format(np.std(iterations)))

if __name__ == "__main__":
	start()
