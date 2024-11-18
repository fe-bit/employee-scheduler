import random
import numpy as np
from typing import List, Callable, Tuple

class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        chromosome_length: int,
        fitness_func: Callable,
        mutation_rate: float = 0.01,
        crossover_rate: float = 0.8,
        elitism: bool = True
    ):
        """
        Initialize the Genetic Algorithm.
        
        Args:
            population_size: Number of individuals in population
            chromosome_length: Length of binary string representing solution
            fitness_func: Function to evaluate fitness of a chromosome
            mutation_rate: Probability of mutation for each gene
            crossover_rate: Probability of crossover between parents
            elitism: Whether to preserve the best solution in each generation
        """
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.fitness_func = fitness_func
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism
        self.population = self._initialize_population()
        
    def _initialize_population(self) -> List[str]:
        """Create initial random population."""
        return [
            ''.join(random.choice('01') for _ in range(self.chromosome_length))
            for _ in range(self.population_size)
        ]
    
    def _calculate_fitness(self, chromosome: str) -> float:
        """Calculate fitness for a chromosome using the provided fitness function."""
        return self.fitness_func(chromosome)
    
    def _select_parent(self, fitness_values: List[float]) -> str:
        """Select parent using tournament selection."""
        tournament_size = 3
        tournament_indices = random.sample(range(self.population_size), tournament_size)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return self.population[winner_index]
    
    def _crossover(self, parent1: str, parent2: str) -> Tuple[str, str]:
        """Perform crossover between two parents."""
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(1, self.chromosome_length - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]
            return child1, child2
        return parent1, parent2
    
    def _mutate(self, chromosome: str) -> str:
        """Apply mutation to a chromosome."""
        mutated = list(chromosome)
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = '1' if mutated[i] == '0' else '0'
        return ''.join(mutated)
    
    def evolve(self, generations: int) -> Tuple[str, float, List[float]]:
        """
        Evolve the population for the specified number of generations.
        
        Returns:
            Tuple containing:
            - Best chromosome found
            - Best fitness value
            - List of best fitness values per generation
        """
        best_fitness_history = []
        best_chromosome = None
        best_fitness = float('-inf')
        
        for generation in range(generations):
            # Calculate fitness for all chromosomes
            fitness_values = [self._calculate_fitness(chrom) for chrom in self.population]
            
            # Track best solution
            generation_best_fitness = max(fitness_values)
            generation_best_index = fitness_values.index(generation_best_fitness)
            generation_best_chromosome = self.population[generation_best_index]
            
            if generation_best_fitness > best_fitness:
                best_fitness = generation_best_fitness
                best_chromosome = generation_best_chromosome
            
            best_fitness_history.append(best_fitness)
            
            # Create new population
            new_population = []
            
            # Elitism: preserve best solution
            if self.elitism:
                new_population.append(generation_best_chromosome)
            
            # Generate new individuals
            while len(new_population) < self.population_size:
                # Select parents
                parent1 = self._select_parent(fitness_values)
                parent2 = self._select_parent(fitness_values)
                
                # Create offspring
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutate offspring
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Ensure population size remains constant
            self.population = new_population[:self.population_size]
        
        return best_chromosome, best_fitness, best_fitness_history

# Example usage for solving a simple maximization problem
def example_usage():
    # Example fitness function: maximize the number of 1's in the binary string
    def fitness_function(chromosome: str) -> float:
        return sum(int(gene) for gene in chromosome)
    
    # Initialize GA
    ga = GeneticAlgorithm(
        population_size=100,
        chromosome_length=20,
        fitness_func=fitness_function,
        mutation_rate=0.01,
        crossover_rate=0.8,
        elitism=True
    )
    
    # Run evolution
    best_solution, best_fitness, fitness_history = ga.evolve(generations=50)
    
    print(f"Best solution: {best_solution}")
    print(f"Best fitness: {best_fitness}")
    
    # Plot fitness history
    import matplotlib.pyplot as plt
    plt.plot(fitness_history)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Fitness Evolution')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    example_usage()