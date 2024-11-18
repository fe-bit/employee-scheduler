from optimizations.genetic_algorithm import GeneticAlgorithm

genetic_algorithm = GeneticAlgorithm(population_size=10, mutation_rate=0.01)
best_chromosome, best_fitness, best_fitness_history = genetic_algorithm.evolve(50000)
print(best_fitness)
