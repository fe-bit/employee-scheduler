from optimizations.genetic_algorithm import GeneticAlgorithm
from optimizations.genetic_algorithm.genetic_algorithm_tabu import GeneticAlgorithmTabu
from optimizations.brute_force import BruteForce
import time
from shifts import get_total_work_hours_per_employee, get_shifts_per_employee

EMPLOYEES = 20

def genetic():
    t0 = time.time()
    genetic_algorithm = GeneticAlgorithmTabu(population_size=1000, mutation_rate=0.01, employees=EMPLOYEES)
    best_chromosome, best_fitness, best_fitness_history = genetic_algorithm.evolve(1000000, target_fitness=0)
    t1 = time.time()
    print(best_chromosome)
    print(best_fitness)
    print("Search took:", t1-t0, "s")
    print(get_total_work_hours_per_employee(get_shifts_per_employee(genetic_algorithm.shifts, best_chromosome)))


def brute_force():
    t0 = time.time()
    bf = BruteForce(employees=EMPLOYEES)
    best_chromosome, best_fitness, best_fitness_history= bf.run()
    t1 = time.time()
    print(best_chromosome)
    print(best_fitness)
    print("Search took:", t1-t0, "s")


genetic()
